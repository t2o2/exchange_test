from python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV API_KEY="VLx3KJaiJsxvIjaDMThhyofV9LK1w1xWpQT91vjAasYl1eSPeSKpuk0B"
ENV API_SECRET="GNK8enjBad5xlNXUWrHjsu/lVQ9dacei7/MpVr+G5uL341OBPca0//2yLM9XtBcZtaJZfKI5xGtTtOS+FqhirA=="

COPY . .

RUN chmod +x run_tests.sh