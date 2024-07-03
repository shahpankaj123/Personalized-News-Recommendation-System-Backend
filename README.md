---

# Personalized News Recommendation System Backend

## Overview
This project is a Django REST Framework (DRF) backend for a personalized news recommendation system. It provides APIs for managing users, articles, user preferences, and recommendations.

## Installation
Follow these steps to set up the project:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/shahpankaj123/Personalized-News-Recommendation-System-Backend
   ```

2. **Navigate to the project directory:**
   ```bash
   cd Personalized-News-Recommendation-System-Backend
   ```

3. **Create a virtual environment (optional but recommended):**
   ```bash
   python3 -m venv venv
   ```

4. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

6. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

7. **(Optional) Load initial data (e.g., sample articles):**
   ```bash
   python manage.py loaddata sample_data.json
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

## Configuration
- **Database**: This project uses MySQL. Ensure your MySQL database is set up and configured in `settings.py`.
- **Redis**: Used for caching. Ensure Redis is installed and running on your machine.
- **Celery**: Used for sending emails and task scheduling.
  - **Broker**: Redis is used as the message broker for Celery.
  - **Beat**: Celery Beat is used for scheduling tasks.

### Redis Configuration
1. Install Redis:
   - On macOS:
     ```bash
     brew install redis
     ```
   - On Linux:
     ```bash
     sudo apt-get install redis-server
     ```
   - On Windows: Follow the instructions on the [Redis website](https://redis.io/download).

2. Start Redis server:
   ```bash
   redis-server
   ```

### Celery Configuration
1. Add the following settings in your `settings.py`:

   ```python
   # Celery Configuration Options
   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   CELERY_TIMEZONE = 'UTC'
   ```

2. Start Celery worker and Beat in separate terminal windows:
   ```bash
   # Start Celery worker
   celery -A your_project_name worker --loglevel=info

   # Start Celery Beat
   celery -A your_project_name beat --loglevel=info
   ```

## Contributing
Contributions are welcome! Feel free to open issues or pull requests for any improvements, bug fixes, or new features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Authors
This project is developed and maintained by:
- [Pankaj Shah](https://github.com/shahpankaj123)
- [Sameer Maharjan](https://github.com/Starez1011)

---
