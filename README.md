# DayMinder

## Overview

**DayMinder** is a task and event management web application designed to help users efficiently organize their schedules. The application allows users to add, edit, and delete tasks or events, receive reminder notifications, and track their task completion.

## Features

- **Task/Event Management:** Manage your schedule with ease.
- **Reminder Notifications:** Stay on top of your tasks with timely reminders.
- **Task Completion Tracking:** Monitor progress by marking tasks as completed or cancelled.
- **Daily Schedule Input:** Get reminders to plan for the next day.
- **Google Calendar Integration:** Sync tasks with Google Calendar.

## For Users

### Getting Started

1. **Visit the Official Website:** [DayMinder](http://yourdomain.com)
2. **Sign Up or Log In:** Create an account or log in to start managing your tasks. You may use the app without signing up, but there would be limitations.
3. **Using DayMinder:**
   - **Dashboard:** View and manage your tasks and events.
   - **Settings:** Customize notification preferences and account settings.
   - **Help:** Access our help section for FAQs and support.

### Features

- **Create Tasks/Events:** Easily add tasks or events to your schedule.
- **Set Reminders:** Customize reminder notifications based on your preferences.
- **Track Progress:** Update task status and monitor your achievements.

## For Developers

### Installation

To set up a local development environment for DayMinder:

1. **Clone the Repository**
    - ```git clone https://github.com/tech-gecko/DayMinder.git```
    - ```cd dayminder```

2. **Create a Virtual Environment**
    - ```python3 -m venv venv```
    - ```source venv/bin/activate```

3. **Install Dependencies**
    - ```pip install -r requirements.txt```

4. **Set Up the Database**
    - Create a MySQL database and configure config.py with the appropriate credentials and database settings.

5. **Run the Application Locally**
    - ```flask run```

### Deployment

To deploy DayMinder on a production server, follow these steps:

1. **Secure Your Server**
    (Configure UFW to allow Nginx and SSH):
    - ```sudo ufw allow 'Nginx Full'```
    - ```sudo ufw enable```

2. **Set Up Nginx**
    - Configure Nginx as a reverse proxy to Gunicorn.
    - Create an Nginx configuration file for your Flask app in ```/etc/nginx/sites-available/```.

3. **Set Up SSL**
    - Use Certbot to set up HTTPS: ```sudo certbot --nginx```

4. **Deploy Gunicorn**
    - Use Gunicorn to serve the Flask application: ```gunicorn --bind 0.0.0.0:8000 wsgi:app```

5. **Load Balancing (Optional)**
    - Configure HAProxy for load balancing across multiple servers if needed.

### GitHub Workflow

If you want to contribute to DayMinder, here's how to do it:

1. **Branching**
    - Start by creating a new branch for your feature or bugfix: ```git checkout -b feature/your-feature-name```
    - Once your work is done, push your branch to GitHub: ```git push origin feature/your-feature-name```

2. **Pull Requests**
    - Open a pull request against the main branch for review.

### Contributing

Contributions are welcome! Here's how you can get involved:

- **Fork the Repository**: Create your own copy of the project.
- **Create a Branch**: Work on a new feature or fix a bug.
- **Submit a Pull Request**: Propose your changes for review and inclusion.

### Contact

For any questions, suggestions, or issues, feel free to open an issue or reach out to [w0nderzz2001@gmail.com].