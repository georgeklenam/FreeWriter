# FreeWriter Deployment Guide

This guide covers deploying the FreeWriter Django application using Docker containers.

## Prerequisites

- Docker and Docker Compose installed
- Git (for cloning the repository)
- At least 1GB of available RAM

## Development Environment

### Quick Start

1. **Clone and navigate to the project:**

   ```bash
   git clone <repository-url>
   cd FreeWriter
   ```

2. **Build and run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Open your browser and go to `http://localhost:8000`
   - The application will be running with hot-reload enabled

### Development Commands

- **Start services:** `docker-compose up`
- **Start in background:** `docker-compose up -d`
- **Stop services:** `docker-compose down`
- **View logs:** `docker-compose logs -f web`
- **Rebuild:** `docker-compose up --build`

## Production Environment

### Environment Variables

Create a `.env` file in the project root:

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (if using external database)
DATABASE_URL=postgresql://user:password@host:port/dbname
```

### Production Deployment

1. **Build and run production container:**

   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

2. **Run database migrations:**

   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

3. **Create superuser:**

   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

4. **Collect static files:**

   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
   ```

### Production Commands

- **Start production:** `docker-compose -f docker-compose.prod.yml up -d`
- **Stop production:** `docker-compose -f docker-compose.prod.yml down`
- **View logs:** `docker-compose -f docker-compose.prod.yml logs -f web`
- **Restart:** `docker-compose -f docker-compose.prod.yml restart`

## Docker Commands Reference

### Building Images

```bash
# Build development image
docker build -t freewriter:dev .

# Build production image
docker build -f Dockerfile.prod -t freewriter:prod .
```

### Running Containers

```bash
# Run development container
docker run -p 8000:8000 -v $(pwd):/app freewriter:dev

# Run production container
docker run -p 8000:8000 freewriter:prod
```

### Container Management

```bash
# List running containers
docker ps

# Stop container
docker stop <container_id>

# Remove container
docker rm <container_id>

# View container logs
docker logs <container_id>
```

## Troubleshooting

### Common Issues

1. **Port already in use:**

   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Kill the process or change port in docker-compose.yml
   ```

2. **Permission denied errors:**

   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

3. **Database connection issues:**

   ```bash
   # Check if database is accessible
   docker-compose exec web python manage.py dbshell
   ```

4. **Static files not loading:**

   ```bash
   # Recollect static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

### Logs and Debugging

```bash
# View application logs
docker-compose logs web

# View real-time logs
docker-compose logs -f web

# Access container shell
docker-compose exec web bash

# Check Django status
docker-compose exec web python manage.py check
```

## Performance Optimization

### Production Settings

- Use `Dockerfile.prod` for production builds
- Enable gunicorn with multiple workers
- Use volume mounts for persistent data
- Implement proper logging and monitoring

### Resource Limits

Add to your docker-compose file:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

## Security Considerations

- Never commit `.env` files to version control
- Use strong, unique SECRET_KEY values
- Regularly update base images and dependencies
- Run containers as non-root users (already configured)
- Implement proper firewall rules
- Use HTTPS in production

## Monitoring and Maintenance

### Health Checks

The production container includes health checks. Monitor with:

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

### Backup Strategy

```bash
# Backup database
docker-compose exec web python manage.py dumpdata > backup.json

# Backup media files
tar -czf media_backup.tar.gz media/
```

### Updates

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose -f docker-compose.prod.yml up --build -d
```

## Support

For issues and questions:

- Check the logs: `docker-compose logs web`
- Review Django documentation
- Check Docker documentation
- Review the project README.md

---

**Note**: This deployment guide assumes you're running on a Linux/Unix system. Windows users may need to adjust some commands accordingly.
