# FreeWriter

A Django-based web application for managing and sharing PDF books and eBooks. FreeWriter serves as a search engine for PDF files, allowing users to browse, search, and download books across various categories.

## Features

- **User Authentication**: Register, login, and logout functionality with modern, beautiful UI
- **Book Management**: Upload, categorize, and manage books with cover images and PDF files
- **Search Functionality**: Search books by title
- **Category System**: Organize books by genres and categories
- **Responsive Design**: Bootstrap 5-based modern UI with custom authentication styling
- **File Handling**: Support for image uploads (covers) and PDF files
- **Beautiful Admin Interface**: Jazzmin-powered Django admin with modern UI
- **Production Ready**: Gunicorn and WhiteNoise for production deployment

## Technology Stack

- **Backend**: Django 3.2.23
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite3
- **Python Version**: 3.10 (recommended), 3.8-3.10 supported
- **Image Processing**: Pillow 10.1.0
- **Admin Interface**: Django Jazzmin 2.6.0
- **Production Server**: Gunicorn 21.2.0
- **Static Files**: WhiteNoise 6.6.0

## Installation

### Option 1: Docker (Recommended)

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd FreeWriter
   ```

2. **Build the Docker image:**

   ```bash
   docker build -t freewriter .
   ```

3. **Run the container:**

   ```bash
   docker run -p 8000:8000 -v $(pwd)/media:/app/media freewriter
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

### Option 2: Local Development

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd FreeWriter
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   # For production (exact versions)
   pip install -r requirements.txt
   ```

4. **Run migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional):**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

7. **Open your browser and navigate to `http://127.0.0.1:8000/`**

## Project Structure

```
FreeWriter/
├── bookapp/                 # Main Django application
│   ├── models.py           # Database models (Book, Category, BookSearch)
│   ├── views.py            # View functions and logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # URL routing
│   └── templates/          # HTML templates
├── FreeWriter/             # Django project settings
│   ├── settings.py         # Project configuration
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI application entry point
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files (PDFs, images)
├── templates/              # Base templates
└── manage.py               # Django management script
```

## Usage

- **Home Page**: View recommended, fiction, and business books
- **Books**: Browse all available books
- **Search**: Search for specific books by title
- **Categories**: Filter books by genre/category
- **User Account**: Register/login to access additional features
- **Admin Panel**: Access the beautiful Jazzmin admin interface at `/admin/`
  - Username: `admin`
  - Password: `f001`

## Loading Sample Data

To get started with books from your existing media folder, run:

```bash
# If using Docker
docker exec -it <container_name> python manage.py create_books_from_images

# If running locally
python manage.py create_books_from_images
```

This will create:

- Books based on images in your `media/img/` folder
- Proper titles, authors, and summaries for each book
- Automatic categorization (Fiction, Business, Science, Technology, Self-Help)
- Real book covers instead of dummy images
- **PDF files** from your `media/pdf/` folder when available
- **Welib.org links** as fallback when PDF files are not found

## Automatic Setup

When using Docker, the container automatically:

- Runs database migrations
- Creates a superuser with credentials:
  - **Username**: `admin`
  - **Password**: `f001`
- Creates books from existing images in your media folder (if no books exist)
- Fixes missing images and PDFs for existing books (prevents duplicates)
- Adds Welib.org search links as fallback for missing PDFs
- Starts the Gunicorn server

You can access the admin panel at `/admin/` using these credentials.

## Troubleshooting

### Images Not Displaying

If images are not showing on the website:

1. **Check Media Files**: Ensure the `media/` directory has proper read permissions
2. **Verify File Permissions**: Ensure the `media/` directory has proper read permissions
3. **Check Database**: Verify that books have cover_image fields populated
4. **Django Settings**: Confirm `MEDIA_URL` and `MEDIA_ROOT` are properly configured

### Common Issues

- **No Books Showing**: Books are automatically created from your media folder when using Docker
- **Broken Images**: Images are automatically fixed and linked when using Docker
- **Missing PDFs**: PDFs are automatically assigned and Welib.org links added when using Docker
- **Template Errors**: Check that all templates extend `base.html`
- **Static Files**: Run `python manage.py collectstatic` if needed
- **Database Errors**: If you see 'pdf_url' column errors, ensure migrations are run: `python manage.py migrate`

**Note**: For local development, you may need to run these commands manually:

- `python manage.py create_books_from_images`
- `python manage.py fix_images`
- `python manage.py fix_pdfs`

## Docker Support

The application is containerized with a single Dockerfile using Gunicorn for both development and production.

### Docker Commands

```bash
# Build the image
docker build -t freewriter .

# Run the container
docker run -p 8000:8000 -v $(pwd)/media:/app/media freewriter

# Run in background
docker run -d -p 8000:8000 -v $(pwd)/media:/app/media --name freewriter-app freewriter

# Stop the container
docker stop freewriter-app

# Remove the container
docker rm freewriter-app
```

### Remote Server Deployment

For deploying on a remote server:

1. **Upload your project** to the server
2. **Run the deployment script:**

   ```bash
   chmod +x deploy.sh
   ./deploy.sh
   ```

3. **Or deploy manually:**

   ```bash
   # Build and run in production mode
   docker build -t freewriter .
   docker run -d \
     --name freewriter-app \
     -p 8000:8000 \
     -v $(pwd)/media:/app/media \
     -e DEBUG=False \
     --restart unless-stopped \
     freewriter
   ```

4. **Check the application:**

   ```bash
   # View logs
   docker logs freewriter-app
   
   # Check status
   docker ps
   ```

## Troubleshooting

### Common Installation Issues

1. **Docker build errors**: Ensure Docker is properly installed and running
2. **Pillow installation errors**: Try using Python 3.9.18 for best compatibility
3. **Version conflicts**: Use `requirements.txt` for dependencies
4. **Python version**: Python 3.10 is recommended for best compatibility

### Alternative Solutions

- Use Python 3.9.18 for best compatibility
- Use Docker to avoid environment issues

## Contributing

This project was created in 2021 by George Klenam. Contributions are welcome!

## License

© George Klenam @2021

---

**Note**: FreeWriter is your #1 search engine for PDF files. We have eBooks for you to download for free. No annoying ads, no download limits, enjoy it and don't forget to share the love!