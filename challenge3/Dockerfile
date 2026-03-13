FROM python:3.11-slim
WORKDIR /app
RUN pip install flask --no-cache-dir && \
    apt-get update && apt-get install -y iputils-ping && \
    rm -rf /var/lib/apt/lists/*
COPY app.py .
EXPOSE 5000
CMD ["python", "app.py"]
