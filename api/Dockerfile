FROM python:3.11-slim

WORKDIR /app

COPY ai-model/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ai-model/train.py .
RUN python train.py

COPY api/main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
