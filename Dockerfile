# Use an official Python image compatible with Django 4.2.4
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*
    
# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Copy entrypoint script
# COPY entrypoint.sh /app/entrypoint.sh
# Ensure entrypoint has Unix line endings and is executable (fixes permission denied on some hosts)
# RUN sed -i 's/\r$//' /app/entrypoint.sh && chmod +x /app/entrypoint.sh
# Execute explicitly with bash to avoid exec permission / interpreter issues
# ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Expose port (default for Django)
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
