Age Guesser API

The Age Guesser API is a Django-based application that estimates a person's age based on their name by leveraging the Agify.io API. It also computes and returns an estimated year of birth.

Features

Age estimation based on name
Caching of requests to optimize API usage and improve response times
Docker support for easy deployment


Prerequisites
Before you begin, ensure you have met the following requirements:

Python 3.9 or later
Docker and Docker Compose (for containerization and deployment)
Setting Up for Development

Clone the repository:
git clone https://github.com/dunmininu/agify-project.git
cd agify_project

Create and activate a virtual environment:
For Unix-based systems:
python3 -m venv venv
source venv/bin/activate

For Windows:
python -m venv venv
.\venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run migrations:
python manage.py migrate

Start the development server:
python manage.py runserver

The API will be available at http://localhost:8000/api/human-age.

Testing

To run the tests, use the following command:
pytest

Ensure all tests pass before moving on to deployment or making changes to the application.

Docker Deployment
This project includes Docker support for easy deployment. Follow these steps to containerize the application.

Build the Docker image:
docker-compose build

Run the application:
docker-compose up

This command starts the application and a PostgreSQL database as specified in docker-compose.yml. The application will be accessible on http://localhost:8000/api/human-age.

Using the API
To guess an age, send a POST request to the /api/human-age endpoint with a JSON payload containing the name. For example:
curl -X POST http://localhost:8000/api/human-age -H "Content-Type: application/json" -d '{"name": "michael"}'

Response:
{"name": "michael", "age": 50, "date_of_birth": "1971"}

Additional Information

Caching: The application caches responses to optimize API calls. Cached data expires after 24 hours.
Rate Limiting: Be mindful of the Agify API's rate limit of 1000 requests per day.
Contributing

Contributions to the Age Guesser API are welcome. Please follow these steps to contribute:

Fork the repository.
Create a new branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.
