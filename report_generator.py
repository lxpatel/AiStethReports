def compile_patient_summary(patient_history: str, audio_metrics: dict, blood_results: dict) -> str:
    # 1. Gather all blood alerts
    blood_alerts = []
    low_hb = False
    
    for marker, data in blood_results.items():
        if "🚨" in data["status"]:
            blood_alerts.append(f"• {marker}: {data['observed_value']} ({data['status']}) -> Ref: {data['reference_range']}")
            if "Hemoglobin" in marker and "LOW" in data["status"]:
                low_hb = True
                
    blood_summary_text = "\n".join(blood_alerts) if blood_alerts else "• All monitored biochemical metrics fall within standard physiological ranges."
    
    # 2. Gather acoustic metrics
    acoustic_finding = audio_metrics.get("acoustic_classification", "Unclassified")
    confidence = audio_metrics.get("confidence_score", "N/A")
    
    # 3. Intelligent Cross-Analysis Logic (Data Fusion)
    diagnostic_insight = ""
    if "Murmur" in acoustic_finding and low_hb:
        diagnostic_insight = "⚠️ CLINICAL CORRELATION: Combined findings of Low Hemoglobin (Anemia) and turbulent heart sounds strongly suggest a physiological 'Anemic Murmur' caused by decreased blood viscosity. Recommend iron profile evaluation."
    elif "Murmur" in acoustic_finding:
        diagnostic_insight = "⚠️ CLINICAL CORRELATION: Isolated turbulent systolic sound detected. Suggests potential structural valve abnormality (e.g., aortic stenosis or mitral regurgitation). Recommend echocardiogram evaluation."
    elif low_hb:
        diagnostic_insight = "⚠️ CLINICAL CORRELATION: Microcytic/Normocytic Anemia indicated by low Hb marker. Cardiac acoustic pathways present clean rhythms. Suggests purely dietary or metabolic iron deficiency."
    else:
        diagnostic_insight = "✅ SYSTEM INSIGHT: No immediate cross-system pathophysiological correlations detected. Patient displays stable hemodynamic parameters."

    # 4. Generate the complete formatted brief
    detailed_report = f"""
====================================================================
        NAVAL MEDICAL SUPPORT SERVICE SYSTEM - MULTI-MODAL ANALYSIS
====================================================================
[1. CLINICAL CONTEXT & HISTORY]
{patient_history}

[2. ACOUSTIC CORE (HEART SOUNDS DETAILED FINDING)]
- Diagnostic Class: {acoustic_finding}
- Confidence Layer : {confidence}
- Telemetry Matrix : Matrix Size {audio_metrics.get('feature_dimensions')} | Total Samples: {audio_metrics.get('total_samples_extracted')}

[3. BIOCHEMICAL PROFILE ANALYSIS (FULL BLOOD PANEL)]
{blood_summary_text}

====================================================================
[4. ADVANCED CLINICAL SYNTHESIS REPORT]
{diagnostic_insight}

RECOMMENDED NEXT ACTIONS FOR MEDICAL OFFICER:
1. Conduct targeted echocardiography if structural murmur flags persist.
2. Review physiological workloads if operational fatigue correlates with low baseline oxygen-carrying markers (Hb).
====================================================================
"""
    return detailed_report