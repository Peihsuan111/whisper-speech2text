import whisper
import datetime
import glob, sys


def formatter_time(time_int):
    time_str = str(datetime.timedelta(seconds=time_int))
    if "." not in time_str:
        time_str += ".000"
    else:
        time_str = time_str[:-3]
    return time_str


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
