from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import Optional, List


def create_image(
    db: Session,
    album_id: int,
    image_url: str,
    user_id: int,
    caption: Optional[str] = None,
    location: Optional[str] = None
) -> Optional[dict]:
    """Create a new image."""
    query = text("""
        INSERT INTO images (album_id, caption, image_url, location, user_id)
        VALUES (:album_id, :caption, :image_url, :location, :user_id)
        RETURNING id, album_id, caption, image_url, location, date_added, user_id, created_at, updated_at
    """)
    
    try:
        result = db.execute(query, {
            "album_id": album_id,
            "caption": caption,
            "image_url": image_url,
            "location": location,
            "user_id": user_id
        })
        db.commit()
        row = result.fetchone()
        
        if row:
            return {
                "id": row[0],
                "album_id": row[1],
                "caption": row[2],
                "image_url": row[3],
                "location": row[4],
                "date_added": str(row[5]),
                "user_id": row[6],
                "created_at": str(row[7]),
                "updated_at": str(row[8])
            }
        return None
    except Exception as e:
        db.rollback()
        raise e


def get_image_by_id(db: Session, image_id: int) -> Optional[dict]:
    """Get an image by ID."""
    query = text("""
        SELECT id, album_id, caption, image_url, location, date_added, user_id, created_at, updated_at
        FROM images
        WHERE id = :image_id
    """)
    
    result = db.execute(query, {"image_id": image_id})
    row = result.fetchone()
    
    if row:
        return {
            "id": row[0],
            "album_id": row[1],
            "caption": row[2],
            "image_url": row[3],
            "location": row[4],
            "date_added": str(row[5]),
            "user_id": row[6],
            "created_at": str(row[7]),
            "updated_at": str(row[8])
        }
    return None


def update_image(
    db: Session,
    image_id: int,
    caption: Optional[str] = None,
    image_url: Optional[str] = None,
    location: Optional[str] = None
) -> Optional[dict]:
    """Update an image."""
    # Build dynamic update query
    updates = []
    params = {"image_id": image_id}
    
    if caption is not None:
        updates.append("caption = :caption")
        params["caption"] = caption
    
    if image_url is not None:
        updates.append("image_url = :image_url")
        params["image_url"] = image_url
    
    if location is not None:
        updates.append("location = :location")
        params["location"] = location
    
    if not updates:
        # No updates to make, just return the existing image
        return get_image_by_id(db, image_id)
    
    query = text(f"""
        UPDATE images
        SET {', '.join(updates)}
        WHERE id = :image_id
        RETURNING id, album_id, caption, image_url, location, date_added, user_id, created_at, updated_at
    """)
    
    try:
        result = db.execute(query, params)
        db.commit()
        row = result.fetchone()
        
        if row:
            return {
                "id": row[0],
                "album_id": row[1],
                "caption": row[2],
                "image_url": row[3],
                "location": row[4],
                "date_added": str(row[5]),
                "user_id": row[6],
                "created_at": str(row[7]),
                "updated_at": str(row[8])
            }
        return None
    except Exception as e:
        db.rollback()
        raise e


def delete_image(db: Session, image_id: int) -> bool:
    """Delete an image."""
    query = text("""
        DELETE FROM images
        WHERE id = :image_id
    """)
    
    try:
        result = db.execute(query, {"image_id": image_id})
        db.commit()
        return result.rowcount > 0
    except Exception as e:
        db.rollback()
        raise e


def get_album_images(db: Session, album_id: int) -> List[dict]:
    """Get all images in an album."""
    query = text("""
        SELECT id, album_id, caption, image_url, location, date_added, user_id, created_at, updated_at
        FROM images
        WHERE album_id = :album_id
        ORDER BY date_added DESC
    """)
    
    result = db.execute(query, {"album_id": album_id})
    images = []
    
    for row in result:
        images.append({
            "id": row[0],
            "album_id": row[1],
            "caption": row[2],
            "image_url": row[3],
            "location": row[4],
            "date_added": str(row[5]),
            "user_id": row[6],
            "created_at": str(row[7]),
            "updated_at": str(row[8])
        })
    
    return images

