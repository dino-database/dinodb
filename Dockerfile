# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create the /app/data directory and set appropriate permissions
RUN mkdir -p /app/data && chown -R appuser:appuser /app/data

# Switch to the non-root user
USER appuser

# Expose the application port
EXPOSE 8000

# Command to run the application
CMD [ "python", "main.py" ]