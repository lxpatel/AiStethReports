from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import uvicorn
import shutil
import os

# Import our modular analysis and document engines
from pipeline import process_stethoscope_audio
from blood_parser import analyze_blood_metrics
from report_generator import compile_patient_summary
from pdf_generator import generate_medical_pdf

app = FastAPI(title="AiStethReports API", version="3.0.0")

# Configure CORS Middleware rules to link seamlessly with your frontend index.html
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
    # 1. Validation Guards: Verify correct inbound file payload tracking
    if not audio_file.filename.endswith('.wav') or not blood_report.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file extensions provided.")
        
    audio_path = os.path.join(UPLOAD_DIR, audio_file.filename)
    blood_path = os.path.join(UPLOAD_DIR, blood_report.filename)
    
    # 2. Stage binary data chunks into local storage buffers
    with open(audio_path, "wb") as a_buf, open(blood_path, "wb") as b_buf:
        shutil.copyfileobj(audio_file.file, a_buf)
        shutil.copyfileobj(blood_report.file, b_buf)
        
    try:
        # 3. Process Acoustic Signal Analysis Layer
        audio_metrics = process_stethoscope_audio(audio_path)
        
        # 4. Process Biochemical Laboratory PDF Reading Layer
        blood_analysis = analyze_blood_metrics(blood_path)
        
        # 5. Synthesize Multimodal Intelligence Findings Text Block
        final_summary_report = compile_patient_summary(
            patient_history=patient_history,
            audio_metrics=audio_metrics,
            blood_results=blood_analysis
        )
        
        # 6. Generate the Standardized EHR Medical Record PDF Document
        pdf_filename = f"Report_{audio_file.filename.split('.')[0]}.pdf"
        pdf_output_path = os.path.join(UPLOAD_DIR, pdf_filename)
        
        generate_medical_pdf(
            patient_history=patient_history,
            audio_metrics=audio_metrics,
            blood_results=blood_analysis,
            filename=pdf_output_path
        )
        
        # Clean up transient audio/blood file assets post-compilation to keep directory clear
        os.remove(audio_path)
        os.remove(blood_path)
        
        # 7. Return payload tracking strings including the clean browser download link
        return {
            "status": "Success",
            "compiled_brief": final_summary_report,
            "pdf_report_url": f"http://127.0.0.1:8000/api/v2/download-report/{pdf_filename}",
            "raw_data_payloads": {
                "acoustic_metrics": audio_metrics,
                "biochemical_metrics": blood_analysis
            }
        }
        
    except Exception as e:
        # Emergency Cleanup Loop: Erase any stranded local files on pipeline exceptions
        for p in [audio_path, blood_path]:
            if os.path.exists(p): os.remove(p)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/download-report/{filename}")
def download_report(filename: str):
    """
    Serves the statically compiled clinical PDF document to the web client.
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/pdf')
    raise HTTPException(status_code=404, detail="Requested medical record file not found on staging buffer.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)