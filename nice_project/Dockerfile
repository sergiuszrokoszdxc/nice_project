FROM python:3.8.3-alpine3.11 as build

LABEL version="0.2"
LABEL project="nice project"
LABEL name="Sergiusz Rokosz"
LABEL email="<sergiusz.rokosz@dxc.com>"

RUN python3 -m pip install --upgrade pip \
  && pip install wheel

RUN mkdir /wheel

COPY . .

RUN python3 -m pip wheel --wheel-dir=/wheel -r requirements.txt \
  && python3 -m pip install --no-index --find-links=/wheel -r requirements.txt

RUN python3 -m pip wheel --wheel-dir=/wheel --no-index --find-links=/wheel .

RUN python3 -m pip install -r requirements_dev.txt

ENTRYPOINT [ "/bin/sh", "entrypoint.sh" ]

FROM python:3.8.3-alpine3.11 as application

RUN python3 -m pip install --upgrade pip \
  && pip install wheel

RUN mkdir /wheel

COPY --from=build /wheel /wheel
# add statics folder
RUN pip install --no-index --find-links=/wheel /wheel/*.whl

COPY entrypoint.sh entrypoint.sh

ENV FLASK_APP=nice_project.app:flask_app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000