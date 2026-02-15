from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional, List


def create_audio(
    db: Session,
    image_id: int,
    url: str
) -> Optional[dict]:
    """Create a new audio record."""
    query = text("""
        INSERT INTO audio (image_id, url)
        VALUES (:image_id, :url)
        RETURNING id, image_id, url, created_at, updated_at
    """)
    
    try:
        result = db.execute(query, {
            "image_id": image_id,
            "url": url
        })
        db.commit()
        row = result.fetchone()
        
        if row:
            return {
                "id": row[0],
                "image_id": row[1],
                "url": row[2],
                "created_at": str(row[3]),
                "updated_at": str(row[4])
            }
        return None
    except Exception as e:
        db.rollback()
        raise e


def get_audio_by_id(db: Session, audio_id: int) -> Optional[dict]:
    """Get an audio record by ID."""
    query = text("""
        SELECT id, image_id, url, created_at, updated_at
        FROM audio
        WHERE id = :audio_id
    """)
    
    result = db.execute(query, {"audio_id": audio_id})
    row = result.fetchone()
    
    if row:
        return {
            "id": row[0],
            "image_id": row[1],
            "url": row[2],
            "created_at": str(row[3]),
            "updated_at": str(row[4])
        }
    return None


def get_audio_by_image_id(db: Session, image_id: int) -> Optional[dict]:
    """Get audio record for a specific image."""
    query = text("""
        SELECT id, image_id, url, created_at, updated_at
        FROM audio
        WHERE image_id = :image_id
        LIMIT 1
    """)
    
    result = db.execute(query, {"image_id": image_id})
    row = result.fetchone()
    
    if row:
        return {
            "id": row[0],
            "image_id": row[1],
            "url": row[2],
            "created_at": str(row[3]),
            "updated_at": str(row[4])
        }
    return None


def update_audio(
    db: Session,
    audio_id: int,
    url: Optional[str] = None
) -> Optional[dict]:
    """Update an audio record."""
    if url is None:
        # No updates to make, just return the existing audio
        return get_audio_by_id(db, audio_id)
    
    query = text("""
        UPDATE audio
        SET url = :url
        WHERE id = :audio_id
        RETURNING id, image_id, url, created_at, updated_at
    """)
    
    try:
        result = db.execute(query, {
            "audio_id": audio_id,
            "url": url
        })
        db.commit()
        row = result.fetchone()
        
        if row:
            return {
                "id": row[0],
                "image_id": row[1],
                "url": row[2],
                "created_at": str(row[3]),
                "updated_at": str(row[4])
            }
        return None
    except Exception as e:
        db.rollback()
        raise e


def delete_audio(db: Session, audio_id: int) -> bool:
    """Delete an audio record."""
    query = text("""
        DELETE FROM audio
        WHERE id = :audio_id
    """)
    
    try:
        result = db.execute(query, {"audio_id": audio_id})
        db.commit()
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        raise e


def delete_audio_by_image_id(db: Session, image_id: int) -> bool:
    """Delete audio record for a specific image."""
    query = text("""
        DELETE FROM audio
        WHERE image_id = :image_id
    """)
    
    try:
        result = db.execute(query, {"image_id": image_id})
        db.commit()
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        raise e

