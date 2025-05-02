# Django Blog Project

A full-featured blog application built with Django that includes CRUD operations, image uploads, and related posts functionality.

## Features

- Create, Read, Update, and Delete blog posts
- Image upload support
- Responsive design with Bootstrap
- Related posts section
- Pagination
- Clean and modern UI

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Access the admin interface at `http://127.0.0.1:8000/admin/`

## Usage

- Home page: View all blog posts
- Click "New Post" to create a new blog post
- Click "Read More" to view full post details
- Edit and Delete options are available for each post
- Related posts are shown at the bottom of each post detail page

## Project Structure

- `blog/` - Main application directory
  - `models.py` - Database models
  - `views.py` - View functions and classes
  - `urls.py` - URL routing
  - `templates/` - HTML templates
- `blog_project/` - Project configuration
- `media/` - Uploaded media files 