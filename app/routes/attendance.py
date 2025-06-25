from fastapi import APIRouter, HTTPException
from app.utils.database import get_db_connection

router = APIRouter()

@router.get("/attendance")
async def get_attendance(limit: int = 100):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT a.id, u.name, a.timestamp
                       FROM attendance a
                       JOIN users u ON a.user_id = u.id
                       ORDER BY a.timestamp DESC
                       LIMIT %s""",
                    (limit,)
                )
                records = [
                    {"id": id, "name": name, "timestamp": timestamp}
                    for id, name, timestamp in cur.fetchall()
                ]
                return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
