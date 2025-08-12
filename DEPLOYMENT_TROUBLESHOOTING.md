# FreeWriter Deployment Troubleshooting Guide

## 🚨 Common Deployment Issues

### 1. **Infinite Loop During Startup**

**Symptoms:** Application keeps restarting, showing repeated "Starting FreeWriter application..." messages

**Causes:**

- Migration conflicts between local and remote database schemas
- Database connection issues
- Missing dependencies
- Script errors causing restarts

**Solutions:**

```bash
# Stop the current deployment
docker-compose down  # or equivalent

# Check logs for specific errors
docker-compose logs -f

# Reset migrations if needed
python reset_migrations.py

# Restart deployment
docker-compose up -d
```

### 2. **Migration Conflicts**

**Symptoms:** Database setup fails with migration errors

**Solutions:**

```bash
# Option 1: Reset migrations (WARNING: This will clear your database)
python reset_migrations.py

# Option 2: Manual migration fix
python manage.py migrate --fake-initial
python manage.py migrate

# Option 3: Check migration status
python manage.py showmigrations
```

### 3. **Database Connection Issues**

**Symptoms:** "Database connection failed" errors

**Solutions:**

- Ensure database service is running
- Check database credentials in settings
- Verify network connectivity
- Check firewall settings

### 4. **Missing Dependencies**

**Symptoms:** Import errors or missing module errors

**Solutions:**

```bash
# Install requirements
pip install -r requirements.txt

# Check Python version compatibility
python --version

# Verify Django installation
python -c "import django; print(django.get_version())"
```

## 🔧 **Quick Fix Commands**

### **Reset Everything (Nuclear Option)**

```bash
# Stop all services
docker-compose down

# Remove volumes (WARNING: This deletes all data)
docker-compose down -v

# Rebuild and restart
docker-compose up --build -d
```

### **Check Application Status**

```bash
# Check running containers
docker-compose ps

# Check logs
docker-compose logs -f app

# Check database
docker-compose exec db sqlite3 /path/to/db.sqlite3 ".tables"
```

### **Manual Database Setup**

```bash
# Connect to container
docker-compose exec app bash

# Run setup manually
python setup_db.py

# Check migrations
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser
```

## 📋 **Deployment Checklist**

### **Before Deployment**

- [ ] All migrations are committed and up to date
- [ ] Database credentials are correctly configured
- [ ] All required environment variables are set
- [ ] Dependencies are properly specified in requirements.txt

### **During Deployment**

- [ ] Monitor startup logs for errors
- [ ] Verify database connection
- [ ] Check migration status
- [ ] Confirm application is responding

### **After Deployment**

- [ ] Test all major functionality
- [ ] Verify static files are served
- [ ] Check error logs
- [ ] Monitor performance metrics

## 🆘 **Emergency Procedures**

### **If Application Won't Start**

1. Stop all services: `docker-compose down`
2. Check error logs: `docker-compose logs app`
3. Identify the specific error
4. Apply appropriate fix from above
5. Restart: `docker-compose up -d`

### **If Database is Corrupted**

1. Stop services: `docker-compose down`
2. Backup current database (if possible)
3. Reset migrations: `python reset_migrations.py`
4. Restart: `docker-compose up -d`

### **If Static Files Aren't Loading**

1. Check STATIC_ROOT and STATIC_URL settings
2. Run: `python manage.py collectstatic`
3. Verify static file permissions
4. Check web server configuration

## 📞 **Getting Help**

If you continue to experience issues:

1. **Check the logs first** - Most errors are visible in the application logs
2. **Review this guide** - Common solutions are listed above
3. **Check Django documentation** - For framework-specific issues
4. **Review deployment logs** - Look for specific error messages

## 🔍 **Debug Mode**

For detailed debugging, you can temporarily enable Django debug mode:

```python
# In settings.py
DEBUG = True

# This will show detailed error pages
# REMEMBER TO DISABLE IN PRODUCTION
```

**Remember:** Always backup your data before making significant changes to your deployment!
