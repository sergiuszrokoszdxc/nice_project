FROM python:3.8.3-alpine3.11 as build

LABEL version="0.2"
LABEL project="nice project"
LABEL name="Sergiusz Rokosz"
LABEL email="<sergiusz.rokosz@dxc.com>"

RUN apk add build-base \
  && apk add linux-headers \
  && apk add python-dev

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install wheel

RUN mkdir /wheel

COPY . .

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip wheel --wheel-dir=/wheel . \
  && python3 -m pip install --no-index --find-links=/wheel .

FROM python:3.8.3-alpine3.11 as application

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install wheel

RUN mkdir /wheel

COPY --from=build /wheel /wheel

RUN python3 -m pip install --no-index --find-links=/wheel /wheel/*.whl

COPY entrypoint.sh entrypoint.sh

RUN sed -i 's/\r$//' entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
# TODO: add pip cache