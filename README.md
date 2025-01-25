# README

## Job Analytics API

### Overview
This project is a Django Rest Framework (DRF) application designed to provide analytics on job roles sourced from various locations. It processes job data from a CSV file and allows users to:

1. Identify job role distribution by location (city and state).
2. Identify job role distribution per state.
3. Cluster job roles based on a 50-mile radius.


### Endpoints
| Endpoint                              | Method | Description                                          |
|---------------------------------------|--------|------------------------------------------------------|
| `/api/analytics/roles-distribution/`  | GET    | Job role distribution by city and state             |
| `/api/analytics/roles-per-state/`     | GET    | Job role distribution per state                     |
| `/api/analytics/roles-cluster/`       | GET    | Cluster job roles by location (50-mile radius)      |

### Prerequisites
- Python 3.8+
- Django 4.x
- Django Rest Framework
- Pandas
- Geopy

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/job-analytics-api.git
   cd job-analytics-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Load CSV data:
   - Place your CSV file (e.g., `interview_test.csv`) in the project directory.
   - Run the custom management command:
     ```bash
     python manage.py load_job_data
     ```

6. Start the server:
   ```bash
   python manage.py runserver
   ```

### Testing the API
Use Postman or a browser to test the endpoints. For example:
- `http://127.0.0.1:8000/api/analytics/roles-distribution/`

### Example Response
**Roles Distribution by Location**:
```json
[
    {
        "role": "RN",
        "location": "Austin, Dallas, Houston, and 5 more cities, Texas",
        "job_count": 12,
        "population": 800000
    },
    {
        "role": "LPN",
        "location": "Orlando, Gotha, Maitland, and 3 more cities, Florida",
        "job_count": 8,
        "population": 450000
    }
]
```



