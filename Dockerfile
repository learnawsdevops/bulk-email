# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy requirements and app files


# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
