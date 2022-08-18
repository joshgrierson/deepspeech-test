import subprocess

def chunk_fn(audio_input, audio_ouput, duration = 0.1):
    try:
        print("Chunking audio...")
        str_duration = str(duration)
        subprocess.call([
            "sox", audio_input, audio_ouput,
            "silence",
            "1", str_duration, "1%",
            "1", str_duration, "1%",
            ":", "newfile", ":", "restart"
        ])
        print("Completed!")
    except Exception as ex:
        print("Failed to call sox")
        print(ex)
