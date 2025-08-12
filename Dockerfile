# Dockerfile for FreeWriter
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=FreeWriter.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libjpeg-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Make startup script executable
RUN chmod +x startup.sh

# Create necessary directories
RUN mkdir -p /app/media/img /app/media/pdf /app/staticfiles /app/logs

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/books/health/ || exit 1

# Run the startup script
CMD ["./startup.sh"]
