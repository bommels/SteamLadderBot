FROM python:3.6-slim

RUN apt-get update && apt-get install -y --no-install-recommends swig build-essential libssl-dev ffmpeg

WORKDIR /opt/app
ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . /opt/app

CMD ["python", "bot/bot.py"]
