# Use official Python image
FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy requirements and app files


# Install dependencies

RUN rm -rf firstapp
COPY . /app
# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
