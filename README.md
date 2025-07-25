## Project Overview:

**Internship Support Tool** is a web-based platform designed to help university students—especially those in technical fields—stay organized and motivated during the internship application process. The platform combines two key features:

- **Watchlist Notifications** – Students can track specific companies and receive alerts when new internship opportunities are posted.
- **Motivational Tools** – Check-ins, reminders, and gamified elements like streaks and badges encourage consistent progress.

This tool aims to reduce the stress of internship hunting by centralizing opportunity tracking, boosting accountability, and supporting students' long-term career growth.

## Directory Structure:

```
AspireLink
├─ Dockerfile
├─ README.md
├─ app
│  ├─ api.py
│  ├─ auth.py
│  ├─ db.py
│  ├─ main.py
│  ├─ models.py
│  ├─ schema.py
│  ├─ static
│  │  └─ styles
│  │     └─ base.css
│  └─ templates
│     ├─ base.html
│     ├─ dashboard.html
│     ├─ display_watchlist.html
│     ├─ index.html
│     ├─ internship.html
│     ├─ login.html
│     ├─ profile.html
│     └─ register.html
├─ docker-compose.yml
├─ requirements.txt
├─ scripts
│  ├─ fetch_internships.py
│  └─ init_database.py
└─ tests
   ├─ conftest.py
   └─ test_reg.py

```

## Basic Setup:

### Clone the repository

```bash
git clone https://github.com/siaslas98/AspireLink.git
cd AspireLink
```

### Setup Environment Variables

- Create a `.env` file in the root of the repository and add the following line:
  `DATABASE_URL=postgresql://myuser:mypassword@db:5432/aspirelink_db`
  **Note: this runs with docker, no need to install PostgreSQL separately**

### Run the app using Docker

- Make sure Docker is installed and running on your machine. Then run:
  ```bash
  docker compose up --build
  ```
  - This will:
    - Start the FastAPI app on http://localhost:8001
    - Start a PostgreSQL database
    - Mount code for live reloading

### Initialize the database

In another terminal:

```bash
docker exec -it aspirelink-web-1 python scripts/init_database.py
```

## Some Important Commands:

- Access the database

  ```bash
  docker exec -it aspirelink-db-1 psql -U myuser -d aspirelink_db
  ```

- After accessing database, clear all entries in the users and watchlist table and reset id to 0
  ```
  TRUNCATE watchlist_items, users CASCADE;
  ```
- Run tests

  ```
  docker exec -it aspirelink-web-1 pytest -v tests/
  ```
