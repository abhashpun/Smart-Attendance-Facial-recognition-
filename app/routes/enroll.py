from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.utils.database import get_db_connection
from app.config import FACE_RECOGNITION_THRESHOLD
import face_recognition, json, io
from PIL import Image
import numpy as np

router = APIRouter()

@router.post("/enroll")
async def enroll_user(name: str = Form(...), image: UploadFile = File(...)):
    try:
        contents = await image.read()
        pil_image = Image.open(io.BytesIO(contents))
        rgb_image = np.array(pil_image.convert('RGB'))

        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

        if not face_encodings:
            raise HTTPException(status_code=400, detail="No face found in image")
        if len(face_encodings) > 1:
            raise HTTPException(status_code=400, detail="Multiple faces found in image")

        encoding_str = json.dumps(face_encodings[0].tolist())

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO users (name, encoding) VALUES (%s, %s) RETURNING id", (name, encoding_str))
                user_id = cur.fetchone()[0]
                conn.commit()

        return {"id": user_id, "name": name, "status": "success"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
