"""File handles the routes to compare the "area-like game" of comparing IBD to TD and assigning an ELO rating :D """
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func 
import models 
import database 
from database import get_db 
from schemas import ComparisonResponse, RandomComparisonResponse, ComparisonRequest
import choix,math
import oath2
import admin
from task_runner import export_csv
from tasks.export_tasks import export_comparison_votes_csv_celery


router = APIRouter(prefix="/comparison", tags=["comparison"])


def random_comparison_payload(random_api: models.Documentation):
    ibd_win_percentage = (
        int_or_default(random_api.ibd_wins, 0) / int_or_default(random_api.comparison_count, 0) * 100
        if int_or_default(random_api.comparison_count, 0) > 0
        else 0
    )
    td_win_percentage = (
        int_or_default(random_api.td_wins, 0) / int_or_default(random_api.comparison_count, 0) * 100
        if int_or_default(random_api.comparison_count, 0) > 0
        else 0
    )

    return {
        "documentation_id": random_api.id,
        "documentation_title": random_api.documentation_title,
        "td_doc": random_api.TD_md,
        "ibd_doc": random_api.IBD_generated_md,
        "ibd_doc_elo_rating": int_or_default(random_api.ibd_doc_elo_rating, 1000),
        "td_doc_elo_rating": int_or_default(random_api.td_doc_elo_rating, 1000),
        "bt_ibd_rating": float_or_none(random_api.bt_ibd_rating),
        "bt_td_rating": float_or_none(random_api.bt_td_rating),
        "bt_ibd_win_prob": float_or_none(random_api.bt_ibd_win_prob),
        "bt_ibd_win_prob_ci_lower": float_or_none(random_api.bt_ibd_win_prob_ci_lower),
        "bt_ibd_win_prob_ci_upper": float_or_none(random_api.bt_ibd_win_prob_ci_upper),
        "comparison_count": int_or_default(random_api.comparison_count, 0),
        "IBD_wins": int_or_default(random_api.ibd_wins, 0),
        "TD_wins": int_or_default(random_api.td_wins, 0),
        "IBD_win_percentage": ibd_win_percentage,
        "TD_win_percentage": td_win_percentage,
        "created_at": random_api.created_at,
    }


def comparison_candidate_query(db: Session):
    return (
        db.query(models.Documentation)
        .filter(models.Documentation.TD_md.isnot(None))
        .filter(func.length(func.trim(models.Documentation.TD_md)) > 0)
        .filter(models.Documentation.IBD_generated_md.isnot(None))
        .filter(func.length(func.trim(models.Documentation.IBD_generated_md)) > 0)
    )


def reset_document_comparison_stats(doc: models.Documentation):
    doc.comparison_count = 0
    doc.ibd_wins = 0
    doc.td_wins = 0
    doc.ibd_doc_elo_rating = 1000
    doc.td_doc_elo_rating = 1000
    doc.bt_ibd_rating = None
    doc.bt_td_rating = None
    doc.bt_ibd_win_prob = None
    doc.bt_ibd_win_prob_ci_lower = None
    doc.bt_ibd_win_prob_ci_upper = None


def recompute_document_comparison_stats(db: Session, doc_ids: list[int] | None = None) -> int:
    docs_query = db.query(models.Documentation)
    if doc_ids is not None:
        docs_query = docs_query.filter(models.Documentation.id.in_(doc_ids))
    updated_docs = 0
    for doc in docs_query.all():
        reset_document_comparison_stats(doc)
        comparison_rows = (
            db.query(models.Comparison)
            .filter(models.Comparison.documentation_id == doc.id)
            .order_by(models.Comparison.created_at.asc(), models.Comparison.id.asc())
            .all()
        )
        bt_rows = []
        for row in comparison_rows:
            td_wins = row.winner == "TD"
            doc.td_doc_elo_rating, doc.ibd_doc_elo_rating = calculate_elo(
                int_or_default(doc.td_doc_elo_rating, 1000),
                int_or_default(doc.ibd_doc_elo_rating, 1000),
                td_wins,
            )
            doc.comparison_count += 1
            if td_wins:
                doc.td_wins += 1
                bt_rows.append((0, 1))
            else:
                doc.ibd_wins += 1
                bt_rows.append((1, 0))
        if len(bt_rows) >= 2:
            bradley_terry_results = calculate_bradley_terry(bt_rows)
            if bradley_terry_results:
                doc.bt_td_rating = bradley_terry_results["bt_td_rating"]
                doc.bt_ibd_rating = bradley_terry_results["bt_ibd_rating"]
                doc.bt_ibd_win_prob = bradley_terry_results["bt_ibd_win_prob"]
        updated_docs += 1
    return updated_docs


# Randomly get an API's TD and IBD documentation
@router.get("/random", response_model=RandomComparisonResponse)
async def get_random_api(db:Session = Depends(get_db)):
    """Function gets gets a random row and returns the associated md for TD and IBD for the random API"""
    random_api = comparison_candidate_query(db).order_by(func.random()).first()

    if random_api is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No documentation found")

    return random_comparison_payload(random_api)


@router.get("/random-user", response_model=RandomComparisonResponse)
async def get_random_api_for_user(
    db: Session = Depends(get_db),
    curr_user: Session = Depends(oath2.get_current_user),
):
    """Get a random comparison this user has not already voted on."""
    voted_doc_ids = (
        db.query(models.Comparison.documentation_id)
        .filter(models.Comparison.user_id == curr_user.id)
        .subquery()
    )
    random_api = (
        comparison_candidate_query(db)
        .filter(~models.Documentation.id.in_(voted_doc_ids))
        .order_by(func.random())
        .first()
    )
    if random_api is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No remaining comparison documents are available")
    return random_comparison_payload(random_api)


# ELO RATING LOGIC-------
def calculate_elo(rating_a: float, rating_b: float, a_wins: bool, k: int = 32) -> tuple[int, int]:
    """Returns updated (rating_a, rating_b) after one match."""
    expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    expected_b = 1 - expected_a

    score_a = 1 if a_wins else 0
    score_b = 1 - score_a

    new_a = rating_a + k * (score_a - expected_a)
    new_b = rating_b + k * (score_b - expected_b)

    return round(new_a), round(new_b)


def int_or_default(value, default=0):
    try:
        if value is None:
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def float_or_none(value):
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None

# END OF ELO + Bradly Terry/luce style RATING LOGIC------

# BRADELY TERRY LOGIC 

def calculate_bradley_terry(comparisons):
    """
    comparisons format:

    (1, 0) -> IBD beats TD
    (0, 1) -> TD beats IBD

    item 0 = TD
    item 1 = IBD

    The Bradley–Terry probability is:

    Given the observed comparison data, what is the estimated probability that IBD beats TD in a future random comparison?
    """

    if not comparisons:
        return None

    try:
        # alpha adds smoothing so it does not explode when one side always wins :D
        beta_td, beta_ibd = choix.ilsr_pairwise(
            n_items=2,
            data=comparisons,
            alpha=0.01,
            max_iter=1000
        )
    except RuntimeError:
        return None

    # P(IBD > TD), the probability that IBD docs win TD
    p_ibd_wins = (
        math.exp(beta_ibd)
        /
        (math.exp(beta_ibd) + math.exp(beta_td))
    )

    return {
        "bt_td_rating": float(beta_td),
        "bt_ibd_rating": float(beta_ibd),
        "bt_ibd_win_prob": float(p_ibd_wins),
    }

# Allows the user to vote on which documentation they like
@router.post("/vote", response_model=ComparisonResponse)
async def vote_preference(
    vote: ComparisonRequest,
    db: Session = Depends(get_db),
    curr_user: Session = Depends(oath2.get_current_user)
):
    compared_doc = db.query(models.Documentation).filter(
        models.Documentation.id == vote.documentation_id
    ).first()

    if not compared_doc:
        raise HTTPException(status_code=404, detail="DOCUMENTATION NOT FOUND")

    if vote.winner not in ["TD", "IBD"]:
        raise HTTPException(status_code=400, detail="Winner must be TD or IBD")

    compared_doc.td_doc_elo_rating = int_or_default(compared_doc.td_doc_elo_rating, 1000)
    compared_doc.ibd_doc_elo_rating = int_or_default(compared_doc.ibd_doc_elo_rating, 1000)
    compared_doc.comparison_count = int_or_default(compared_doc.comparison_count, 0)
    compared_doc.td_wins = int_or_default(compared_doc.td_wins, 0)
    compared_doc.ibd_wins = int_or_default(compared_doc.ibd_wins, 0)

    # Elo
    td_wins = vote.winner == "TD"
    new_TD, new_IBD = calculate_elo(
        compared_doc.td_doc_elo_rating,
        compared_doc.ibd_doc_elo_rating,
        td_wins
    )

    # Add new comparison first
    new_comparison = models.Comparison(
        documentation_id=vote.documentation_id,
        winner=vote.winner,
        comments=vote.comments,
        user_id=curr_user.id,
    )

    db.add(new_comparison)

    # Update counts
    compared_doc.comparison_count += 1

    if vote.winner == "TD":
        compared_doc.td_wins += 1
    else:
        compared_doc.ibd_wins += 1

    # Update Elo
    compared_doc.td_doc_elo_rating = new_TD
    compared_doc.ibd_doc_elo_rating = new_IBD

    try:
        # Get previous comparisons and include the current in-memory vote. This
        # optional model update must never prevent the actual vote/counter write.
        comparison_rows = db.query(models.Comparison).filter(
            models.Comparison.documentation_id == vote.documentation_id
        ).all()

        collections = [
            (0, 1) if row.winner == "TD" else (1, 0)
            for row in comparison_rows
        ]
        collections.append((0, 1) if vote.winner == "TD" else (1, 0))

        if len(collections) >= 2:
            bradley_terry_results = calculate_bradley_terry(collections)
            if bradley_terry_results:
                compared_doc.bt_td_rating = bradley_terry_results["bt_td_rating"]
                compared_doc.bt_ibd_rating = bradley_terry_results["bt_ibd_rating"]
                compared_doc.bt_ibd_win_prob = bradley_terry_results["bt_ibd_win_prob"]
    except Exception:
        compared_doc.bt_td_rating = float_or_none(compared_doc.bt_td_rating)
        compared_doc.bt_ibd_rating = float_or_none(compared_doc.bt_ibd_rating)
        compared_doc.bt_ibd_win_prob = float_or_none(compared_doc.bt_ibd_win_prob)

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Could not save arena vote: {exc}") from exc

    db.refresh(new_comparison)
    db.refresh(compared_doc)

    return {
    "id": new_comparison.id,
    "documentation_id": new_comparison.documentation_id,
    "winner": new_comparison.winner,

    # Elo
    "ibd_doc_elo_rating": int_or_default(compared_doc.ibd_doc_elo_rating, 1000),
    "td_doc_elo_rating": int_or_default(compared_doc.td_doc_elo_rating, 1000),

    # Bradley-Terry
    "bt_ibd_rating": float_or_none(compared_doc.bt_ibd_rating),
    "bt_td_rating": float_or_none(compared_doc.bt_td_rating),
    "bt_ibd_win_prob": float_or_none(compared_doc.bt_ibd_win_prob),
    "bt_ibd_win_prob_ci_lower": float_or_none(compared_doc.bt_ibd_win_prob_ci_lower),
    "bt_ibd_win_prob_ci_upper": float_or_none(compared_doc.bt_ibd_win_prob_ci_upper),

    # Vote counts
    "comparison_count": int_or_default(compared_doc.comparison_count, 0),
    "IBD_wins": int_or_default(compared_doc.ibd_wins, 0),
    "TD_wins": int_or_default(compared_doc.td_wins, 0),

    # Convenience percentages
    "IBD_win_percentage": (
        int_or_default(compared_doc.ibd_wins, 0) / int_or_default(compared_doc.comparison_count, 0) * 100
        if int_or_default(compared_doc.comparison_count, 0) > 0
        else 0
    ),

    "TD_win_percentage": (
        int_or_default(compared_doc.td_wins, 0) / int_or_default(compared_doc.comparison_count, 0) * 100
        if int_or_default(compared_doc.comparison_count, 0) > 0
        else 0
    ),

    "comments": new_comparison.comments,
    "created_at": new_comparison.created_at,
    "user_id": new_comparison.user_id,
}


@router.delete("/attempts")
async def reset_all_comparison_attempts(
    scope: str = Query("all"),
    user_id: int | None = Query(None),
    user_email: str | None = Query(None),
    db: Session = Depends(get_db),
    curr_user: Session = Depends(admin.get_current_admin),
):
    """Delete Arena comparison votes for all users or one selected user and rebuild aggregate stats."""
    selected_user = None
    selected_scope = (scope or "all").strip().lower()
    if selected_scope not in {"all", "user"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="scope must be all or user")
    if selected_scope == "user":
        selected_email = (user_email or "").strip().lower()
        if user_id is not None:
            selected_user = db.query(models.User).filter(models.User.id == user_id).first()
        elif selected_email:
            selected_user = db.query(models.User).filter(func.lower(models.User.email) == selected_email).first()
        if selected_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")

    comparisons_query = db.query(models.Comparison)
    affected_doc_ids = None
    if selected_user is not None:
        comparisons_query = comparisons_query.filter(models.Comparison.user_id == selected_user.id)
        affected_doc_ids = [
            row[0]
            for row in comparisons_query.with_entities(models.Comparison.documentation_id).distinct().all()
        ]
    deleted_comparisons = comparisons_query.delete(synchronize_session=False)
    updated_docs = recompute_document_comparison_stats(db, affected_doc_ids)
    db.commit()
    return {
        "deleted_comparisons": deleted_comparisons,
        "updated_documents": updated_docs,
        "scope": selected_scope,
        "user_id": selected_user.id if selected_user else None,
        "user_email": selected_user.email if selected_user else None,
    }


# Export Arena comparison votes through the Celery/Redis queue (the frontend
# polls the returned task id), or inline as a direct CSV when the broker is down.
@router.get("/export")
async def export_comparison_votes_csv(
    curr_user: Session = Depends(admin.get_current_admin),
):
    """Export all Arena A/B comparison votes and aggregate document stats."""
    return await export_csv(export_comparison_votes_csv_celery)

# Get the leaderboard :D . Using elo as the main ranking metric with supporting evidence of bradley-terry etc
@router.get("/leaderboard")
async def get_leaderboard_ibd(db: Session = Depends(get_db)):
    """Function returns the IBD leaderboard ranked by IBD Elo rating"""

    all_docs = (
        db.query(models.Documentation)
        .filter(models.Documentation.IBD_generated_md.isnot(None))
        .filter(func.length(func.trim(models.Documentation.IBD_generated_md)) > 0)
        .order_by(
            models.Documentation.comparison_count.desc(),
            models.Documentation.ibd_doc_elo_rating.desc(),
            models.Documentation.created_at.desc(),
        )
        .all()
    )

    result = []

    for rank, doc in enumerate(all_docs, start=1):
        # Include recent qualitative feedback so the leaderboard can show why
        # participants preferred one side, not just the aggregate score.
        recent_comments = (
            db.query(models.Comparison)
            .filter(models.Comparison.documentation_id == doc.id)
            .filter(models.Comparison.comments.isnot(None))
            .filter(models.Comparison.comments != "")
            .order_by(models.Comparison.created_at.desc())
            .limit(8)
            .all()
        )

        result.append({
            "rank": rank,
            "documentation_id": doc.id,
            "documentation_title": doc.documentation_title,
            "source_code": doc.source_code,
            "IBD_generated_md": doc.IBD_generated_md,
            "TD_md": doc.TD_md,
            "invariants": doc.invariants,
            "hypothesis_tests": doc.hypothesis_tests,

            # Elo
            "ibd_doc_elo_rating": doc.ibd_doc_elo_rating,
            "td_doc_elo_rating": doc.td_doc_elo_rating,

            # Bradley-Terry
            "bt_ibd_rating": doc.bt_ibd_rating,
            "bt_td_rating": doc.bt_td_rating,
            "bt_ibd_win_prob": doc.bt_ibd_win_prob,
            "bt_ibd_win_prob_ci_lower": doc.bt_ibd_win_prob_ci_lower,
            "bt_ibd_win_prob_ci_upper": doc.bt_ibd_win_prob_ci_upper,

            # Vote counts
            "comparison_count": doc.comparison_count,
            "IBD_wins": doc.ibd_wins,
            "TD_wins": doc.td_wins,

            # Convenience percentages
            "IBD_win_percentage": (
                doc.ibd_wins / doc.comparison_count * 100
                if doc.comparison_count > 0
                else 0
            ),
            "TD_win_percentage": (
                doc.td_wins / doc.comparison_count * 100
                if doc.comparison_count > 0
                else 0
            ),

            "created_at": doc.created_at,
            "owner_id": doc.owner_id,
            "comments": [
                {
                    "winner": comment.winner,
                    "comment": comment.comments,
                    "created_at": comment.created_at,
                    "user_id": comment.user_id,
                }
                for comment in recent_comments
            ],
        })

    return result



# Finally route to get specific stats of a post :D 
@router.get("/{documentation_id}/stats")
async def get_comparison_stats(
    documentation_id: int,
    db: Session = Depends(get_db)
):
    """Function gets comparison stats for one documentation row"""

    doc = db.query(models.Documentation).filter(
        models.Documentation.id == documentation_id
    ).first()

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="DOCUMENTATION NOT FOUND"
        )

    ibd_win_percentage = (
        doc.ibd_wins / doc.comparison_count * 100
        if doc.comparison_count > 0
        else 0
    )

    td_win_percentage = (
        doc.td_wins / doc.comparison_count * 100
        if doc.comparison_count > 0
        else 0
    )

    return {
        "documentation_id": doc.id,
        "documentation_title": doc.documentation_title,

        "comparison_count": doc.comparison_count,
        "IBD_wins": doc.ibd_wins,
        "TD_wins": doc.td_wins,

        "IBD_win_percentage": ibd_win_percentage,
        "TD_win_percentage": td_win_percentage,

        "ibd_doc_elo_rating": doc.ibd_doc_elo_rating,
        "td_doc_elo_rating": doc.td_doc_elo_rating,

        "bt_ibd_rating": doc.bt_ibd_rating,
        "bt_td_rating": doc.bt_td_rating,
        "bt_ibd_win_prob": doc.bt_ibd_win_prob,

        "created_at": doc.created_at,
        "owner_id": doc.owner_id,
    }
