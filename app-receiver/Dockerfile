FROM python:3.11

WORKDIR /app-receiver

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python3", "services/rabbitmq.py"]