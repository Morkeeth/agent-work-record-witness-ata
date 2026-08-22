FROM python:3.12-slim
WORKDIR /app
COPY . .
ENV PORT=8080 FLEET_STORE=jsonl FLEET_STORE_PATH=/tmp/fleet-propagations.jsonl
EXPOSE 8080
CMD ["python3", "cloud/service.py"]
