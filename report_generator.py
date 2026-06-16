def compile_patient_summary(patient_history: str, audio_metrics: dict, blood_results: dict) -> str:
    """
    Integrates clinical inputs, acoustic telemetry, and biochemical markers
    into a standardized medical synthesis framework for evaluation.
    """
    
    # 1. Parse out flagged blood anomalies for quick triage visibility
    anomalies = []
    if isinstance(blood_results, dict):
        for marker, data in blood_results.items():
            if "status" in data and "🚨" in data["status"]:
                anomalies.append(f"{marker}: {data['observed_value']} (Ref: {data['reference_range']})")
    
    anomalies_text = ", ".join(anomalies) if anomalies else "None Detected"
    
    # 2. Extract key structural parameters from our working acoustic engine
    feature_dims = audio_metrics.get("feature_dimensions", "N/A")
    total_samples = audio_metrics.get("total_samples_extracted", "N/A")
    
    # 3. Compile everything into a unified clinical brief
    clinical_brief = f"""
====================================================================
            NAVAL MEDICAL SUPPORT SERVICE SYSTEM - REPORT SUMMARY
====================================================================
[CLINICAL CONTEXT / PATIENT HISTORY]
{patient_history}

[ACOUSTIC TELEMETRY (DIGITAL STETHOSCOPE CORE)]
- Feature Matrix Map Dimensions : {feature_dims}
- Total Auditory Packets Isolated: {total_samples}
- Acoustic Pipeline Status      : Fingerprint Isolated Successfully

[BIOCHEMICAL SCREENING (BLOOD ANALYSIS LAYER)]
- Flagged Lab Anomalies Detected: {anomalies_text}
====================================================================
RECOMMENDED NEXT ACTIONS FOR MEDICAL OFFICER:
1. Cross-reference localized acoustic signatures with verified clinical anomalies.
2. Monitor patient vital trend metrics if localized anomalies exist.
"""
    return clinical_brief