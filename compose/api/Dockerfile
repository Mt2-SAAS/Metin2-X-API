FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./compose/api/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

EXPOSE 8000

CMD ["/entrypoint.sh", "db:3306", "--", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
