FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/app/ /app