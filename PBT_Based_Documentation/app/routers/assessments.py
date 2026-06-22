import admin
from fastapi import APIRouter, Body, HTTPException, Depends, Query, status
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
import models
from database import get_db
from openai import OpenAI
import os, json
import legacy_backend
import random
import oath2
from collections import defaultdict
from fastapi import Response
from schemas import (
    AssessmentQuestionSubmit,
    AssessmentAnswerResponse,
    AssessmentAnswerAdminResponse,
    AssessmentDocumentationOption,
    AssessmentQuestionAdminResponse,
    AssessmentQuestionUpdate,
    AssessmentRetakeGrantRequest,
    AssessmentRetakeGrantResponse,
    AssessmentResponse,
    AssessmentStatsResponse,
    AssessmentSubmit,
    DocumentationResponse,
)
from fastapi.responses import FileResponse
import pandas as pd
router = APIRouter(prefix="/assessments", tags=["assessments"])
ASSESSMENT_MODEL = os.environ.get("OPENAI_ASSESSMENT_METRICS_MODEL", "gpt-5.5")


def generate_assessment_json(prompt: str, payload: dict) -> dict:
    """Generate assessment JSON with any configured model provider."""
    config = legacy_backend.model_provider_config(
        payload,
        fallback_model=ASSESSMENT_MODEL,
        model_field="metrics_model",
    )
    if config["provider"] == "openai" and not config["api_key"] and not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OpenAI key is required. Paste a key or set OPENAI_API_KEY.")

    if config["provider"] == "claude":
        raw = legacy_backend.anthropic_response_text(
            config["model"],
            prompt,
            config["api_key"],
        )
    else:
        client_kwargs = {}
        if config["api_key"]:
            client_kwargs["api_key"] = config["api_key"]
        if config["base_url"]:
            client_kwargs["base_url"] = config["base_url"]
        client = OpenAI(**client_kwargs)
        if not legacy_backend.prefers_chat_completions(config) and hasattr(client, "responses"):
            response = client.responses.create(
                model=config["model"],
                input=prompt,
            )
            raw = response.output_text
        else:
            response = client.chat.completions.create(
                model=config["model"],
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert software engineer and technical educator.",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            raw = response.choices[0].message.content or ""

    return json.loads(legacy_backend.strip_fences(raw))


def request_payload_from_provider_fields(
    body: dict | None,
    model_provider: str | None,
    model: str | None,
    api_key: str | None,
    base_url: str | None,
) -> dict:
    """Merge JSON body provider settings with query-param overrides."""
    payload = dict(body or {})
    if model_provider:
        payload["model_provider"] = model_provider
    if model:
        payload["metrics_model"] = model
    if api_key:
        payload["api_key"] = api_key
    if base_url:
        payload["base_url"] = base_url
    return payload



# CODEX VIBE CODED OPEN LOGIC ABOVE


# ADMIN SIDE ROUTES
@router.get("/documentation/{documentation_id}", response_model=list[AssessmentQuestionAdminResponse])
async def list_documentation_questions(
    documentation_id:int,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """List all comprehension questions attached to a documentation row."""
    doc = db.query(models.Documentation).filter(models.Documentation.id == documentation_id).first()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documentation not found")
    return (
        db.query(models.AssessmentQuestion)
        .filter(models.AssessmentQuestion.documentation_id == documentation_id)
        .order_by(models.AssessmentQuestion.id.asc())
        .all()
    )


@router.get("/documentation/{documentation_id}/answers", response_model=list[AssessmentAnswerAdminResponse])
async def list_documentation_answers(
    documentation_id:int,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """List all submitted answers for questions attached to a documentation row."""
    doc = db.query(models.Documentation).filter(models.Documentation.id == documentation_id).first()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documentation not found")
    rows = (
        db.query(models.AssessmentAnswer, models.AssessmentQuestion.documentation_id, models.User.email)
        .join(models.AssessmentQuestion, models.AssessmentAnswer.question_id == models.AssessmentQuestion.id)
        .outerjoin(models.User, models.AssessmentAnswer.user_id == models.User.id)
        .filter(models.AssessmentQuestion.documentation_id == documentation_id)
        .order_by(models.AssessmentAnswer.id.asc())
        .all()
    )
    return [
        {
            "id": answer.id,
            "attempt_id": answer.attempt_id,
            "question_id": answer.question_id,
            "documentation_id": doc_id,
            "user_id": answer.user_id,
            "user_email": user_email,
            "user_response": answer.user_response,
            "is_correct": answer.is_correct,
        }
        for answer, doc_id, user_email in rows
    ]


@router.put("/questions/{question_id}", response_model=AssessmentQuestionAdminResponse)
async def update_assessment_question(
    question_id:int,
    payload:AssessmentQuestionUpdate,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Edit one existing comprehension question."""
    question = db.query(models.AssessmentQuestion).filter(models.AssessmentQuestion.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if payload.correct_response not in payload.choices:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Correct response must match one of the choices")
    question.question = payload.question
    question.choices = payload.choices
    question.correct_response = payload.correct_response
    question.explanation = payload.explanation
    db.commit()
    db.refresh(question)
    return question


@router.delete("/questions/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assessment_question(
    question_id:int,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Delete one existing comprehension question."""
    question = db.query(models.AssessmentQuestion).filter(models.AssessmentQuestion.id == question_id).first()
    if question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    db.delete(question)
    db.commit()
    return None


@router.post("/documentation/{documentation_id}/retake-access", response_model=AssessmentRetakeGrantResponse)
async def grant_documentation_retake_access(
    documentation_id:int,
    payload:AssessmentRetakeGrantRequest,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Allow everyone, or one selected user, to take this documentation assessment again."""
    doc = db.query(models.Documentation).filter(models.Documentation.id == documentation_id).first()
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documentation not found")

    selected_user = None
    selected_email = (payload.user_email or "").strip().lower() or None
    if payload.scope == "user":
        if payload.user_id is not None:
            selected_user = db.query(models.User).filter(models.User.id == payload.user_id).first()
        elif selected_email:
            selected_user = db.query(models.User).filter(func.lower(models.User.email) == selected_email).first()
        if selected_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
        selected_email = (selected_user.email or selected_email or "").lower()

    creator = db.query(models.User).filter(models.User.email == curr_user.email).first()
    grant = models.AssessmentRetakeGrant(
        documentation_id=documentation_id,
        allow_all_users=payload.scope == "all",
        user_id=selected_user.id if selected_user else None,
        user_email=selected_email,
        created_by=creator.id if creator else None,
    )
    db.add(grant)
    db.commit()
    db.refresh(grant)
    return grant


@router.delete("/attempts")
async def reset_all_assessment_attempts(
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Delete every assessment attempt and submitted answer for all users."""
    deleted_answers = db.query(models.AssessmentAnswer).delete(synchronize_session=False)
    deleted_attempts = db.query(models.AssessmentAttempt).delete(synchronize_session=False)
    deleted_retake_grants = 0
    retake_grants_table_found = inspect(db.bind).has_table("assessment_retake_grants")
    if retake_grants_table_found:
        deleted_retake_grants = db.query(models.AssessmentRetakeGrant).delete(synchronize_session=False)
    db.commit()
    return {
        "deleted_answers": deleted_answers,
        "deleted_attempts": deleted_attempts,
        "deleted_retake_grants": deleted_retake_grants,
        "retake_grants_table_found": retake_grants_table_found,
    }


@router.post("/generate/{documentation_id}")
async def generate_questions(
    documentation_id:int,
    model: str | None = None,
    n_questions:int = 10,
    choice:int=4,
    model_provider: str | None = Query(None),
    api_key: str | None = Query(None),
    base_url: str | None = Query(None),
    provider_payload: dict | None = Body(None),
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Function (mostly for demo purposes) lets an AI model generate a couple of multiple choice questions where the can answer only using source code
    and provided documentation
    """

    random_documentation = db.query(models.Documentation).filter(models.Documentation.id == documentation_id).first()
    if random_documentation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Documentation not found"
        )

    PROMPT = f"""You are an expert software engineer and technical educator.

Your task is to create a standardized comprehension assessment for a software function.

Requirements:

* Generate exactly {n_questions} multiple-choice questions.
* Every question must have exactly {choice} answer choices.
* Exactly one answer choice must be correct.
* Correct answer letters should be reasonably diverse across the question set.
* Do NOT cluster most correct answers on the same letter. For example, avoid patterns like A, B, B, B, C, D unless the content genuinely requires it.
* Some overlap is acceptable, but distribute correct answers across A/B/C/D whenever possible.
* Questions should test function behavior, parameters, return values, assumptions, edge cases, exceptions, and common misunderstandings.
* Questions should NOT test variable names, coding style, line-by-line source code knowledge, or documentation wording.
* Avoid trick questions and duplicate concepts.
* Include a brief explanation for the correct answer.

MANDATORY COVERAGE REQUIREMENTS:

* At least 2 questions MUST focus on edge cases or boundary conditions.
* At least 2 questions MUST focus on exceptions, errors, invalid inputs, or situations that cause the function to fail.
* At least 1 question MUST focus on return values or output behavior.
* At least 1 question MUST focus on parameter behavior or parameter interactions.
* Remaining questions may cover general behavior, assumptions, or common misconceptions.

For exception-related questions:
* Ask what exception is raised, when an exception occurs, or what input/state causes failure.
* Use only exceptions that are actually possible according to the source code.

For edge-case questions:
* Focus on empty inputs, null values, boundary values, degenerate cases, special parameter combinations, or unusual but valid inputs when applicable.

Questions should collectively cover the function's most important behaviors rather than repeatedly testing the same concept.

Return ONLY valid JSON.

Schema:

{{
  "questions": [
    {{
      "question": "string",
      "choices": {{
        "A": "string",
        "B": "string",
        "C": "string",
        "D": "string"
      }},
      "correct_answer": "A",
      "explanation": "string"
    }}
  ]
}}

Function Name:
{random_documentation.documentation_title}

Source Code:
{random_documentation.source_code}
"""

    payload = request_payload_from_provider_fields(
        provider_payload,
        model_provider,
        model,
        api_key,
        base_url,
    )
    try:
        output = generate_assessment_json(PROMPT, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)) from exc

    # Update the database.
    # assessment_questions is where we store the documentation_id, question(s), and the correct response

    new_QA = None
    for q in output["questions"]:
        new_QA = models.AssessmentQuestion(
            documentation_id=documentation_id,
            question=q["question"],
            choices=q["choices"],
            correct_response=q["correct_answer"],
            explanation=q["explanation"]
        )

        db.add(new_QA)
    db.commit()
    if new_QA is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No questions were generated")
    db.refresh(new_QA)
    return new_QA

# Enable admin to submit questions etc
@router.post("/admin_submit", response_model=AssessmentQuestionAdminResponse)
async def question_submit(
    assessment:AssessmentQuestionSubmit,
    db:Session=Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Function allows admin users to submit questions etc """
    new_question = models.AssessmentQuestion(documentation_id=assessment.documentation_id,
                                             question = assessment.question,
                                             choices = assessment.choices,
                                             correct_response = assessment.correct_response,
                                             explanation = assessment.explanation)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

# Enable to alter the questions
@router.put("/submit/update", response_model=AssessmentQuestionAdminResponse)
async def question_update(
    assessment:AssessmentQuestionSubmit,
    db:Session = Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Function allows admin users to update their questions"""
    question = db.query(models.AssessmentQuestion).filter(models.AssessmentQuestion.id == assessment.id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUND!")
    # Updating...
    question.documentation_id = assessment.documentation_id
    question.question = assessment.question
    question.choices = assessment.choices
    question.correct_response = assessment.correct_response
    question.explanation = assessment.explanation


    db.commit()
    db.refresh(question)
    return question

# Allow admin to delete submitted responses
@router.delete("/submit/delete/{id}")
async def delete_responses(
    id:int,
    db:Session = Depends(get_db),
    curr_user:Session=Depends(admin.get_current_admin),
):
    """Function deletes a question"""
    question = db.query(models.AssessmentQuestion).filter(models.AssessmentQuestion.id == id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUND!")
    # Delete the question from the database
    db.delete(question)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)








    # USER SIDE ROUTES

# Get a random assessment
def latest_attempt_for_user(documentation_id:int, db:Session, curr_user:models.User):
    return (
        db.query(models.AssessmentAttempt)
        .filter(
            models.AssessmentAttempt.documentation_id == documentation_id,
            models.AssessmentAttempt.user_id == curr_user.id,
        )
        .order_by(models.AssessmentAttempt.created_at.desc(), models.AssessmentAttempt.id.desc())
        .first()
    )


def latest_retake_grant_for_user(documentation_id:int, db:Session, curr_user:models.User):
    return (
        db.query(models.AssessmentRetakeGrant)
        .filter(models.AssessmentRetakeGrant.documentation_id == documentation_id)
        .filter(
            (models.AssessmentRetakeGrant.allow_all_users == True)
            | (models.AssessmentRetakeGrant.user_id == curr_user.id)
            | (func.lower(models.AssessmentRetakeGrant.user_email) == (curr_user.email or "").lower())
        )
        .order_by(models.AssessmentRetakeGrant.created_at.desc(), models.AssessmentRetakeGrant.id.desc())
        .first()
    )


def user_can_start_documentation(documentation_id:int, db:Session, curr_user:models.User) -> bool:
    latest_attempt = latest_attempt_for_user(documentation_id, db, curr_user)
    if latest_attempt is None:
        return True
    latest_grant = latest_retake_grant_for_user(documentation_id, db, curr_user)
    return bool(latest_grant and latest_grant.created_at > latest_attempt.created_at)


@router.get("/documentation-options", response_model=list[AssessmentDocumentationOption])
async def list_assessment_documentation_options(db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """List documentation rows that have at least one assessment question."""
    rows = (
        db.query(
            models.Documentation.id,
            models.Documentation.documentation_title,
            func.count(models.AssessmentQuestion.id).label("question_count"),
        )
        .join(models.AssessmentQuestion, models.AssessmentQuestion.documentation_id == models.Documentation.id)
        .group_by(models.Documentation.id, models.Documentation.documentation_title)
        .order_by(models.Documentation.documentation_title.asc(), models.Documentation.id.asc())
        .all()
    )
    return [
        {
            "documentation_id": row.id,
            "documentation_title": row.documentation_title,
            "question_count": row.question_count,
            "attempted": not user_can_start_documentation(row.id, db, curr_user),
        }
        for row in rows
    ]


def build_assessment_for_documentation(documentation:models.Documentation, db:Session, curr_user:models.User):
    assessment = db.query(models.AssessmentQuestion).filter(
        models.AssessmentQuestion.documentation_id == documentation.id
    ).order_by(models.AssessmentQuestion.id.asc()).all()
    if not assessment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for this documentation")

    choices = ["TD", "IBD"]
    if random.choice(choices) == "TD":
        markdown = documentation.TD_md
        doc_type = "TD"
    else:
        markdown = documentation.IBD_generated_md
        doc_type = "IBD"

    new_attempt = models.AssessmentAttempt(documentation_id = documentation.id, user_id = curr_user.id,
                                           documentation_type = doc_type,
                                           total_questions = len(assessment),
                                           total_correct = 0)
    db.add(new_attempt)
    db.commit()
    db.refresh(new_attempt)

    return {
        "attempt_id": new_attempt.id,
        "documentation_id": documentation.id,
        "documentation_title": documentation.documentation_title,
        "documentation_type": doc_type,
        "documentation": markdown,
        "questions": [
            {
                "id": q.id,
                "question": q.question,
                "choices": q.choices
            }
            for q in assessment
        ]
    }


@router.get("/documentation/{documentation_id}/start", response_model=AssessmentResponse)
async def start_documentation_assessment(documentation_id:int, db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """Start an assessment for one selected documentation row."""
    documentation = db.query(models.Documentation).filter(models.Documentation.id == documentation_id).first()
    if not documentation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"NOT FOUND")
    if not user_can_start_documentation(documentation_id, db, curr_user):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This documentation was already completed. Ask an admin to allow a retake.")
    return build_assessment_for_documentation(documentation, db, curr_user)


@router.get("/random", response_model=AssessmentResponse)
async def get_random_assessment(db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """function gets random assessment and also ranodmly chooses to do TD or IBD """
    query = (
        db.query(models.Documentation)
        .join(models.AssessmentQuestion, models.AssessmentQuestion.documentation_id == models.Documentation.id)
        .group_by(models.Documentation.id)
    )
    candidates = query.all()
    available = [doc for doc in candidates if user_can_start_documentation(doc.id, db, curr_user)]
    documentation = random.choice(available) if available else None
    if not documentation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No remaining documentation assessments are available")

    return build_assessment_for_documentation(documentation, db, curr_user)


# Route allows user to submit their answer
@router.post("/submit", response_model=AssessmentAnswerResponse)
async def submit_answers(response:AssessmentSubmit, db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """Function allows user to submit response to the database"""
    attempting_question = db.query(models.AssessmentQuestion).filter(models.AssessmentQuestion.id == response.question_id).first()
    if not attempting_question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"QUESTION WAS NOT FOUND")


    attempt = (
        db.query(models.AssessmentAttempt)
        .filter(
            models.AssessmentAttempt.id == response.attempt_id,
            models.AssessmentAttempt.user_id == curr_user.id
        )
        .first()
    )

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt was not found"
        )

    existing_answer = (
    db.query(models.AssessmentAnswer)
    .filter(
        models.AssessmentAnswer.attempt_id == response.attempt_id,
        models.AssessmentAnswer.question_id == response.question_id,
        models.AssessmentAnswer.user_id == curr_user.id
    )
    .first()
    )

    if existing_answer:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You already answered this question for this attempt"
        )


    # If the user answers correct
    is_correct = attempting_question.correct_response == response.user_response


    user_response = models.AssessmentAnswer(attempt_id = response.attempt_id, question_id = response.question_id,
                                            user_response = response.user_response,
                                            is_correct = is_correct,
                                            user_id = curr_user.id)


    db.add(user_response)

    # update the questions/correct asnwers attempted
    if is_correct:
        attempt.total_correct += 1
    db.commit()
    db.refresh(user_response)
    return {
        "id": user_response.id,
        "attempt_id": user_response.attempt_id,
        "question_id": user_response.question_id,
        "user_response": user_response.user_response,
        "is_correct": user_response.is_correct,
        "correct_response": attempting_question.correct_response,
        "explanation": attempting_question.explanation,
    }



# Get assessment statistics
@router.get("/stats", response_model=AssessmentStatsResponse)
async def get_stats(db:Session = Depends(get_db), curr_user:Session = Depends(oath2.get_current_user)):
    """function gets the statistics of the current user """
    all_user_attempts = db.query(models.AssessmentAnswer).filter(models.AssessmentAnswer.user_id == curr_user.id).all()
    if not all_user_attempts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"USER WAS NOT FOUND")


    total_answered = len(all_user_attempts)
    total_correct = sum(answer.is_correct for answer in all_user_attempts)

    percentage_correct = (
        total_correct / total_answered * 100
        if total_answered > 0
        else 0
    )
    return  {
    "total_answered": total_answered,
    "total_correct": total_correct,
    "total_incorrect": total_answered-total_correct,
    "percentage_correct": percentage_correct
}

# Allow the user to download the data as a CSV file

# Download EVERYTHING


@router.get("/export")
async def export_assessment_question_table_csv(
    db: Session = Depends(get_db),
    curr_user = Depends(oath2.get_current_user)
):
    """Function exports assessment data as a CSV."""

    data = (
        db.query(
            models.AssessmentQuestion.id.label("question_id"),
            models.AssessmentQuestion.documentation_id,
            models.AssessmentQuestion.question,
            models.AssessmentQuestion.choices,
            models.AssessmentQuestion.correct_response,
            models.AssessmentQuestion.explanation,

            models.AssessmentAttempt.id.label("attempt_id"),
            models.AssessmentAttempt.user_id,
            models.AssessmentAttempt.documentation_type,
            models.AssessmentAttempt.total_questions,
            models.AssessmentAttempt.total_correct,
            models.AssessmentAttempt.created_at,

            models.AssessmentAnswer.id.label("answer_id"),
            models.AssessmentAnswer.user_response,
            models.AssessmentAnswer.is_correct,
        )
        .join(
            models.AssessmentAnswer,
            models.AssessmentAnswer.question_id == models.AssessmentQuestion.id
        )
        .join(
            models.AssessmentAttempt,
            models.AssessmentAttempt.id == models.AssessmentAnswer.attempt_id
        )
        .filter(models.AssessmentAnswer.user_id == curr_user.id)
        .all()
    )



    result = [row._asdict() for row in data]

    df = pd.DataFrame(result)
    df["percentage_correct"] = (
    df["total_correct"] / df["total_questions"] * 100
)

    file_name = "User_Assessment_Table.csv"
    df.to_csv(file_name, index=False)

    return FileResponse(
        path=file_name,
        filename=file_name,
        media_type="text/csv"
    )
