# FreeWriter

A Django-based web application for managing and sharing PDF books and eBooks. FreeWriter serves as a search engine for PDF files, allowing users to browse, search, and download books across various categories.

## Features

- **User Authentication**: Register, login, and logout functionality
- **Book Management**: Upload, categorize, and manage books with cover images and PDF files
- **Search Functionality**: Search books by title
- **Category System**: Organize books by genres and categories
- **Responsive Design**: Bootstrap 5-based modern UI
- **File Handling**: Support for image uploads (covers) and PDF files

## Technology Stack

- **Backend**: Django 3.2.23
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite3
- **Python Version**: 3.10 (recommended), 3.8-3.10 supported
- **Image Processing**: Pillow 10.1.0
- **Admin Interface**: Django Jazzmin 2.6.0

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
   docker run -p 8000:8000 -v $(pwd):/app freewriter
   ```

4. **Access the application:**
   - Open your browser and go to `http://localhost:8000`

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
- Creates books from existing images in your media folder
- Assigns PDF files when available
- Adds Welib.org search links as fallback for missing PDFs
- Starts the Django development server

You can access the admin panel at `/admin/` using these credentials.

## Troubleshooting

### Images Not Displaying

If images are not showing on the website:

1. **Check Media Files**: Visit `/book/media_test/` to verify media directory structure and file existence
2. **Verify File Permissions**: Ensure the `media/` directory has proper read permissions
3. **Check Database**: Verify that books have cover_image fields populated
4. **Django Settings**: Confirm `MEDIA_URL` and `MEDIA_ROOT` are properly configured

### Common Issues

- **No Books Showing**: Run `python manage.py create_books_from_images` to create books from your media folder
- **Broken Images**: Run `python manage.py fix_images` to fix broken image references
- **Missing PDFs**: Run `python manage.py fix_pdfs` to fix missing PDF files and add Welib.org links
- **Link Existing Images**: Run `python manage.py link_existing_images` to link real images from media folder
- **Template Errors**: Check that all templates extend `base.html` (not `templates/base.html`)
- **Static Files**: Run `python manage.py collectstatic` if using production settings

## Docker Support

The application is containerized with a simple Dockerfile for easy deployment.

### Docker Commands

```bash
# Build the image
docker build -t freewriter .

# Run the container
docker run -p 8000:8000 -v $(pwd):/app freewriter

# Run in background
docker run -d -p 8000:8000 -v $(pwd):/app --name freewriter-app freewriter

# Stop the container
docker stop freewriter-app

# Remove the container
docker rm freewriter-app
```

## Troubleshooting

### Common Installation Issues

1. **Docker build errors**: Ensure Docker is properly installed and running
2. **Pillow installation errors**: Try using Python 3.9.18 or use the simple requirements
3. **Version conflicts**: Use `requirements.txt` for dependencies
4. **Python version**: Python 3.9.18 is recommended for best compatibility

### Alternative Solutions

- Use Python 3.9.18 for best compatibility
- Use `requirements-simple.txt` for minimal setup
- Use Docker to avoid environment issues
- Check the `DEPLOYMENT.md` for detailed troubleshooting

## Contributing

This project was created in 2021 by George Klenam. Contributions are welcome!

## License

© George Klenam @2021

---

**Note**: FreeWriter is your #1 search engine for PDF files. We have eBooks for you to download for free. No annoying ads, no download limits, enjoy it and don't forget to share the love!
