from deepspeech import Model
from chunk import chunk_fn
import transcribe

model_path = "./models/models.pbmm"
scorer_path = "./models/models.scorer"

if __name__ == "__main__":
    ds = Model(model_path)
    ds.enableExternalScorer(scorer_path)
    chunk_fn("./audio/long.wav", "chunk.wav", 0.2, ds.sampleRate())
    transcribe.run(ds)