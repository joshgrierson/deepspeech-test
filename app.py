import os
from deepspeech import Model
import numpy as np
import json

model_path = "./models/models.pbmm"
scorer_path = "./models/models.scorer"

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
    return json.dumps(json_result, indent=None)

def fetch_audio_file():
    file = open("./audio/long.wav", "rb")
    audio = np.frombuffer(file.read(), dtype=np.int16)
    return audio

# TODO: Transcode audio to have same sample rate as DS using Sox
def lambda_handler(event, context):
    ds = Model(model_path)
    statusCode = 200
    response = None
    print(event)
    try:
        ds.enableExternalScorer(scorer_path)
        samplerate = ds.sampleRate()
        print("Deepspeech sample rate " + str(samplerate))
        audio = fetch_audio_file()
        response = metadata_json_output(ds.sttWithMetadata(audio, 2))
    except Exception as ex:
        print("Error occurred attempting to transcribe")
        print(ex)
        statusCode = 400
        response = "TRANSCRIBE_FAILED"
    return {
        "statusCode": statusCode,
        "body": response
    }