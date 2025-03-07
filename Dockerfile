# Stage 1: Build stage
FROM python:3.11-slim as builder

# Set the working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY . .

# Stage 2: Runtime stage
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install runtime dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files from the build stage
COPY --from=builder /app /app

# Expose the port FastAPI runs on
EXPOSE 8000

# Set Loguru to use JSON format (optional, for structured logging)
ENV LOGURU_FORMAT="{\"time\": \"{time}\", \"level\": \"{level}\", \"message\": \"{message}\"}"

# Create a non-root user
RUN useradd -m appuser
USER appuser

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
