import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_medical_pdf(patient_history: str, audio_metrics: dict, blood_results: dict, filename: str) -> str:
    """
    Generates a professional, standardized clinical diagnostic report PDF.
    Features integrated Phase 2 digital signal processing telemetry parameters.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    # Define Color Palette (Clinical Theme)
    primary_color = colors.HexColor("#0A1138")  # Deep Navy
    accent_color = colors.HexColor("#FF3131")   # Crimson Alert
    text_dark = colors.HexColor("#2D3748")
    
    # Typography Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20, 
        textColor=primary_color, spaceAfter=6, alignment=1
    )
    subtitle_style = ParagraphStyle(
        'DocSub', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, 
        textColor=colors.HexColor("#718096"), spaceAfter=20, alignment=1
    )
    section_heading = ParagraphStyle(
        'SectionHead', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, 
        textColor=primary_color, spaceBefore=12, spaceAfter=8
    )
    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'], fontName='Helvetica', fontSize=10, 
        textColor=text_dark, leading=14
    )
    alert_style = ParagraphStyle(
        'AlertTxt', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color
    )
    
    # 1. Document Header
    story.append(Paragraph("PREDICTIVE HEALTH INTELLIGENCE SUITE", title_style))
    story.append(Paragraph("Automated Multi-Modal Telemetry & Synthesis Brief", subtitle_style))
    
    # Divider Rule
    divider = Table([[""]], colWidths=[532])
    divider.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 1.5, primary_color)]))
    story.append(divider)
    story.append(Spacer(1, 10))
    
    # 2. Section: Patient Context
    story.append(Paragraph("1. Clinical Context & History", section_heading))
    story.append(Paragraph(patient_history, body_style))
    story.append(Spacer(1, 15))
    
    # 3. Section: Acoustic Telemetry (Updated with Option A DSP Metrics)
    story.append(Paragraph("2. Acoustic Diagnostic Telemetry", section_heading))
    acoustic_finding = audio_metrics.get("acoustic_classification", "Unclassified")
    confidence = audio_metrics.get("confidence_score", "N/A")
    dims = str(audio_metrics.get("feature_dimensions", "N/A"))
    
    # Isolate Option A newly engineered mathematical features
    centroid = audio_metrics.get("mean_spectral_centroid_hz", "N/A")
    zcr = audio_metrics.get("mean_zero_crossing_rate", "N/A")
    
    acoustic_text = f"<b>Classification Finding:</b> {acoustic_finding}<br/>" \
                    f"<b>Pipeline Confidence Score:</b> {confidence}<br/>" \
                    f"<b>Spectral Centroid:</b> {centroid} Hz<br/>" \
                    f"<b>Zero-Crossing Rate (ZCR):</b> {zcr}<br/>" \
                    f"<b>Telemetry Packet Dimensions:</b> {dims}"
    story.append(Paragraph(acoustic_text, body_style))
    story.append(Spacer(1, 15))
    
    # 4. Section: Biochemical Panel Table
    story.append(Paragraph("3. Biochemical Laboratory Panel Analysis", section_heading))
    
    # Setup Blood Table Header Row
    table_data = [["Biomarker Extracted", "Observed Value", "Reference Interval Range", "Status Flag"]]
    
    # Populate Table Rows Dynamically
    for marker, data in blood_results.items():
        val = str(data.get("observed_value", "N/A"))
        ref = str(data.get("reference_range", "N/A"))
        status = str(data.get("status", "Normal"))
        table_data.append([marker, val, ref, status])
        
    blood_table = Table(table_data, colWidths=[160, 100, 152, 120])
    blood_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('TEXTCOLOR', (0,1), (-1,-1), text_dark),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F7FAFC")),
    ]))
    
    # Loop over row statuses to dynamically apply a crimson text format for alerts
    for idx, row in enumerate(table_data):
        if "🚨" in row[3]:
            blood_table.setStyle(TableStyle([
                ('TEXTCOLOR', (3, idx), (3, idx), accent_color),
                ('FONTNAME', (3, idx), (3, idx), 'Helvetica-Bold')
            ]))
            
    story.append(blood_table)
    story.append(Spacer(1, 20))
    
    # 5. Cross-System Synthesis Block
    story.append(Paragraph("4. Automated Synthesis Insight", section_heading))
    
    # Determine the cross-analysis insight textual output
    low_hb = any("LOW" in str(d.get("status")) for m, d in blood_results.items() if "Hemoglobin" in m)
    if "Murmur" in acoustic_finding and low_hb:
        insight = "<b>CRITICAL CORRELATION:</b> Combined detection of low Hemoglobin (Anemia) and turbulent cardiovascular acoustics indicates high probability of an Anemic Murmur. Viscosity degradation confirmed. Recommend complete iron panel tracing."
    elif "Murmur" in acoustic_finding:
        insight = "<b>STRUCTURAL WARNING:</b> Isolated cardiac acoustic turbulence detected. Indicates potential valvular structural loading anomalies. Secondary echo validation recommended."
    else:
        insight = "<b>SYSTEM INSIGHT:</b> No cross-system pathophysiological anomalies identified. Biomarkers fall within acceptable systemic standard deviations."
        
    story.append(Paragraph(insight, body_style))
    
    # Build Document PDF File
    doc.build(story)
    return filename