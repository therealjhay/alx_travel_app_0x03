alx_travel_app_0x00
A Django RESTful API for travel property listings, bookings, and reviews.
Includes MySQL database integration, environment variable support, Swagger API docs, and a database seeder.

Features
List travel properties with price, description, and location

Create and view bookings for listings

Leave reviews and ratings for listings

MySQL database configuration via .env

Swagger API docs at /swagger/

Sequelize-like database seeding with a single command

CORS enabled for local frontend development

Getting Started
1. Clone the Repository
bash
git clone https://github.com/yourusername/alx_travel_app_0x00.git
cd alx_travel_app_0x00
2. Create & Activate Virtual Environment
bash
python -m venv venv
source venv/Scripts/activate      # Or venv/bin/activate on Mac/Linux
3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory:

text
SECRET_KEY=your_secret_key_here
DEBUG=True
MYSQL_DATABASE=your_database_name
MYSQL_USER=your_database_user
MYSQL_PASSWORD=your_database_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
5. Apply Migrations
bash
python manage.py makemigrations
python manage.py migrate
6. Seed the Database
Populate with sample listings:

bash
python manage.py seed
7. Run Development Server
bash
python manage.py runserver
API Docs: http://127.0.0.1:8000/swagger/

Sample Endpoint: http://127.0.0.1:8000/api/example/

Project Structure
text
alx_travel_app_0x00/
├── alx_travel_app/
│   ├── settings.py
│   └── urls.py
├── listings/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── management/
│       └── commands/
│           └── seed.py
├── requirements.txt
├── .env
└── manage.py
Models
Listing: title, description, location, price

Booking: listing (FK), guest_name, guest_email, check_in, check_out

Review: listing (FK), reviewer_name, rating, comment

Seeding
To seed the database with sample listings, run:

bash
python manage.py seed
