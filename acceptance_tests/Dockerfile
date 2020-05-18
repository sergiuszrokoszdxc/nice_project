FROM python

COPY . .

RUN python3 -m pip install -r requirements

CMD [ "python3", "-m", "unittest", "acceptance_tests"]