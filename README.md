# Task Tracker

## Start the Backend

Run:

uvicorn app.main:app --reload --port 8000

The backend runs at:

http://localhost:8000

## Open the Frontend

Open a second terminal and run:

cd frontend
python -m http.server 5500

Then open this in the browser:

http://localhost:5500/index.html

## Run the Tests

From the project root, run:

python -m pytest -q

Expected result:

17 passed
