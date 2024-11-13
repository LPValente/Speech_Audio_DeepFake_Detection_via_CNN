import numpy as np
import librosa
import librosa.display
from pydub import AudioSegment, silence
import matplotlib.pyplot as plt
import pathlib
import os


def plot_Signal(file):
    y, sr = librosa.load(file)
    plt.plot(y)
    plt.title('Sinal de Áudio')
    plt.xlabel('Tempo (samples)')
    plt.ylabel('Amplitude')
    
def plot_FFT(file, n_fft=2048):
    y, sr = librosa.load(file)
    ft = np.abs(librosa.stft(y[:n_fft], hop_length = n_fft+1))
    plt.plot(ft)
    plt.title('Spectrum')
    plt.xlabel('Frequency Bin')
    plt.ylabel('Amplitude')
    
def plot_Spectrogram_STFT(file):
    y, sr = librosa.load(file)
    spec = np.abs(librosa.stft(y,
                               #sr=sr,
                               hop_length=10))
    #spec = librosa.stft(y, hop_length=1)
    spec = librosa.amplitude_to_db(spec, ref=np.max)
    librosa.display.specshow(spec,
                             sr=sr,
                             hop_length=10,
                             x_axis='s',
                             y_axis='hz',
                            cmap='viridis'
                            )
    plt.colorbar(format='%+2.0f dB')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência (Hz)')
    ax = plt.gca()
    ax.set_ylim(0,8000)
    plt.title('Espectrograma (STFT)')
    
def plot_Spectrogram_MEL(file):
    y, sr = librosa.load(file)
    
    plt.figure()
    mel_spect = librosa.feature.melspectrogram(y=y,
                                               sr=sr,
                                               n_fft=1024,
                                               hop_length=10
                                               )
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
    librosa.display.specshow(mel_spect,
                             sr=sr,
                             hop_length=10,
                             y_axis='mel',
                             x_axis='time',
                             cmap='viridis'
                             )
    plt.colorbar(format='%+2.0f dB')
    plt.xlabel('Tempo (s)')
    plt.ylabel('Frequência Mel')
    plt.title('Espectrograma (Mel)')
    
def gen_Spectrogram_MEL(file, fileSaveName):
    y, sr = librosa.load(file)
    mel_spect = librosa.feature.melspectrogram(y=y,
                                           sr=sr,
                                           n_fft=1024,
                                           hop_length=10
                                           )
    mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
    plt.axis("off")
    plt.subplots_adjust(0,0,1,1,0,0)
    librosa.display.specshow(mel_spect,
                         hop_length=10,
                         #y_axis='mel',
                         #fmax=8000,
                         #x_axis='time'
                         )
    plt.savefig(fileSaveName)
    plt.clf()


#------------------------------------------------------------------------#

def audio_Lenght(file, format):
    audio = AudioSegment.from_file(file, format=format)
    length_in_sec = len(audio) / 1000
    return length_in_sec

def remove_Audio_Silence(file, format, length_in_sec):
    audio = AudioSegment.from_file(file, )
    leading_silence = silence.detect_leading_silence(audio)
    trailing_silence = silence.detect_leading_silence(audio.reverse())

    trimmed = audio[leading_silence:length_in_sec-trailing_silence]
    duration_trimmed = len(trimmed) / 1000
    return trimmed, duration_trimmed

def audio_Parts(filename, path, trimmed, duration_trimmed, duration, format): #verificar
    i = 1
    k=int(duration_trimmed/2)
    while duration_trimmed >= 2:
                parte_audio = trimmed[:duration]
                
                parte_audio.export(path+filename[:-4]+"-"+str(i)+"of"+str(k) + '.' + format, format=format)
                print("Salvando pedaço de arquivo "+str(i)+"of"+str(k)+": "+filename+" - "+str(len(parte_audio)/1000)+"sec")
                
                resto = trimmed[duration:]
                trimmed=resto
                duration_trimmed=len(resto) / 1000
                i=i+1
    return i