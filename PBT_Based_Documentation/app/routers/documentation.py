"""File handles the route logic for documentation. 
This includes getting all documentation, getting documentation only with user, 
getting only IBD documentation, and getting on TD documentation
"""

import json

from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
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


router = APIRouter(
    prefix="/documentation", tags=["documentation"]
)

api_router = APIRouter(prefix="/api", tags=["legacy documentation api"])


def legacy_error(exc: Exception) -> JSONResponse:
    """Keep old server.py-style validation errors as JSON 400s."""
    status_code = status.HTTP_400_BAD_REQUEST if isinstance(exc, ValueError) else status.HTTP_500_INTERNAL_SERVER_ERROR
    return JSONResponse(status_code=status_code, content={"error": str(exc)})


@api_router.post("/source")
async def lookup_source(payload: dict):
    """Drop-in FastAPI replacement for server.py's /api/source endpoint."""
    try:
        return legacy_backend.resolve_source(str(payload.get("object_name") or ""))
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/invariants")
async def generate_invariants(payload: dict):
    """Generate candidate invariants from pasted or looked-up source code."""
    try:
        return legacy_backend.generate_invariants(payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/documentation")
async def generate_documentation(payload: dict):
    """Generate invariant-based Markdown documentation."""
    try:
        return legacy_backend.generate_documentation(payload)
    except Exception as exc:
        return legacy_error(exc)


@api_router.post("/documentation-stream")
async def generate_documentation_stream(payload: dict):
    """Stream generated Markdown so the current frontend can render progressively."""
    try:
        stream = legacy_backend.stream_documentation(payload)
        return StreamingResponse(stream, media_type="text/plain; charset=utf-8")
    except Exception as exc:
        return legacy_error(exc)

@router.get("/", response_model=list[DocumentationResponse])
async def get_all_documentation(db:Session = Depends(get_db)):
    """Function gets every single documentation generated"""
    return db.query(models.Documentation).all()

# USER ENDPOINT LOGIC START-----
@router.get("/me", response_model=list[DocumentationResponse])
async def get_current_user_documentation(
    db:Session = Depends(get_db),
    curr_user:models.User = Depends(oath2.get_current_user)
):
    """Function gets all documentation owned by the current user"""
    all_docs = db.query(models.Documentation).filter(models.Documentation.owner_id == curr_user.id).all()
    return all_docs

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

    if doc.owner_id != curr_user.id:
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
    post_query.update(ibd_doc.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

# DELETE the documentation endpoint

@router.delete("/delete/{id}")
async def delete_docs(id:int, db:Session=Depends(get_db)):
    post_query = db.query(models.Documentation).filter(models.Documentation.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID: {id} NOT FOUND")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
