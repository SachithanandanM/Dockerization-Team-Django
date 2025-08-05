# Use official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside container
WORKDIR /app

# Copy your application code (currently only 'products/' app)
COPY ./products /app/products

# Install dependencies (make sure to add requirements.txt later)
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose port (Django default)
EXPOSE 8000

# Start command (replace with your manage.py-based command later)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
