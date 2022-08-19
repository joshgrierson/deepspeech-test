ARG FUNCTION_DIR="/function"

FROM python:3.7 as build-image

RUN apt-get update && \
    apt-get install -y \
    g++ \
    make \
    cmake \
    unzip \
    libcurl4-openssl-dev

ARG FUNCTION_DIR

RUN mkdir -p ${FUNCTION_DIR}

COPY src/* ${FUNCTION_DIR}
COPY audio/* ${FUNCTION_DIR}/audio/

RUN mkdir ${FUNCTION_DIR}/models
RUN curl -L -o ${FUNCTION_DIR}/models/models.pbmm https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm
RUN curl -L -o ${FUNCTION_DIR}/models/models.scorer https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer

# Lambda runtime initerface client
RUN pip install \
    --target ${FUNCTION_DIR} \
    awslambdaric

FROM python:3.7

ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie

RUN chmod 755 /usr/bin/aws-lambda-rie
RUN pip install deepspeech

ENTRYPOINT [ "/usr/bin/aws-lambda-rie", "/usr/local/bin/python", "-m", "awslambdaric" ]

CMD [ "app.lambda_handler" ]