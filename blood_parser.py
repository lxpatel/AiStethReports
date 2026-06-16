import pypdf
import re

def extract_text_from_pdf(pdf_path):
    """
    Extracts raw text strings out of an uploaded digital PDF document.
    """
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
    print("🩸 Analyzing extracted text from blood report...")
    
    # Define a clean clinical reference dictionary for standard markers
    # Format: [Regex Pattern, Lower Limit, Upper Limit, Unit]
    biomarkers = {
        "Hemoglobin (Hb)": [r"(?:Hemoglobin|Hb)[\s\:]+(\d+\.?\d*)", 12.0, 17.5, "g/dL"],
        "White Blood Cells (WBC)": [r"(?:WBC|White Blood Cell)[\s\:]+(\d+\.?\d*)", 4000, 11000, "cells/mcL"],
        "Platelets": [r"(?:Platelets|PLT)[\s\:]+(\d+\.?\d*)", 150000, 450000, "cells/mcL"]
    }
    
    parsed_results = {}
    
    for marker, rules in biomarkers.items():
        pattern, low, high, unit = rules
        # Search the document text for our regex biomarkers
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
            
    # If no markers match, return a fallback status
    if not parsed_results:
        return {"status": "Parsed text successfully, but no matching target biomarkers were detected."}
        
    return parsed_results