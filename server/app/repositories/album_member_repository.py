from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional, List


def add_album_member(db: Session, album_id: int, user_id: int) -> Optional[dict]:
    """Add a user as a member of an album."""
    query = text("""
        INSERT INTO album_members (album_id, user_id)
        VALUES (:album_id, :user_id)
        ON CONFLICT (album_id, user_id) DO NOTHING
        RETURNING id, album_id, user_id, created_at
    """)
    
    try:
        result = db.execute(query, {
            "album_id": album_id,
            "user_id": user_id
        })
        db.commit()
        row = result.fetchone()
        
        if row:
            return {
                "id": row[0],
                "album_id": row[1],
                "user_id": row[2],
                "created_at": str(row[3])
            }
        return None
    except Exception as e:
        db.rollback()
        raise e


def remove_album_member(db: Session, album_id: int, user_id: int) -> bool:
    """Remove a user from an album."""
    query = text("""
        DELETE FROM album_members
        WHERE album_id = :album_id AND user_id = :user_id
    """)
    
    try:
        result = db.execute(query, {
            "album_id": album_id,
            "user_id": user_id
        })
        db.commit()
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        raise e


def get_album_members(db: Session, album_id: int) -> List[dict]:
    """Get all members of an album."""
    query = text("""
        SELECT id, album_id, user_id, created_at
        FROM album_members
        WHERE album_id = :album_id
        ORDER BY created_at ASC
    """)
    
    result = db.execute(query, {"album_id": album_id})
    members = []
    
    for row in result:
        members.append({
            "id": row[0],
            "album_id": row[1],
            "user_id": row[2],
            "created_at": str(row[3])
        })
    
    return members


def is_album_member(db: Session, album_id: int, user_id: int) -> bool:
    """Check if a user is a member of an album."""
    query = text("""
        SELECT 1
        FROM album_members
        WHERE album_id = :album_id AND user_id = :user_id
        LIMIT 1
    """)
    
    result = db.execute(query, {
        "album_id": album_id,
        "user_id": user_id
    })
    return result.fetchone() is not None

