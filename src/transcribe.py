import json
from time import sleep
import workers
import numpy as np

audio_tmp_dir = "./tmp/"
audio_mapping_file = audio_tmp_dir + "audio-mapping.json"

def words_from_candidate_transcript(metadata):
    word = ""
    word_list = []
    word_start_time = 0
    # Loop through each character
    for i, token in enumerate(metadata.tokens):
        # Append character to word if it's not a space
        if token.text != " ":
            if len(word) == 0:
                # Log the start time of the new word
                word_start_time = token.start_time

            word = word + token.text
        # Word boundary is either a space or the last character in the array
        if token.text == " " or i == len(metadata.tokens) - 1:
            word_duration = token.start_time - word_start_time

            if word_duration < 0:
                word_duration = 0

            each_word = dict()
            each_word["word"] = word
            each_word["start_time"] = round(word_start_time, 4)
            each_word["duration"] = round(word_duration, 4)

            word_list.append(each_word)
            # Reset
            word = ""
            word_start_time = 0

    return word_list


def metadata_json_output(metadata):
    json_result = dict()
    json_result["transcripts"] = [{
        "confidence": transcript.confidence,
        "words": words_from_candidate_transcript(transcript),
    } for transcript in metadata.transcripts]
    return json_result

def do_transcribe(ds, cursor_key):
    file = open(audio_tmp_dir + cursor_key, "r")
    audio = np.frombuffer(file.read(), dtype=np.int16)
    # return ds.sttWithMetadata(audio, 1)
    return ds.stt(audio)

def task_complete(result):
    # meta = metadata_json_output(result)
    print("Transcribe complete: ", result)

def run(ds):
    f = open(audio_mapping_file, "r")
    mapping = dict(json.loads(f.read()))
    first_key = next(iter(mapping))
    cursor_key = first_key
    while cursor_key is not None:
        cursor = mapping[cursor_key]
        print("Transcribing audio chunk " + cursor_key + " " + str(cursor["size"]) + "kbs")
        workers.register_task(
            do_transcribe,
            cursor_key,
            ds,
            cursor_key
        )
        cursor_key = cursor["next"]
    workers.run(task_complete)