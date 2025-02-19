FROM node:23-alpine AS frontend

WORKDIR /app

COPY frontend/package*.json .

RUN npm install

COPY frontend /app

RUN npm run build


FROM python:3.13.2-slim AS backend

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install -r requirements.txt

COPY backend /app

COPY --from=frontend /app/dist static/

EXPOSE 8000

CMD [ "python", "-m" , "gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
