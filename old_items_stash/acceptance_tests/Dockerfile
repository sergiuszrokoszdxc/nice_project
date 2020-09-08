FROM python:3.8.3-alpine3.11 as build

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "-m", "unittest", "acceptance_tests"]