from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import os
import time
import traceback

# Import modular analysis blocks
from pipeline import process_stethoscope_audio, process_lung_audio
from blood_parser import analyze_blood_metrics
from vision_parser import analyze_medical_imaging
from report_generator import compile_patient_summary
from pdf_generator import generate_medical_pdf

app = FastAPI(title="AiStethReports Comprehensive Cardio-Pulmonary Suite", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_patient_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f: return f.read()
    raise HTTPException(status_code=404, detail="index.html missing.")

@app.post("/api/v2/generate-comprehensive-report")
async def generate_comprehensive_report(
    patient_history: str = Form(...),
    audio_file: UploadFile = File(...),
    lung_file: UploadFile = File(...),
    blood_report: UploadFile = File(...),
    imaging_file: UploadFile = File(None) # Optional parameter file support
):
    print("\n🚀 [INGESTION CALL]: Incoming complex multi-modal diagnostic stream...")
    run_id = int(time.time())
    audio_path = os.path.join(UPLOAD_DIR, f"heart_{run_id}.wav")
    lung_path = os.path.join(UPLOAD_DIR, f"lung_{run_id}.wav")
    blood_path = os.path.join(UPLOAD_DIR, f"panel_{run_id}.pdf")
    imaging_path = os.path.join(UPLOAD_DIR, f"scan_{run_id}.png") if imaging_file else None
    
    try:
        # Stage core assets
        with open(audio_path, "wb") as f: f.write(await audio_file.read())
        with open(lung_path, "wb") as f: f.write(await lung_file.read())
        with open(blood_path, "wb") as f: f.write(await blood_report.read())
        
        # Handle imaging file if provided
        imaging_analysis = None
        if imaging_file and imaging_file.filename:
            print(f"↳ Ingesting radiographic diagnostic asset: {imaging_file.filename}")
            # Ensure correct extension fallback mapping
            ext = os.path.splitext(imaging_file.filename)[1]
            imaging_path = os.path.join(UPLOAD_DIR, f"scan_{run_id}{ext}")
            with open(imaging_path, "wb") as f: f.write(await imaging_file.read())
            # Fire computer vision matrix diagnostic run
            imaging_analysis = analyze_medical_imaging(imaging_path)

        print("✅ Data staging complete. Launching integrated multi-modal loops...")
        heart_metrics = process_stethoscope_audio(audio_path)
        lung_metrics = process_lung_audio(lung_path)
        blood_analysis = analyze_blood_metrics(blood_path)
        
        combined_acoustic_metrics = {
            "heart_metrics": heart_metrics,
            "lung_metrics": lung_metrics
        }
        
        # Cross system synthesis block
        final_summary_report = compile_patient_summary(
            patient_history=patient_history,
            audio_metrics=combined_acoustic_metrics,
            blood_results=blood_analysis
        )
        
        # Extend brief summary text if visual insights exist
        if imaging_analysis:
            final_summary_report += f"\n\n=== AUTOMATED RADIOLOGICAL CONTEXT ===\n{imaging_analysis['radiology_classification']}\nNote: {imaging_analysis['clinical_note']}"

        pdf_filename = f"Comprehensive_EHR_Record_{run_id}.pdf"
        pdf_output_path = os.path.join(UPLOAD_DIR, pdf_filename)
        
        # Generate final certified medical record PDF file document
        generate_medical_pdf(
            patient_history=patient_history,
            audio_metrics=combined_acoustic_metrics,
            blood_results=blood_analysis,
            imaging_results=imaging_analysis, # Injected parameters matching PDF engine mapping
            filename=pdf_output_path
        )
        
        # Permanent cleanup execution loop
        for p in [audio_path, lung_path, blood_path, imaging_path]:
            if p and os.path.exists(p): os.remove(p)
            
        print("✨ Multi-modal master synthesis completed. Operational package dispatched.")
        return {
            "status": "Success",
            "compiled_brief": final_summary_report,
            "pdf_report_url": f"/api/v2/download-report/{pdf_filename}",
            "raw_data_payloads": {
                "acoustic_metrics": combined_acoustic_metrics,
                "biochemical_metrics": blood_analysis,
                "radiological_metrics": imaging_analysis
            }
        }
        
    except Exception as e:
        print("\n=== CRITICAL PIPELINE CRASH LOG ===")
        traceback.print_exc()
        print("===================================\n")
        for p in [audio_path, lung_path, blood_path, imaging_path]:
            if p and os.path.exists(p): os.remove(p)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/download-report/{filename}")
def download_report(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/pdf')
    raise HTTPException(status_code=404, detail="File not found on buffer.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)