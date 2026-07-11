from app.celery_app import celery_app
from app import models
from app.database import SessionLocal
from app.schemas import DocumentationResponse

import pandas as pd

@celery_app.task(name="ibd.export_assessment_question_table_csv")
def export_assessment_question_table_csv_celery(user_id: int):
    """Function exports assessment data as a CSV."""
    with SessionLocal() as db:
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
            .filter(models.AssessmentAnswer.user_id == user_id)
            .all()
        )

    result = [row._asdict() for row in data]
    df = pd.DataFrame(result)
    if not df.empty and {"total_correct", "total_questions"}.issubset(df.columns):
        df["percentage_correct"] = df.apply(
            lambda row: (row["total_correct"] / row["total_questions"] * 100)
            if row.get("total_questions") else None,
            axis=1,
        )

    file_name = "User_Assessment_Table.csv"
    return {
        "filename": file_name,
        "media_type": "text/csv",
        "content": df.to_csv(index=False),
    }


@celery_app.task(name="ibd.export_all_assessment_responses_csv")
def export_all_assessment_responses_csv_celery():
    """Export all quiz questions, attempts, answers, and user identifiers for admin analysis."""
    with SessionLocal() as db:
        data = (
            db.query(
                models.AssessmentQuestion.id.label("question_id"),
                models.AssessmentQuestion.documentation_id,
                models.Documentation.documentation_title,
                models.AssessmentQuestion.question,
                models.AssessmentQuestion.choices,
                models.AssessmentQuestion.correct_response,
                models.AssessmentQuestion.explanation,
                models.AssessmentAttempt.id.label("attempt_id"),
                models.AssessmentAttempt.user_id,
                models.User.email.label("user_email"),
                models.AssessmentAttempt.documentation_type,
                models.AssessmentAttempt.total_questions,
                models.AssessmentAttempt.total_correct,
                models.AssessmentAttempt.created_at.label("attempt_created_at"),
                models.AssessmentAnswer.id.label("answer_id"),
                models.AssessmentAnswer.user_response,
                models.AssessmentAnswer.is_correct,
            )
            .join(models.Documentation, models.Documentation.id == models.AssessmentQuestion.documentation_id)
            .outerjoin(models.AssessmentAnswer, models.AssessmentAnswer.question_id == models.AssessmentQuestion.id)
            .outerjoin(models.AssessmentAttempt, models.AssessmentAttempt.id == models.AssessmentAnswer.attempt_id)
            .outerjoin(models.User, models.User.id == models.AssessmentAnswer.user_id)
            .order_by(models.AssessmentQuestion.documentation_id.asc(), models.AssessmentQuestion.id.asc(), models.AssessmentAnswer.id.asc())
            .all()
        )

    result = [row._asdict() for row in data]
    df = pd.DataFrame(result)
    if not df.empty and {"total_correct", "total_questions"}.issubset(df.columns):
        df["percentage_correct"] = df.apply(
            lambda row: (row["total_correct"] / row["total_questions"] * 100)
            if row.get("total_questions") else None,
            axis=1,
        )

    file_name = "All_Assessment_Responses.csv"
    return {
        "filename": file_name,
        "media_type": "text/csv",
        "content": df.to_csv(index=False),
    }


@celery_app.task(name="ibd.export_documentation_table_csv")
def export_documentation_table_csv_celery():
    """Export every documentation row so future research can be done."""
    with SessionLocal() as db:
        data = db.query(models.Documentation).all()
        result = [DocumentationResponse.model_validate(doc).model_dump() for doc in data]

    df = pd.DataFrame(result)
    return {
        "filename": "Documentation_Table_Data.csv",
        "media_type": "text/csv",
        "content": df.to_csv(index=False),
    }


@celery_app.task(name="ibd.export_comparison_votes_csv")
def export_comparison_votes_csv_celery():
    """Export all Arena A/B comparison votes and aggregate document stats."""
    with SessionLocal() as db:
        rows = (
            db.query(
                models.Comparison.id.label("comparison_id"),
                models.Comparison.documentation_id,
                models.Documentation.documentation_title,
                models.Comparison.winner,
                models.Comparison.comments,
                models.Comparison.user_id,
                models.User.email.label("user_email"),
                models.Comparison.created_at,
                models.Documentation.comparison_count,
                models.Documentation.ibd_wins,
                models.Documentation.td_wins,
                models.Documentation.ibd_doc_elo_rating,
                models.Documentation.td_doc_elo_rating,
                models.Documentation.bt_ibd_rating,
                models.Documentation.bt_td_rating,
                models.Documentation.bt_ibd_win_prob,
            )
            .join(models.Documentation, models.Documentation.id == models.Comparison.documentation_id)
            .outerjoin(models.User, models.User.id == models.Comparison.user_id)
            .order_by(models.Comparison.created_at.desc(), models.Comparison.id.desc())
            .all()
        )
        result = [row._asdict() for row in rows]

    df = pd.DataFrame(result)
    return {
        "filename": "Arena_Comparison_Votes.csv",
        "media_type": "text/csv",
        "content": df.to_csv(index=False),
    }
