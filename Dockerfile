FROM python:3.7-slim

WORKDIR /app

COPY . /app

RUN python3 -m pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["/bin/bash", "/app/run.sh"]