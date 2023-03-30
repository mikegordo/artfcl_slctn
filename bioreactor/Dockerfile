FROM python:3.9-slim-buster

WORKDIR /app

ADD . /app

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

CMD [ "python3", "main.py" ]
