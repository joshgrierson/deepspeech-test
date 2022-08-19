import subprocess
import os
import json

audio_dir = "tmp"

def setup_tmp_dir():
    try:
        os.mkdir(audio_dir)
    except Exception as ex:
        print("Failed to mkdir [" + audio_dir + "]")
        print(ex)

def generate_audio_mapping():
    audio_chunks = os.listdir(audio_dir + "/")
    audio_chunks.sort()
    map = dict()
    for i, chunk in enumerate(audio_chunks):
        if chunk.endswith(".wav"):
            bytes = os.path.getsize(audio_dir + "/" + chunk)
            next_chunk = None
            if i < len(audio_chunks) - 1:
                next_chunk = audio_chunks[i + 1]
            map[chunk] = {
                "size": bytes / 100,
                "transcribed": None,
                "next": next_chunk
            }
    return map

def chunk_fn(audio_input, audio_ouput, duration = 0.1):
    output = audio_dir + "/" + audio_ouput
    try:
        print("Chunking audio...")
        setup_tmp_dir()
        str_duration = str(duration)
        subprocess.call([
            "sox", audio_input, output,
            "silence",
            "1", str_duration, "1%",
            "1", str_duration, "1%",
            ":", "newfile", ":", "restart"
        ])
        audio_mapping = json.dumps(generate_audio_mapping(), indent=2)
        f = open(audio_dir + "/" + "audio-mapping.json", "a")
        f.write(audio_mapping)
        f.close()
        print("Completed!")
    except Exception as ex:
        print("Failed to complete chunking")
        print(ex)
