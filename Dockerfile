# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Set Loguru to use JSON format (optional, for structured logging)
ENV LOGURU_FORMAT="{\"time\": \"{time}\", \"level\": \"{level}\", \"message\": \"{message}\"}"

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
