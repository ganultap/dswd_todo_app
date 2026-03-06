# Django Todo App

This project implements the March 6, 2026 hands-on exam rubric from the provided PDF using Django.

## Included features

- User registration, login, and logout
- Protected todo routes
- Per-user todo CRUD with ownership checks
- Flash notifications for success and error states
- Responsive interface with consistent styling

## Setup

1. Create and activate a virtual environment:
   `python3 -m venv .venv`
   `source .venv/bin/activate`
2. Install dependencies:
   `pip install -r requirements.txt`
3. Run migrations:
   `python manage.py migrate`
4. Start the development server:
   `python manage.py runserver`

Open `http://127.0.0.1:8000/`.

## Run tests

`python manage.py test`
