FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port Hugging Face Spaces expects
EXPOSE 7860

# Run the FastAPI server continuously
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
