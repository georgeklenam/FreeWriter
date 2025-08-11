# FreeWriter Production Deployment Guide

This guide covers deploying FreeWriter to production using Docker with Gunicorn and WhiteNoise.

## 🚀 Quick Start

### 1. Build Production Image

```bash
# Build the production Docker image
docker build -f Dockerfile.prod -t freewriter-prod .

# Or using the production dockerignore
docker build -f Dockerfile.prod --file .dockerignore.prod -t freewriter-prod .
```

### 2. Run Production Container

```bash
# Run the production container
docker run -d \
  --name freewriter-prod \
  -p 8000:8000 \
  -v $(pwd)/media:/app/media \
  -v $(pwd)/logs:/app/logs \
  -e SECRET_KEY="your-secret-key-here" \
  freewriter-prod
```

### 3. Access the Application

- **Main Site**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Default Admin**: `admin` / `f001`

## 📋 Production Requirements

### System Requirements

- **Docker**: 20.10+
- **Memory**: 512MB minimum, 1GB recommended
- **Storage**: 2GB minimum for application + media files
- **CPU**: 1 core minimum, 2 cores recommended

### Environment Variables

```bash
# Required
SECRET_KEY=your-secret-key-here

# Optional (for HTTPS)
SECURE_SSL_REDIRECT=True
SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
```

## 🔧 Production Configuration

### Security Settings

The production settings include:

- ✅ **DEBUG = False**
- ✅ **Security headers** (HSTS, XSS protection, etc.)
- ✅ **CSRF protection**
- ✅ **Session security**
- ✅ **Non-root user** in container

### Performance Optimizations

- ✅ **Gunicorn** with 3 workers
- ✅ **WhiteNoise** for static file serving
- ✅ **Compressed static files**
- ✅ **SQLite3** database
- ✅ **In-memory caching**

### File Storage

- ✅ **Media files** stored in `/app/media/`
- ✅ **Static files** collected to `/app/staticfiles/`
- ✅ **Logs** written to `/app/logs/`

## 🐳 Docker Commands

### Build and Run

```bash
# Build production image
docker build -f Dockerfile.prod -t freewriter-prod .

# Run with volume mounts
docker run -d \
  --name freewriter-prod \
  -p 8000:8000 \
  -v $(pwd)/media:/app/media \
  -v $(pwd)/logs:/app/logs \
  -e SECRET_KEY="your-secret-key-here" \
  freewriter-prod

# Run in background
docker run -d \
  --name freewriter-prod \
  -p 8000:8000 \
  -v $(pwd)/media:/app/media \
  -v $(pwd)/logs:/app/logs \
  -e SECRET_KEY="your-secret-key-here" \
  --restart unless-stopped \
  freewriter-prod
```

### Management Commands

```bash
# View logs
docker logs freewriter-prod

# Follow logs
docker logs -f freewriter-prod

# Execute commands in container
docker exec -it freewriter-prod python manage.py shell --settings=FreeWriter.settings_prod

# Create superuser
docker exec -it freewriter-prod python manage.py createsuperuser --settings=FreeWriter.settings_prod

# Run management commands
docker exec -it freewriter-prod python manage.py create_books_from_images --settings=FreeWriter.settings_prod
docker exec -it freewriter-prod python manage.py fix_pdfs --settings=FreeWriter.settings_prod
docker exec -it freewriter-prod python manage.py fix_images --settings=FreeWriter.settings_prod

# Stop container
docker stop freewriter-prod

# Remove container
docker rm freewriter-prod

# Remove image
docker rmi freewriter-prod
```

## 🔒 Security Considerations

### 1. Secret Key

```bash
# Generate a secure secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set in environment
export SECRET_KEY="your-generated-secret-key"
```

### 2. Allowed Hosts

Update `ALLOWED_HOSTS` in `settings_prod.py`:

```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'localhost']
```

### 3. HTTPS (Recommended)

```bash
# Set HTTPS environment variables
export SECURE_SSL_REDIRECT=True
export SECURE_PROXY_SSL_HEADER=('HTTP_X_FORWARDED_PROTO', 'https')
```

## 📊 Monitoring and Logging

### Log Files

- **Application logs**: `/app/logs/django.log`
- **Gunicorn logs**: Container stdout/stderr
- **Access logs**: Gunicorn access log

### Health Checks

The container includes health checks:
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' freewriter-prod
```

### Performance Monitoring

```bash
# Monitor resource usage
docker stats freewriter-prod

# Check disk usage
docker exec freewriter-prod df -h
```

## 🔄 Backup and Recovery

### Database Backup

```bash
# Backup SQLite database
docker exec freewriter-prod cp /app/db.sqlite3 /app/backup_$(date +%Y%m%d_%H%M%S).sqlite3

# Copy backup from container
docker cp freewriter-prod:/app/backup_20231201_120000.sqlite3 ./backup.sqlite3
```

### Media Files Backup

```bash
# Backup media directory
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz media/
```

### Full Backup Script

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="backups/$DATE"

mkdir -p $BACKUP_DIR

# Backup database
docker exec freewriter-prod cp /app/db.sqlite3 /app/backup_$DATE.sqlite3
docker cp freewriter-prod:/app/backup_$DATE.sqlite3 $BACKUP_DIR/

# Backup media files
tar -czf $BACKUP_DIR/media_backup.tar.gz media/

# Backup logs
tar -czf $BACKUP_DIR/logs_backup.tar.gz logs/

echo "Backup completed: $BACKUP_DIR"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Permission Errors

```bash
# Fix media directory permissions
sudo chown -R 1000:1000 media/
sudo chmod -R 755 media/
```

#### 2. Static Files Not Loading

```bash
# Recollect static files
docker exec freewriter-prod python manage.py collectstatic --noinput --settings=FreeWriter.settings_prod
```

#### 3. Database Issues

```bash
# Reset database (WARNING: This will delete all data)
docker exec freewriter-prod rm /app/db.sqlite3
docker exec freewriter-prod python manage.py migrate --settings=FreeWriter.settings_prod
```

#### 4. Memory Issues

```bash
# Check memory usage
docker stats freewriter-prod

# Increase memory limit
docker run -d --memory=1g --name freewriter-prod ...
```

### Log Analysis

```bash
# View recent logs
docker logs --tail=100 freewriter-prod

# Search for errors
docker logs freewriter-prod | grep -i error

# Monitor real-time
docker logs -f freewriter-prod
```

## 🔄 Updates and Maintenance

### Update Application

```bash
# Stop current container
docker stop freewriter-prod

# Remove old container
docker rm freewriter-prod

# Build new image
docker build -f Dockerfile.prod -t freewriter-prod .

# Run new container
docker run -d \
  --name freewriter-prod \
  -p 8000:8000 \
  -v $(pwd)/media:/app/media \
  -v $(pwd)/logs:/app/logs \
  -e SECRET_KEY="your-secret-key-here" \
  --restart unless-stopped \
  freewriter-prod
```

### Database Migrations

```bash
# Run migrations
docker exec freewriter-prod python manage.py migrate --settings=FreeWriter.settings_prod

# Check migration status
docker exec freewriter-prod python manage.py showmigrations --settings=FreeWriter.settings_prod
```

## 📈 Scaling Considerations

### Horizontal Scaling

For high traffic, consider:

- **Load balancer** (nginx, haproxy)
- **Multiple containers** behind load balancer
- **External database** (PostgreSQL, MySQL)
- **CDN** for static files
- **Redis** for caching

### Vertical Scaling

```bash
# Increase resources
docker run -d \
  --name freewriter-prod \
  --memory=2g \
  --cpus=2 \
  -p 8000:8000 \
  -v $(pwd)/media:/app/media \
  -v $(pwd)/logs:/app/logs \
  -e SECRET_KEY="your-secret-key-here" \
  freewriter-prod
```

## 🎯 Production Checklist

- [ ] **Security**
  - [ ] Secret key set via environment variable
  - [ ] DEBUG = False
  - [ ] Allowed hosts configured
  - [ ] HTTPS enabled (recommended)

- [ ] **Performance**
  - [ ] Static files collected
  - [ ] Gunicorn workers configured
  - [ ] WhiteNoise enabled
  - [ ] Logging configured

- [ ] **Monitoring**
  - [ ] Health checks working
  - [ ] Logs accessible
  - [ ] Resource monitoring set up

- [ ] **Backup**
  - [ ] Database backup strategy
  - [ ] Media files backup
  - [ ] Recovery procedures tested

- [ ] **Documentation**
  - [ ] Deployment procedures documented
  - [ ] Troubleshooting guide available
  - [ ] Contact information for support

## 📞 Support

For deployment issues:

1. Check the logs: `docker logs freewriter-prod`
2. Verify configuration in `settings_prod.py`
3. Test locally with production settings
4. Review this deployment guide

---

**Note**: This deployment guide assumes you're using Docker. For other deployment methods (Heroku, AWS, etc.), additional configuration may be required.
