
# Personalized News Recommendation System Backend

## Overview
This project is a Django REST Framework (DRF) backend for a personalized news recommendation system. It provides APIs for managing users, articles, user preferences, and recommendations.

## Installation
1. Clone the repository:
   ```
   https://github.com/shahpankaj123/Personalized-News-Recommendation-System-Backend
   ```

2. Navigate to the project directory:
   ```
   cd Personalized-News-Recommendation-System-Backend
   ```

3. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

5. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

6. Apply migrations:
   ```
   python manage.py migrate
   ```

7. (Optional) Load initial data (e.g., sample articles):
   ```
   python manage.py loaddata sample_data.json
   ```

8. Run the development server:
   ```
   python manage.py runserver
   ```

## Configuration
- **Database**: We used MySQL Database.
- **Settings**: Update `settings.py` as per your requirements (e.g., security settings, allowed hosts, etc.).

## Contributing
Contributions are welcome! Feel free to open issues or pull requests for any improvements, bug fixes, or new features.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```

Feel free to customize it according to your specific project's needs.
