import pypdf
import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as f:
        reader = pypdf.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def analyze_blood_metrics(pdf_path):
    raw_text = extract_text_from_pdf(pdf_path)
    
    # Comprehensive Clinical Reference Dictionary
    biomarkers = {
        "Hemoglobin (Hb)": [r"(?:Hemoglobin|Hb)[\s\:]+(\d+\.?\d*)", 12.0, 17.5, "g/dL"],
        "White Blood Cells (WBC)": [r"(?:WBC|White Blood Cell|Leukocytes)[\s\:]+(\d+\.?\d*)", 4000, 11000, "cells/mcL"],
        "Platelets (PLT)": [r"(?:Platelets|PLT)[\s\:]+(\d+\.?\d*)", 150000, 450000, "cells/mcL"],
        "Red Blood Cells (RBC)": [r"(?:RBC|Red Blood Cell)[\s\:]+(\d+\.?\d*)", 4.3, 5.9, "million/mcL"],
        "Fasting Blood Sugar": [r"(?:Glucose|Fasting Blood Sugar|FBS)[\s\:]+(\d+\.?\d*)", 70, 100, "mg/dL"],
        "Total Cholesterol": [r"(?:Cholesterol|Total Cholesterol)[\s\:]+(\d+\.?\d*)", 100, 200, "mg/dL"]
    }
    
    parsed_results = {}
    
    for marker, rules in biomarkers.items():
        pattern, low, high, unit = rules
        match = re.search(pattern, raw_text, re.IGNORECASE)
        
        if match:
            value = float(match.group(1))
            status = "Normal"
            if value < low:
                status = "🚨 LOW (Anomalous)"
            elif value > high:
                status = "🚨 HIGH (Anomalous)"
                
            parsed_results[marker] = {
                "observed_value": value,
                "reference_range": f"{low} - {high} {unit}",
                "status": status
            }
        else:
            # If a marker isn't found in the PDF, list it as normal/unspecified for fallback safety
            parsed_results[marker] = {
                "observed_value": "Not Detected",
                "reference_range": f"{low} - {high} {unit}",
                "status": "Clear / No Alert"
            }
            
    return parsed_results