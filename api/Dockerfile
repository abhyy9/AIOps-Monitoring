FROM python:3.11-slim

WORKDIR /app

COPY ../ai-model/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ../ai-model/train.py .
COPY ../ai-model/ ./ai-model/
COPY . .

RUN python train.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]