import numpy as np
from pathlib import Path
from sklearn import preprocessing
import tensorflow as tf
import librosa
import librosa.display
from tensorflow import keras


#Path of the audio data directory
Data_directory="/home/ak47/AI_proj/Data/"
entries = Path(Data_directory)

#List of speakers
subject_names=[]
for entry in entries.iterdir():
    subject_names.append(str(entry.name))

#Path of all the audio clips
audio=[]
for name in subject_names:
    file= Path(Data_directory+name)
    for f in file.iterdir():
        audio.append((Data_directory+name+"/"+str(f.name)))

speakers=[]
for file_path in audio:
    speakers.append(tf.strings.split(file_path, '/')[-2])
speaker_encoder = preprocessing.LabelEncoder()
speaker_idx = speaker_encoder.fit_transform([bytes.decode(s.numpy()) for s in speakers])
encoded_speaker_ds = tf.data.Dataset.from_tensor_slices(speaker_idx)
unique_speakers = len(speaker_encoder.classes_)


#Extraction of MFCC features
mfcc_f=[]
for i in range(1):
    wave, sample_rate = librosa.load(audio[i], mono=True, sr=22050)
    mfcc = librosa.feature.mfcc(wave,n_mfcc=128, sr=22050)
    mfcc = mfcc[:, :128]
    pad_width = 128 - mfcc.shape[1]
    mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    mfcc = tf.convert_to_tensor(mfcc)
    mfcc = tf.expand_dims(mfcc, 2)
    mfcc_f.append(mfcc)

audio_ds=tf.data.Dataset.from_tensor_slices(mfcc_f) 
complete_labeled_ds = tf.data.Dataset.zip((audio_ds, encoded_speaker_ds))
tf.data.experimental.save(complete_labeled_ds, Data_directory+'final_data')