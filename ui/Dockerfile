FROM python:3.9-slim-buster

WORKDIR /app/main

ADD . /app/main

ADD ./shared /app/shared

RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 8080

CMD [ "python3", "main.py" ]
