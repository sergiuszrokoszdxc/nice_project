FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY ./mastermind mastermind