FROM python:3.12.2-slim

WORKDIR /calorie-tracker

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host=0.0.0.0