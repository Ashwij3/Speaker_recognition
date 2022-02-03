from pydub import AudioSegment
import librosa
import os


t1 = 0000  # Works in milliseconds
t2 = 2000


def split():

    global t1
    global t2

    files = r'data_folder_path'
    f = len(files)
    print(f)
    
    for i in range(1,f+1):
        t = int(librosa.get_duration(filename=rf"data_folder_path"))
        print(t)
        newAudio = AudioSegment.from_wav(fr"data_folder_path")
        for j in range(1,(t//2)+1):
            print(t1,t2)
            new = newAudio[t1:t2]
            t1 = t1 + 2000
            t2 = t2 + 2000
            new.export(f'new_audio{i}', format="wav") #Exports to a wav file in the current path.



split()

