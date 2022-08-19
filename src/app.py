from deepspeech import Model
import numpy as np
import transcribe

model_path = "./models/models.pbmm"
scorer_path = "./models/models.scorer"

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
        transcribe.run(ds)
    except Exception as ex:
        print("Error occurred attempting to transcribe")
        print(ex)
        statusCode = 400
        response = "TRANSCRIBE_FAILED"
    return {
        "statusCode": statusCode,
        "body": response
    }