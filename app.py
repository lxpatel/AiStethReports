from fastapi import FastAPI, UploadFile, File, HTTPException
import uvicorn
import shutil
import os
# Import our working audio engine from pipeline.py
from pipeline import process_stethoscope_audio

app = FastAPI(
    title="AiStethReports API", 
    description="Secure Digital Stethoscope Acoustic Processing Core",
    version="1.0.0"
)

# Temporary directory to stage uploaded medical files safely
UPLOAD_DIR = "temp_patient_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"status": "online", "system": "Naval Medical Support AI Core"}

@app.post("/api/v1/analyze-audio")
async def upload_and_analyze_audio(file: UploadFile = File(...)):
    # 1. Verification Guard: Check if the uploaded file is a valid WAV payload
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Invalid format. Only .wav digital stethoscope data accepted.")
    
    # 2. Securely stage the binary file payload on the local environment
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 3. Pass the data through our pipeline.py signal-processing layer
        clean_waves, raw_mfccs, sample_rate = process_stethoscope_audio(file_path)
        
        # Calculate some basic clinical metrics to return as structured JSON metadata
        signal_energy = float(clean_waves.size)
        feature_matrix_shape = list(raw_mfccs.shape)
        
        # Clean up the staged file after extraction to remain secure
        os.remove(file_path)
        
        return {
            "status": "Success",
            "filename": file.filename,
            "metrics": {
                "sampling_rate_hz": sample_rate,
                "total_samples_extracted": signal_energy,
                "feature_dimensions": feature_matrix_shape
            },
            "analysis": "Acoustic fingerprints successfully isolated. Ready for clinical synthesis layer."
        }
        
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Pipeline processing error: {str(e)}")

if __name__ == "__main__":
    # Spin up the Uvicorn deployment engine locally on port 8000
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)