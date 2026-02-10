# 🚐 Traffiki: Fleet Command Center

**Traffiki** is a Full-Stack Fleet Management System designed for high-volume Matatu Saccos. It simulates the lifecycle of public transport assets, tracking vehicles from "Active" duty to "Unroadworthy" status, and enforces operational workflows for repair budgeting.

![Tech Stack](https://img.shields.io/badge/Stack-Django%20%7C%20Angular%20%7C%20Tailwind-blue)

## 🚀 Key Features

* **Real-Time State Machine:** Tracks vehicle status (`Active`, `Unroadworthy`, `Fixed`, `Fixer-Upper`) with strict transition logic.
* **"Clean Deck" Protocol:** A frontend guardrail that prevents admins from downloading new repair budgets until all "Fixed" vehicles are deployed back to the road.
* **Automated Financial Reporting:** Server-side CSV generation that calculates repair costs based on mechanic reports.
* **Chaos Simulation:** A "Reset" button that wipes the database and generates 200+ randomized vehicle records to test system load.

## 🛠️ Technology Stack

* **Backend:** Django 5, Django REST Framework (DRF)
* **Frontend:** Angular (Standalone Components), TailwindCSS
* **Database:** SQLite (Dev), PostgreSQL (Production-ready)
* **Tools:** Git, Postman

---

## ⚙️ Setup Instructions (How to Run)

To run this project, you need **two separate terminals** active at the same time (one for Django, one for Angular).

### 1. Backend Setup (Django)
*Open Terminal #1*

```bash
# 1. Clone the repository
git clone [https://github.com/Thiani-dk/TRAFFIKI.git](https://github.com/Thiani-dk/TRAFFIKI.git)
cd TRAFFIKI

# 2. Create and activate Virtual Environment
python -m venv venv
source venv/bin/activate  # (On Windows use: venv\Scripts\activate)

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply Database Migrations
python manage.py migrate

# 5. Start the Server
python manage.py runserver
The backend will run at: http://127.0.0.1:8000/

2. Frontend Setup (Angular)
Open Terminal #2

Bash
# 1. Navigate to the frontend folder
cd traffiki-frontend

# 2. Install Node modules
npm install

# 3. Start the Angular Development Server
ng serve
The frontend will run at: http://localhost:4200/

🧪 How to Test the System
Open the Dashboard: Go to http://localhost:4200.

Run Simulation: Click the "⚡ RESET / SIMULATE" button in the top right.

What happens: The backend deletes all data and creates ~200 dummy vehicles with random statuses.

Test the "Clean Deck" Rule:

Look for vehicles with the Green "FIXED" status.

Notice the "Download Budget" button is hidden/disabled.

Click "Deploy" on all Fixed cars.

Once the garage is clear of fixed cars, the Download button appears.

Download Report: Click "Download Budget" to get the generated CSV file.

🐛 Troubleshooting / Common Issues
1. CORS Error (Frontend can't talk to Backend)

Error: Access to XMLHttpRequest at '...' has been blocked by CORS policy.

Fix: Ensure django-cors-headers is installed and CORS_ALLOW_ALL_ORIGINS = True is set in settings.py.

2. "ng" command not found

Fix: You likely need to install the Angular CLI globally:

Bash
npm install -g @angular/cli
3. Database Locked

Fix: If the simulation freezes, stop the Django server (Ctrl+C) and restart it. SQLite sometimes locks during heavy write operations.

📂 Project Structure
TRAFFIKI/
├── fleet_management/      # Django App (Business Logic)
│   ├── models.py          # Database Schemas (Vehicle, Garage)
│   ├── views.py           # API Endpoints & CSV Generator
│   └── urls.py            # API Routes
├── traffiki-frontend/     # Angular Project
│   ├── src/app/           # Components & Services
│   └── tailwind.config.js # Styling Config
├── manage.py              # Django Entry Point
└── db.sqlite3             # Local Database
Author: Daniel Katiso License: MIT
