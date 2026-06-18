# Predictive Cardio-Pulmonary Health Intelligence Suite (v3.0.0)

An advanced multi-modal telehealth platform that combines digital signal processing (DSP), neural acoustic analysis, and biochemical text analytics to automate comprehensive Electronic Health Record (EHR) report generation.

---

## 🚀 Key Features

### Dual-Channel Acoustic Processing Engine

* Processes independent heart and lung stethoscope `.wav` recordings.
* Utilizes specialized frequency-band analysis powered by `librosa`.
* Supports simultaneous cardiac and pulmonary signal interpretation.

### Neural Mel-Spectrogram Visualization

* Converts raw audio signals into high-resolution frequency–decibel maps.
* Generates mel-spectrogram visualizations using `matplotlib` in a headless environment.

### Biochemical Data Analytics

* Extracts and interprets key laboratory biomarkers from patient records.
* Automatically assigns configurable clinical risk thresholds.

### Medical Report Generation Engine

* Produces structured diagnostic summaries in PDF format.
* Includes verification tokens, digital signatures, and comparative spectral visualizations.
* Designed to align with documentation practices outlined in ISO 13485:2016 quality management standards.

### Unified Local Hosting Environment

* Serves frontend assets through `FastAPI` on port `8000`.
* Eliminates browser CORS restrictions and local file access limitations (`file:///`).

---

## 🛠️ System Requirements

* Python 3.10 or later
* Windows operating system (recommended)

---

## 📦 Installation

### 1. Create a Virtual Environment

```bash
python -m venv env
```

### 2. Activate the Virtual Environment

```bash
.\env\Scripts\activate
```

### 3. Install Required Dependencies

```bash
pip install fastapi uvicorn librosa numpy matplotlib reportlab pypdf
```

---

## 📂 Project Structure

```text
├── app.py                  # FastAPI application and local asset server
├── pipeline.py             # Heart and lung acoustic DSP engine
├── blood_parser.py         # Laboratory biomarker parsing module
├── report_generator.py     # Multi-modal analysis and report synthesis
├── pdf_generator.py        # Clinical PDF report generation engine
├── index.html              # Glassmorphic telehealth dashboard interface
└── temp_patient_data/      # Temporary workspace for active processing
```

---

## 💻 Running the Application

### Clear Existing Python Processes (Optional)

```powershell
taskkill /f /im python.exe
```

### Start the FastAPI Server

```bash
python app.py
```

### Access the Dashboard

Open your browser and navigate to:

```text
http://127.0.0.1:8000/
```

---

## 📊 Analytical Pipeline

### A. Cardiac Telemetry (`process_stethoscope_audio`)

**Clinical Focus:** Detection of valvular turbulence patterns.

* **Analysis Range:** 200 Hz – 1200 Hz
* **Evaluation Metric:** Energy density ratio
* **Threshold:** Values greater than `2.2`

**Interpretation:** Elevated energy density ratios may indicate high-velocity flow turbulence consistent with a systolic murmur profile.

---

### B. Pulmonary Telemetry (`process_lung_audio`)

**Clinical Focus:** Detection of adventitious respiratory sounds.

* **Analysis Range:** 400 Hz – 4000 Hz
* **Evaluation Metric:** Spectral energy spikes
* **Threshold:** Values greater than `2.5`

**Interpretation:** Significant spectral spikes may indicate discontinuous inspiratory crackles (rales).

---

## ⚠️ Regulatory Disclaimer

This platform performs algorithmic analysis of electronic health record data and physiological signals for technical assessment and operational monitoring purposes.

Generated reports are intended to support clinical workflows and should not be considered definitive medical diagnoses. All findings must be reviewed and correlated with appropriate clinical evaluation, including physical examination and confirmatory diagnostic procedures such as echocardiography.

This software is not intended to replace professional medical judgment.

---
