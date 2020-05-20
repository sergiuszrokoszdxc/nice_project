FROM python

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD [ "python3", "-m", "unittest", "acceptance_tests"]