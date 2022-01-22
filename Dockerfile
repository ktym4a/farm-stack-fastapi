FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# RUN apk update && apk add python3-dev gcc libc-dev

RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

COPY main.py .
EXPOSE 8000
# FastAPIを8000ポートで待機
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
