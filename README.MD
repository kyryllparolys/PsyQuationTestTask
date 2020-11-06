# PsyQuation
## Running Locally
* **Virtualenv** (optional)
    * `virtualenv venv && source venv/bin/activate`
* **Install Dependencies**
    * `pip install poetry`
    * `git checkout feature/filters`
    * `poetry install`
* **Start Server**
    * Uncomment the db configuratons for local running in settings and comment out ones for docker
    * `python manage.py migrate`
    * `python manage.py runserver`

## Running in docker
* `cp .env.example .env` and fill out all the needed fields
* `docker-compose build && docker-compose up`
* If it fails, just `docker-compose up` again and it should work
