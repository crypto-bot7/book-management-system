FROM python:3.12

WORKDIR /app

RUN apt-get update && apt-get install -y python3-dev gcc build-essential musl-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade cython

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:application", "--host", "0.0.0.0", "--port", "8000"]