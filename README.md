# Citizen Grievance Management Portal (CGMP)

A full-stack web application for managing civic complaints and grievances between citizens and government authorities.

## Features

### For Citizens
- User registration and login
- Submit complaints with title, description, category, and location
- GPS/Map-based location tagging
- Track complaint status in real-time
- Provide feedback and ratings after resolution

### For Government Officials
- View assigned complaints
- Update complaint status (Under Review, Assigned, In Progress, Resolved)
- Add remarks and updates

### For Administrators
- Manage departments and officials
- Assign complaints to appropriate departments/officials
- Monitor complaint progress
- Generate reports and analytics

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Maps**: Leaflet.js for map integration

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser and navigate to: `http://localhost:5000`

## Default Admin Credentials

- Email: `admin@cgmp.gov`
- Password: `admin123`

## Project Structure

```
CGMP/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
└── templates/
    ├── index.html         # Landing page
    ├── login.html         # Login page
    ├── register.html      # Registration page
    ├── citizen_dashboard.html
    ├── submit_complaint.html
    ├── track_complaint.html
    ├── feedback.html
    ├── official_dashboard.html
    ├── update_complaint.html
    ├── admin_dashboard.html
    ├── assign_complaint.html
    ├── manage_officials.html
    └── reports.html
```

## Complaint Status Flow

1. Submitted → 2. Under Review → 3. Assigned → 4. In Progress → 5. Resolved

## Categories

- Road & Infrastructure
- Water Supply
- Electricity
- Waste Management
- Public Safety
- Other Civic Issues

## License

MIT License
