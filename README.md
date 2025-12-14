Instagram Clone - Django Backend

This project is a mini-clone of Instagram, built primarily using the **Django** framework. It implements core social media features including user authentication, a follow system, post creation with image uploads and caption, and dynamic user interactions(likes and comments).

The application uses a modern, responsive UI designed with pure CSS and HTML, linked via Django templates.

Follow these steps to get the project running on your local machine.
Install the following packages in virtual environment of BASE Directory:
asgiref==3.11.0
Django==6.0
pillow==12.0.0
sqlparse==0.5.4
tzdata==2025.3

Clone the project to your local machine:
git clone <Your_GitHub_Repository_URL>
cd <Your_Project_Directory_Name>

Run these Commands for Database Migrations
python manage.py makemigrations
python manage.py migrate

Create a Superuser:
python manage.py createsuperuser

Run the Development Server:
python manage.py runserver
