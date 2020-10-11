import io
import os
from google.cloud import speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "MyFirstProject-da5d6b04be74.json"

def speech2text():
    client = speech.SpeechClient()

    file_name = "output.wav"
    with io.open(file_name, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content = content)

    config = speech.RecognitionConfig(
        audio_channel_count = 2,
        sample_rate_hertz = 44100,
        enable_word_time_offsets = True,
        language_code = "en-US",
    )

    response = client.recognize(request={"config": config, "audio": audio})
    ret = []
    for res in response.results:
        for words in res.alternatives[0].words:
            ret.append([str(words.word), int(words.end_time.seconds) + float(words.end_time.microseconds/1000000)])

    tr = []
    for res in response.results:
        tr.append(res.alternatives[0].transcript.strip())
    return tr, ret

if __name__ == "__main__":
    print(speech2text())