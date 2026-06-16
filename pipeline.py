import librosa
import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

def apply_bandpass_filter(audio_data, sampling_rate, lowcut=20.0, highcut=2000.0, order=4):
    """
    Applies a clinical-grade bandpass filter to remove room noise,
    hums, and friction while isolating heart/lung frequency bands.
    """
    nyquist = 0.5 * sampling_rate
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = signal.butter(order, [low, high], btype='band')
    filtered_audio = signal.lfilter(b, a, audio_data)
    return filtered_audio

def process_stethoscope_audio(file_path):
    print(f"🎬 Loading audio data pipeline for: {file_path}")
    
    # 1. Ingest audio file (Resample to standard 16kHz for ML consistency)
    audio, sr = librosa.load(file_path, sr=16000)
    
    # 2. Filter out clinical ambient noise using our bandpass filter
    clean_audio = apply_bandpass_filter(audio, sr)
    
    # 3. Extract MFCC features (captures the acoustic signature texture)
    mfccs = librosa.feature.mfcc(y=clean_audio, sr=sr, n_mfcc=40)
    
    # 4. Generate a simplified feature array for ML classification inputs
    mfccs_processed_vector = np.mean(mfccs.T, axis=0)
    
    print("✅ Extraction complete! Features transformed into mathematical vectors.")
    print(f"Shape of extracted feature matrix: {mfccs.shape}")
    
    return clean_audio, mfccs, sr

def visualize_acoustic_signature(mfccs, sr):
    """
    Generates a Spectrogram map to display during your naval interview presentation.
    """
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfccs, sr=sr, x_axis='time', cmap='coolwarm')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Stethoscope Acoustic Fingerprint (MFCC Spectrogram)')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Mel Filters')
    plt.tight_layout()
    
    print("📊 Spectrogram plot generated successfully! Displaying window...")
    plt.show()

# --- EXECUTION LINK ---
if __name__ == "__main__":
    # Point this to the exact name of the file you dropped into your folder
    target_audio_file = "test_heart_sound.wav" 
    
    try:
        clean_waves, raw_mfccs, sample_rate = process_stethoscope_audio(target_audio_file)
        visualize_acoustic_signature(raw_mfccs, sample_rate)
    except FileNotFoundError:
        print(f"❌ Error: Could not find '{target_audio_file}' in your directory.")
        print("Please ensure your test audio file is placed inside the AiStethReports folder.")