import pyaudio
import wave

class Recorder:
    def __init__(self):
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 2
        self.fs = 44100
        self.filename = "output.wav"
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = self.sample_format, channels = self.channels, rate = self.fs, frames_per_buffer = self.chunk, input = True)
        self.frames = []
        self.RECORDING = False
        self.PROCESSED = False

    def start(self):
        self.RECORDING = True
        print('Recording')
        while self.RECORDING:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.process()
        self.PROCESSED = True
        print('Finished recording')

    def process(self):
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()