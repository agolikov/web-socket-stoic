# Use the official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the backend code to the container
COPY backend.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "backend:app", "--host", "0.0.0.0", "--port", "8000"]