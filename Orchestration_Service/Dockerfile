FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

ENV PYTHONPATH /app

EXPOSE 50051

CMD ["python", "src/main.py"]