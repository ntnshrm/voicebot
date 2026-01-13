from fastapi import APIRouter, UploadFile, File
import uuid
import os

router = APIRouter()
UPLOAD_DIR = "../data/reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_report(file: UploadFile = File(...)):
    report_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{report_id}_{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "report_id": report_id,
        "filename": file.filename
    }
