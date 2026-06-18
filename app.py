from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn
import os
import time
import traceback

# Import our modular analysis and document engines
from pipeline import process_stethoscope_audio, process_lung_audio
from blood_parser import analyze_blood_metrics
from report_generator import compile_patient_summary
from pdf_generator import generate_medical_pdf

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

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    html_path = "index.html"
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f: return f.read()
    raise HTTPException(status_code=404, detail="index.html dashboard template missing.")

@app.post("/api/v2/generate-comprehensive-report")
async def generate_comprehensive_report(
    patient_history: str = Form(...),
    audio_file: UploadFile = File(...),
    lung_file: UploadFile = File(...),
    blood_report: UploadFile = File(...)
):
    print("\n🚀 [INGESTION CALL]: Inbound multi-modal vectors received...")
    run_id = int(time.time())
    audio_path = os.path.join(UPLOAD_DIR, f"heart_{run_id}.wav")
    lung_path = os.path.join(UPLOAD_DIR, f"lung_{run_id}.wav")
    blood_path = os.path.join(UPLOAD_DIR, f"panel_{run_id}.pdf")
    
    try:
        # Write files natively via byte streaming arrays
        with open(audio_path, "wb") as f: f.write(await audio_file.read())
        with open(lung_path, "wb") as f: f.write(await lung_file.read())
        with open(blood_path, "wb") as f: f.write(await blood_report.read())
            
        print("✅ Data staging complete. Running concurrent cardio-pulmonary diagnostics...")

        # Run individual analytics
        heart_metrics = process_stethoscope_audio(audio_path)
        lung_metrics = process_lung_audio(lung_path)
        blood_analysis = analyze_blood_metrics(blood_path)
        
        # Package full acoustics parameters bundle
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
        
        pdf_filename = f"Report_Cardio_Pulmonary_Suite_{run_id}.pdf"
        pdf_output_path = os.path.join(UPLOAD_DIR, pdf_filename)
        
        generate_medical_pdf(
            patient_history=patient_history,
            audio_metrics=combined_acoustic_metrics,
            blood_results=blood_analysis,
            filename=pdf_output_path
        )
        
        # Transient storage cleanup sweep
        for p in [audio_path, lung_path, blood_path]:
            if os.path.exists(p): os.remove(p)
            
        # Clean up transient sub-spectrogram files safely
        for img in [heart_metrics["spectrogram_img_path"], lung_metrics["spectrogram_img_path"]]:
            if os.path.exists(img): os.remove(img)

        print("✨ Multi-modal synthesis completed successfully.")
        return {
            "status": "Success",
            "compiled_brief": final_summary_report,
            "pdf_report_url": f"/api/v2/download-report/{pdf_filename}",
            "raw_data_payloads": {
                "acoustic_metrics": combined_acoustic_metrics,
                "biochemical_metrics": blood_analysis
            }
        }
        
    except Exception as e:
        print("\n=== CRITICAL PIPELINE CRASH LOG ===")
        traceback.print_exc()
        print("===================================\n")
        for p in [audio_path, lung_path, blood_path]:
            if os.path.exists(p): os.remove(p)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v2/download-report/{filename}")
def download_report(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/pdf')
    raise HTTPException(status_code=404, detail="File not found.")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=False)