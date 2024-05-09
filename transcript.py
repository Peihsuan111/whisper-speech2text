import whisper
from datetime import timedelta
import glob, sys


def formatter_time(seconds):
    td = timedelta(seconds=seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    microseconds = td.microseconds
    return f"{hours:02}:{minutes:02}:{seconds:02}.{microseconds//1000:03}"


voice_files = glob.glob("*.mp3")
if len(voice_files) > 2:
    print("there are more than 2 mp3 files inside folder!")
    sys.exit()

voice_file = voice_files[0]
output_txt = voice_file.split(".")[0] + ".txt"
# Traditional Chinese: large-v2
model = whisper.load_model("large-v2")
result = model.transcribe(voice_file)

sentences = ""
for x in result["segments"]:
    sentence = (
        f"[{formatter_time(x['start'])} --> {formatter_time(x['end'])}] {x['text']}"
    )
    sentences += sentence
    sentences += "\n"
    print(sentence)

with open(output_txt, "w") as text_file:
    text_file.write(str(sentences))
