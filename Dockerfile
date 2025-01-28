FROM python:3.12.2-slim

WORKDIR /calorie-tracker

COPY requirements.txt /calorie-tracker/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /calorie-tracker/requirements.txt

COPY app /calorie-tracker/app

COPY main.py /calorie-tracker/main.py

EXPOSE 8000

CMD ["fastapi", "run" , "main.py", "--port", "8000"]
