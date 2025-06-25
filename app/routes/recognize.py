from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.database import get_db_connection
from app.utils.face_utils import base64_to_image
from app.config import FACE_RECOGNITION_THRESHOLD, ATTENDANCE_COOLDOWN_SECONDS
import json, base64, datetime
import numpy as np
import face_recognition
from PIL import Image

router = APIRouter()

@router.post("/recognize")
async def recognize_faces(image: UploadFile = File(...)):
    try:
        contents = await image.read()
        base64_img = base64.b64encode(contents).decode('utf-8')
        pil_image = base64_to_image(base64_img)
        rgb_image = np.array(pil_image.convert('RGB'))

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, encoding FROM users")
                known_faces = cur.fetchall()

        known_encodings = []
        known_metadata = []
        for user_id, name, encoding_str in known_faces:
            try:
                encoding = np.array(json.loads(encoding_str))
                known_encodings.append(encoding)
                known_metadata.append({"id": user_id, "name": name})
            except json.JSONDecodeError:
                continue

        face_encodings = face_recognition.face_encodings(rgb_image)
        recognized_names = []

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        known_encodings, face_encoding, tolerance=FACE_RECOGNITION_THRESHOLD
                    )

                    if True in matches:
                        match_idx = matches.index(True)
                        user_data = known_metadata[match_idx]
                        user_id = user_data["id"]
                        name = user_data["name"]

                        cur.execute("SELECT timestamp FROM attendance WHERE user_id = %s ORDER BY timestamp DESC LIMIT 1", (user_id,))
                        last_attendance = cur.fetchone()

                        if last_attendance:
                            last_time = last_attendance[0]
                            time_diff = (datetime.datetime.now() - last_time).total_seconds()
                            if time_diff < ATTENDANCE_COOLDOWN_SECONDS:
                                recognized_names.append(f"{name} (already logged)")
                                continue

                        cur.execute("INSERT INTO attendance (user_id) VALUES (%s)", (user_id,))
                        conn.commit()
                        recognized_names.append(name)
                    else:
                        recognized_names.append("Unknown")

        return {"recognized_names": recognized_names}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
