from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import shutil
import os

from pipeline import process_stethoscope_audio
from blood_parser import analyze_blood_metrics
from report_generator import compile_patient_summary

app = FastAPI(title="AiStethReports API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_patient_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/v2/generate-comprehensive-report")
async def generate_comprehensive_report(
    patient_history: str = Form(...),
    audio_file: UploadFile = File(...),
    blood_report: UploadFile = File(...)
):
    if not audio_file.filename.endswith('.wav') or not blood_report.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file extensions provided.")
        
    audio_path = os.path.join(UPLOAD_DIR, audio_file.filename)
    blood_path = os.path.join(UPLOAD_DIR, blood_report.filename)
    
    with open(audio_path, "wb") as a_buf, open(blood_path, "wb") as b_buf:
        shutil.copyfileobj(audio_file.file, a_buf)
        shutil.copyfileobj(blood_report.file, b_buf)
        
    try:
        # Run our detailed analysis subsystems!
        audio_metrics = process_stethoscope_audio(audio_path)
        blood_analysis = analyze_blood_metrics(blood_path)
        
        final_summary_report = compile_patient_summary(
            patient_history=patient_history,
            audio_metrics=audio_metrics,
            blood_results=blood_analysis
        )
        
        os.remove(audio_path)
        os.remove(blood_path)
        
        return {"status": "Success", "compiled_brief": final_summary_report}
        
    except Exception as e:
        for p in [audio_path, blood_path]:
            if os.path.exists(p): os.remove(p)
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)