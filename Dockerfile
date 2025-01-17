FROM python:3.12.2-slim

WORKDIR /calorie-tracker

RUN mkdir -p /logs

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD uvicorn main:app --host=0.0.0.0