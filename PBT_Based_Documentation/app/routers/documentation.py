"""File handles the route logic for documentation. 
This includes getting all documentation, getting documentation only with user, 
getting only IBD documentation, and getting on TD documentation
"""

import json
import admin
from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
import models 
import schemas
from schemas import (
    Documentation,
    DocumentationResponse,
    InvariantsUpdate,
    PostIBDResponse,
    PostTDResponse,
    UserIBDResponse,
    UserTDResponse,
)
import database 
from database import get_db 
import oath2
import utils
import legacy_backend
from task_runner import export_csv
from tasks.export_tasks import export_documentation_table_csv_celery


router = APIRouter(
    prefix="/documentation", tags=["documentation"]
)

api_router = APIRouter(prefix="/api", tags=["legacy documentation api"])


def can_manage_documentation(doc: models.Documentation, curr_user: models.User, db: Session) -> bool:
    """Allow owners and admin users to manage a documentation row."""
    if doc.owner_id == curr_user.id:
        return True
    return db.query(models.AdminUser).filter(models.AdminUser.email == curr_user.email).first() is not None


def legacy_error(exc: Exception) -> JSONResponse:
    """Keep old server.py-style validation errors as JSON 400s."""
    status_code = status.HTTP_400_BAD_REQUEST if isinstance(exc, ValueError) else status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content={"error": str(exc)})


# The anonymous /api/... generation flow has no logged-in user, but the
# Documentation table requires an owner. Persist generations under a shared
# placeholder account so saving works without changing the existing schema.
ANONYMOUS_OWNER_EMAIL = "anonymous@local"
STREAM_END = object()


def get_anonymous_owner_id(db: Session) -> int:
    """Get (or lazily create) the placeholder owner for anonymous generations."""
    owner = db.query(models.User).filter(models.User.email == ANONYMOUS_OWNER_EMAIL).first()
    if owner is None:
        owner = models.User(email=ANONYMOUS_OWNER_EMAIL, password=utils.hash("anonymous"))
        db.add(owner)
        db.commit()
        db.refresh(owner)
    return owner.id


def serialize_invariants(invariants) -> str | None:
    """Store lists/dicts as JSON text while leaving hand-written strings alone."""
    if invariants is None:
        return None
    if isinstance(invariants, str):
        return invariants
    return json.dumps(invariants)


def persist_generated_documentation(db: Session, payload: dict, markdown: str):
    """Save a generated documentation row (markdown + approved invariants).

    Returns the saved row, or None if persistence failed (saving must never
    break the generation response the frontend is waiting on).
    """
    try:
        doc = models.Documentation(
            owner_id=get_anonymous_owner_id(db),
            documentation_title=str(payload.get("api_name") or "api.function"),
            source_code=str(payload.get("source_code") or payload.get("documentation") or ""),
            IBD_generated_md=markdown or "",
            # The generation flow only produces invariant-based docs; keep the
            # NOT NULL traditional-docs column satisfied with an empty string.
            TD_md="",
            invariants=serialize_invariants(payload.get("invariants")),
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc
    except Exception:
        db.rollback()
        return None


def next_stream_chunk(iterator):
    try:
        return next(iterator)
    except StopIteration:
        return STREAM_END


def persist_generated_documentation_in_new_session(payload: dict, markdown: str):
    db = database.SessionLocal()
    try:
        return persist_generated_documentation(db, payload, markdown)
    finally:
        db.close()


def documentation_response_rows(db: Session, docs: list[models.Documentation], curr_user: models.User | None = None):
    """Attach assessment question/response counts to documentation rows."""
    doc_ids = [doc.id for doc in docs]
    if not doc_ids:
        return []

    question_counts = dict(
        db.query(
            models.AssessmentQuestion.documentation_id,
            func.count(models.AssessmentQuestion.id),
        )
        .filter(models.AssessmentQuestion.documentation_id.in_(doc_ids))
        .group_by(models.AssessmentQuestion.documentation_id)
        .all()
    )

    response_query = (
        db.query(
            models.AssessmentQuestion.documentation_id,
            func.count(models.AssessmentAnswer.id),
        )
        .join(models.AssessmentAnswer, models.AssessmentAnswer.question_id == models.AssessmentQuestion.id)
        .filter(models.AssessmentQuestion.documentation_id.in_(doc_ids))
    )
    if curr_user is not None and db.query(models.AdminUser).filter(models.AdminUser.email == curr_user.email).first() is None:
        response_query = response_query.filter(models.AssessmentAnswer.user_id == curr_user.id)
    response_counts = dict(response_query.group_by(models.AssessmentQuestion.documentation_id).all())

    rows = []
    for doc in docs:
        row = DocumentationResponse.model_validate(doc).model_dump()
        row["question_count"] = int(question_counts.get(doc.id, 0) or 0)
        row["response_count"] = int(response_counts.get(doc.id, 0) or 0)
        rows.append(row)
    return rows


@api_router.post("/source")
async def lookup_source(payload: dict):
    """Drop-in FastAPI replacement for server.py's /api/source endpoint."""
    try:
        return await run_in_threadpool(legacy_backend.resolve_source, str(payload.get("object_name") or ""))
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/invariants")
async def generate_invariants(payload: dict):
    """Generate candidate invariants from pasted or looked-up source code."""
    try:
        return await run_in_threadpool(legacy_backend.generate_invariants, payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/documentation")
async def generate_documentation(payload: dict, db: Session = Depends(get_db)):
    """Generate invariant-based Markdown documentation and save it."""
    try:
        result = await run_in_threadpool(legacy_backend.generate_documentation, payload)
        doc = persist_generated_documentation(db, payload, result.get("markdown", ""))
        if doc is not None:
            result["documentation_id"] = doc.id
        return result
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/td-markdown")
async def format_traditional_documentation(payload: dict):
    """Convert pasted traditional/reference docs into Markdown for Arena."""
    try:
        return await run_in_threadpool(legacy_backend.generate_traditional_markdown, payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/documentation-stream")
async def generate_documentation_stream(payload: dict):
    """Stream generated Markdown, then persist the full document once complete."""
    try:
        async def streamer():
            chunks: list[str] = []
            iterator = legacy_backend.stream_documentation(payload)
            while True:
                chunk = await run_in_threadpool(next_stream_chunk, iterator)
                if chunk is STREAM_END:
                    break
                chunks.append(chunk)
                yield chunk
            # Save only after the full markdown has streamed to the client.
            markdown = legacy_backend.strip_markdown_fences("".join(chunks))
            if not payload.get("skip_anonymous_save"):
                await run_in_threadpool(persist_generated_documentation_in_new_session, payload, markdown)

        return StreamingResponse(streamer(), media_type="text/plain; charset=utf-8")
    except Exception as exc:
        return legacy_error(exc)

@router.get("/", response_model=list[DocumentationResponse])
async def get_all_documentation(
    db:Session = Depends(get_db),
    curr_user:Session = Depends(admin.get_current_admin)
):
    """Function gets every single documentation generated"""
    return documentation_response_rows(db, db.query(models.Documentation).all(), curr_user)

# USER ENDPOINT LOGIC START-----
@router.get("/me", response_model=list[DocumentationResponse])
async def get_current_user_documentation(
    db:Session = Depends(get_db),
    curr_user:models.User = Depends(oath2.get_current_user)
):
    """Function gets all documentation owned by the current user"""
    if db.query(models.AdminUser).filter(models.AdminUser.email == curr_user.email).first():
        return documentation_response_rows(db, db.query(models.Documentation).all(), curr_user)
    all_docs = db.query(models.Documentation).filter(models.Documentation.owner_id == curr_user.id).all()
    return documentation_response_rows(db, all_docs, curr_user)

@router.get("/me/ibd", response_model=UserIBDResponse)
async def get_current_user_ibd(db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """Function gets the IBD documentation relating to the user"""
    ibd = db.query(models.Documentation.IBD_generated_md).filter(models.Documentation.owner_id == curr_user.id).all()
    return {"user_ibd": [row[0] for row in ibd]}

@router.get("/me/td", response_model=UserTDResponse)
async def get_current_user_td(db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """Function gets the td documentation relating to the user"""
    td = db.query(models.Documentation.TD_md).filter(models.Documentation.owner_id == curr_user.id).all()
    return {"user_td": [row[0] for row in td]}
# USER ENDPOINT LOGIC END----


# Export all the documentation data through the Celery/Redis queue (the frontend
# polls the returned task id), or inline as a direct CSV when the broker is down.
@router.get("/export")
async def export_documentation_as_csv(curr_user:Session = Depends(admin.get_current_admin)):
    """This function exports every single data in the documentation table so that future reserach can be done"""
    return await export_csv(export_documentation_table_csv_celery)


# LOGIC FOR Invariants (used by stored documentation records)
@router.get("/invariants/{id}")
async def get_invariants(id:int, db:Session=Depends(get_db)):
    """function gets all ivnairants related to the post"""
    invariants = db.query(models.Documentation.invariants).filter(models.Documentation.id == id).scalar()
    if invariants is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} cannot be found/NO invariants")
    try:
        return {"invariants": json.loads(invariants)}
    except json.JSONDecodeError:
        return {"invariants": invariants}


@router.put("/{id}/invariants", response_model=DocumentationResponse)
async def update_invariants(
    id: int,
    payload: InvariantsUpdate,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oath2.get_current_user)
):
    """Update only the invariants column for a stored documentation row."""
    doc = db.query(models.Documentation).filter(
        models.Documentation.id == id
    ).first()

    if not doc:
        raise HTTPException(status_code=404, detail="Documentation not found")

    if not can_manage_documentation(doc, curr_user, db):
        raise HTTPException(status_code=403, detail="Not authorized")

    # Store lists/dicts as JSON text while still allowing hand-written strings.
    doc.invariants = (
        json.dumps(payload.invariants)
        if not isinstance(payload.invariants, str)
        else payload.invariants
    )
    db.commit()
    db.refresh(doc)

    return doc


# POST ID ENDPOINT LOGIC START----
@router.get("/{id}", response_model = DocumentationResponse)
async def get_documentation_by_post_id(id:int, db:Session = Depends(get_db)):
    """Function gets the documentation based off of the post id"""
    docs = db.query(models.Documentation).filter(models.Documentation.id == id).first()
    if not docs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"POST ID: {id} not found")
    return docs

@router.get("/{id}/ibd", response_model=PostIBDResponse)
async def get_only_ibd(id:int, db:Session = Depends(get_db)):
    """Function only gets IBD via post id"""
    # Get only the IBD column and only with the post id
    ibd = db.query(models.Documentation.IBD_generated_md).filter(models.Documentation.id == id).scalar()
    return {"post_IBD": ibd}

@router.get("/{id}/td", response_model=PostTDResponse)
async def get_only_ibd(id:int, db:Session = Depends(get_db)):
    """Function only gets TD via post id"""
    # Get only the IBD column and only with the post id
    td = db.query(models.Documentation.TD_md).filter(models.Documentation.id == id).scalar() # scalar only gets one
    return {"post_TD":td}
# POST ID ENDPOINT LOGIC END----


# Create Documentation Endpoint
@router.post("/create_ibd", response_model=DocumentationResponse)
async def create_IBD(ibd_doc:Documentation, db:Session=Depends(get_db), curr_user:Session=Depends(oath2.get_current_user)):
    """Function lets user create their own posts :D """
    new_ibd_docs = models.Documentation(owner_id=curr_user.id, **ibd_doc.model_dump())
    db.add(new_ibd_docs)
    db.commit()
    db.refresh(new_ibd_docs)
    return new_ibd_docs

# Update the Documentation Endpoint
@router.put("/update_ibd/{id}", response_model=DocumentationResponse)
async def update_IBD(id:int, ibd_doc:Documentation, db:Session=Depends(get_db), curr_user:Session=Depends(oath2.get_current_user)):
    """Function lets users update their documentation"""
    post_query = db.query(models.Documentation).filter(models.Documentation.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"POST ID: {id} CANNOT BE FOUND")
    if not can_manage_documentation(post, curr_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.update(ibd_doc.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@router.put("/{id}/td", response_model=DocumentationResponse)
async def update_TD(
    id: int,
    payload: dict,
    db: Session = Depends(get_db),
    curr_user: models.User = Depends(oath2.get_current_user)
):
    """Update only the traditional/reference Markdown for a saved document."""
    post = db.query(models.Documentation).filter(models.Documentation.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"POST ID: {id} CANNOT BE FOUND")
    if not can_manage_documentation(post, curr_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post.TD_md = str(payload.get("TD_md") or payload.get("td_md") or "")
    db.commit()
    db.refresh(post)
    return post

# DELETE the documentation endpoint

@router.delete("/delete/{id}")
async def delete_docs(
    id:int,
    db:Session=Depends(get_db),
    curr_user:models.User=Depends(oath2.get_current_user)
):
    """Delete one saved documentation row owned by the current user."""
    post_query = db.query(models.Documentation).filter(models.Documentation.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} NOT FOUND")
    if not can_manage_documentation(post, curr_user, db):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
