from fastapi import APIRouter, HTTPException, Query

from database import get_scan_history, delete_scan, clear_scan_history


router = APIRouter(
    prefix="/history",
    tags=["Scan History"]
)


@router.get("/")
def history(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """
    Get scan history with pagination.
    """

    all_history = get_scan_history()

    total = len(all_history)

    history_data = all_history[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "count": len(history_data),
        "history": history_data
    }


@router.delete("/{scan_id}")
def delete_history(scan_id: int):
    """
    Delete one scan from history.
    """

    deleted = delete_scan(scan_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Scan history record not found."
        )

    return {
        "success": True,
        "message": "Scan history deleted successfully.",
        "scan_id": scan_id
    }


@router.delete("/")
def clear_history():
    """
    Delete all scan history.
    """

    deleted_count = clear_scan_history()

    return {
        "success": True,
        "message": "All scan history cleared successfully.",
        "deleted_count": deleted_count
    }