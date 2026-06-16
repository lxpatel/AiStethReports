from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import uvicorn
import shutil
import os

# Import our custom feature processing modules
from pipeline import process_stethoscope_audio
from blood_parser import analyze_blood_metrics
from report_generator import compile_patient_summary

app = FastAPI(
    title="AiStethReports API", 
    description="Integrated Multi-Modal Remote Telehealth Core",
    version="2.0.0"
)

UPLOAD_DIR = "temp_patient_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "online", "system": "Multi-Modal Health Integration Core Ready"}

@app.post("/api/v2/generate-comprehensive-report")
async def generate_comprehensive_report(
    patient_history: str = Form(...),
    audio_file: UploadFile = File(...),
    blood_report: UploadFile = File(...)
):
    # 1. Validation Checks
    if not audio_file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Invalid audio format. Must be a .wav file.")
    if not blood_report.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid report format. Must be a .pdf file.")
        
    # 2. Save incoming payloads locally
    audio_path = os.path.join(UPLOAD_DIR, audio_file.filename)
    blood_path = os.path.join(UPLOAD_DIR, blood_report.filename)
    
    with open(audio_path, "wb") as a_buf, open(blood_path, "wb") as b_buf:
        shutil.copyfileobj(audio_file.file, a_buf)
        shutil.copyfileobj(blood_report.file, b_buf)
        
    try:
        # 3. Execute acoustic feature extraction pipeline
        _, raw_mfccs, sample_rate = process_stethoscope_audio(audio_path)
        audio_metrics = {
            "sampling_rate_hz": sample_rate,
            "total_samples_extracted": float(raw_mfccs.size),
            "feature_dimensions": list(raw_mfccs.shape)
        }
        
        # 4. Execute biochemical data parsing engine
        blood_analysis = analyze_blood_metrics(blood_path)
        
        # 5. Synthesize all telemetry layers into a structured clinical summary text block
        final_summary_report = compile_patient_summary(
            patient_history=patient_history,
            audio_metrics=audio_metrics,
            blood_results=blood_analysis
        )
        
        # Clean up files post-processing
        os.remove(audio_path)
        os.remove(blood_path)
        
        return {
            "status": "Success",
            "compiled_brief": final_summary_report,
            "raw_data_payloads": {
                "acoustic_metrics": audio_metrics,
                "biochemical_metrics": blood_analysis
            }
        }
        
    except Exception as e:
        # Emergency file cleanup on error loops
        for p in [audio_path, blood_path]:
            if os.path.exists(p):
                os.remove(p)
        raise HTTPException(status_code=500, detail=f"Comprehensive processing error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)