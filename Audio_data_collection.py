
import pyaudio
import wave
import noisereduce as nr
import os
import scipy.io.wavfile as wavfile
import time


def add_user():
    #Name of of the subject whose data is collected
    name = input("Subject Name:")

    #Creates Subject directory path
    Data_folder= "data_folder_path"+ name
    #checks if directory already exists
    c=os.path.exists(Data_folder)
    # else creates the directory
    if c== False:
        os.mkdir(Data_folder)



    #initializing parameters

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 88200
    CHUNK = 1024
    


    #Collection process
    audio = pyaudio.PyAudio()
    print("Speak first paragraph")
    print("Speak in 3 seconds")
    time.sleep(1)
    print("Speak in 2 seconds")
    time.sleep(1)
    print("Speak in 1 second")
    time.sleep(1)
    start_time=time.time()

    #Starts recording and can be terminated pressing Ctrl-c
    print("Recording in process, press Ctrl-c to end recording")
    try:
        while True:
            stream = audio.open(format=FORMAT, channels=CHANNELS,rate=RATE, input=True,frames_per_buffer=CHUNK)
            current_time=time.time()
            RECORD_SECONDS=current_time-start_time
            print("recording...")
    except KeyboardInterrupt:
        pass
                
    frames = []

    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    #Saving as .wav format
    stream.stop_stream()
    stream.close()
    audio.terminate()
    fil_nam = input("file name :")
    waveFile = wave.open(Data_folder + '/' + fil_nam + '.wav', 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    print("Audio saved")

    print("Initializing audio cleansing....")

    Data_folder = "C:/Users/ashwi/PycharmProjects/AI_voice_signature/voice_data/" + name + "/cleansed"
    c = os.path.exists(Data_folder)
    if c == False:
        os.mkdir(Data_folder)

    #audio background removal
    rate, data = wavfile.read("data_folder_path" + name +'/'  + fil_nam + ".wav")
    reduced_noise = nr.reduce_noise(y=data, sr=rate)
    wavfile.write("data_folder_path" + name + "/cleansed/" + fil_nam + ".wav", rate,reduced_noise)
    print("Done")


if __name__ == '__main__':
    add_user()

