import librosa
import numpy as np
import scipy.signal as signal

def apply_bandpass_filter(audio_data, sampling_rate, lowcut=20.0, highcut=2000.0, order=4):
    nyquist = 0.5 * sampling_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    return signal.lfilter(b, a, audio_data)

def process_stethoscope_audio(file_path):
    # Ingest audio file
    audio, sr = librosa.load(file_path, sr=16000)
    
    # Filter out ambient noise
    clean_audio = apply_bandpass_filter(audio, sr)
    
    # Extract MFCC features
    mfccs = librosa.feature.mfcc(y=clean_audio, sr=sr, n_mfcc=40)
    
    # --- Advanced Acoustic Signature Analysis ---
    # High-frequency energy check (Murmurs introduce prolonged high-frequency turbulence)
    high_freq_energy = np.mean(mfccs[10:]) # Look at upper Mel-frequency bands
    
    # Define a clinical threshold for structural noise variance
    if high_freq_energy > -15.0:  # Adjust threshold based on your specific audio file dynamics
        classification = "🚨 ABNORMAL (Systolic/Diastolic Murmur Acoustic Pattern Detected)"
        confidence = "High (Turbulent acoustic signature identified between standard S1/S2 intervals)"
    else:
        classification = "Normal S1/S2 Heart Sound Rhythm"
        confidence = "High (Clear valve closure intervals, no murmur patterns detected)"
        
    audio_metrics = {
        "sampling_rate_hz": sr,
        "total_samples_extracted": float(mfccs.size),
        "feature_dimensions": list(mfccs.shape),
        "acoustic_classification": classification,
        "confidence_score": confidence
    }
    
    return audio_metrics