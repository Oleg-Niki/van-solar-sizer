# Van Solar & Battery Sizing Calculator

A serverless web app that helps vanlifers size their solar panels and battery bank based on appliance loads and site-specific solar data.

---

## 📋 Overview

This project combines:

- **Python & AWS Lambda** for backend “fetch + calculate” logic  
- **NREL PVWatts API** (or OpenWeatherMap Solar) for real solar-resource data  
- **Django** for a clean web GUI  
- **sqlite3** for lightweight persistence  

Users enter their location, panel specs, battery specs, and daily appliance usage. The app returns recommended PV wattage and battery amp‐hours, plus load vs. generation charts.

---

## ⚙️ Architecture

1. **Django frontend**  
   - HTML form for inputs  
   - Results page with tables & charts (e.g. Chart.js)  
2. **AWS Lambda functions** (deployed via AWS SAM or Serverless Framework)  
   - `fetch_irradiance`: calls PVWatts (or OWM) → average sun-hours/day  
   - `calc_load`: computes total Wh/day from appliance list  
   - `size_system`: returns array W and battery Ah recommendations  
3. **sqlite3 database**  
   - Tables: `users`, `systems`, `calculations`  

---

## 🛠️ Prerequisites

- Python 3.9+  
- pip (or poetry)  
- AWS account with IAM rights for Lambda, API Gateway, and (optionally) SNS  
- NREL PVWatts API key (free from https://developer.nrel.gov/signup/)  
- (Optional) OpenWeatherMap API key if using their Solar resource endpoint  
- Git & GitHub account  

---

## 🚀 Step-by-Step Setup

### 1. Clone the repo  
```bash
$git clone https://github.com/<your-username>/van-solar-sizer.git
$cd van-solar-sizer
```

### 2. Create & activate a virtual environment
```bash
$python3 -m venv .venv
$source .venv/bin/activate     # macOS/Linux
$.\.venv\Scripts\activate      # Windows PowerShell
```

### 3. Install Python dependencies
```bash
$pip install -r requirements.txt
```

### 4. Configure environment variables
Create a .env file in the project root with your keys:
```bash
$AWS_ACCESS_KEY_ID=YOUR_AWS_KEY
$AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET
$PVWATTS_API_KEY=YOUR_NREL_KEY
$DJANGO_SECRET_KEY=some-random-string
```
### 5. Initialize sqlite3 database
```bash
python manage.py migrate
```
### 6. Define AWS Lambda functions
fetch_irradiance.py

Reads lat, lon from event → calls PVWatts API → returns sun_hours

calc_load.py

Reads appliances list (each with watts & hours) → sums Wh/day

size_system.py

Inputs: sun_hours, daily_load_wh, panel_eff=0.8, bat_v=12, dod=0.5

Outputs:
```bash
panel_w = ceil(daily_load_wh / (sun_hours * panel_eff))

battery_ah = ceil((daily_load_wh / bat_v) / dod)
```
Deploy each with AWS SAM or Serverless Framework; expose via API Gateway.

### 7. Wire up Django views
Forms → collect: location, panel spec, battery spec, appliance list

On submit → call your Lambda endpoints (via boto3 or HTTPS)

Store request & response in sqlite3

Render results + chart (e.g. with Chart.js or Plotly)

### 🎯 Running Locally
1. Start Django dev server:
```bash
python manage.py runserver
```
In another terminal, you can test Lambda functions locally (if using SAM):
```bash
sam local invoke fetchIrradianceFunction --event tests/irradiance_event.json
```
### 📂 Project Structure
```bash
van-solar-sizer/
├── aws/                        # Lambda function code & SAM templates
│   ├── fetch_irradiance.py
│   ├── calc_load.py
│   ├── size_system.py
│   └── template.yaml
├── calculator/                 # Django project
│   ├── calculator/            # settings.py, urls.py
│   ├── sizing/                # app for forms & views
│   └── manage.py
├── requirements.txt
├── README.md
└── .env.example
```
### 📈 Deployment
Lambda & API Gateway:
```bash
cd aws
sam deploy --guided
```
Django:

Host on Heroku, AWS Elastic Beanstalk, or any VPS

Ensure .env variables are set in production

### 🤝 Contribution
Feel free to open issues or PRs—feature requests like “autonomy days” or “email alerts” are welcome!

### 📜 License
This project is MIT-licensed. See LICENSE for details.# van-solar-sizer
