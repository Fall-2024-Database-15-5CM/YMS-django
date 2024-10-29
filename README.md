# YMS Project

This is a Yard Management System (YMS) API built with Django and Django REST Framework, integrated with a MySQL database. The API provides CRUD operations for managing users, divisions, yards, slots, structures, drivers, transactions, and maintenance data.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Django 3.2 or compatible version
- MySQL 5.7 or compatible version
- Postman (for API testing)

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/ymsproject.git
    cd ymsproject
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv ymsenv
    source ymsenv/bin/activate  # On Windows, use `ymsenv\Scripts\activate`
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Database Configuration:**

   Update `DATABASES` in `settings.py` with your MySQL database credentials. Example:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_name',
            'USER': 'your_mysql_user',
            'PASSWORD': 'your_mysql_password',
            'HOST': 'host', 
            'PORT': 'your_port',
        }
    }
    ```

5. **Run Migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Create a superuser (for Django admin):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the server:**

    ```bash
    python manage.py runserver
    ```

   Your server will start at `http://127.0.0.1:8000`.

## API Endpoints

The YMS API includes endpoints for managing users, divisions, yards, and more. Below are some key endpoints:

- **Get Users** - `GET /api/users/`
- **Create User** - `POST /api/users/`
- **Get Divisions** - `GET /api/divisions/`
- **Create Division** - `POST /api/divisions/`

### Example: User Creation

To create a new user, send a `POST` request to `/api/users/` with the following JSON payload:

```json
{
    "username": "dami",
    "password_hash": "hashed_password",
    "phone": "123-456-7890",
    "authority": {
        "division_id": "D001",
        "yard_id": "Y001",
        "yard_name": "Main Yard"
    }
}
```

## Testing with Postman

Open Postman and set up a new request.  
Select POST as the HTTP method.  
Enter http://127.0.0.1:8000/api/users/ as the request URL.  
Go to the Body tab, choose raw, and select JSON as the data format.  
Paste the JSON payload shown above and send the request.  
If the setup is correct, you should receive a response with status 201 Created and the data of the newly created user.


## Verifying Data in MySQL  
To verify that the data has been saved in the MySQL database:  
  
1. Connect to the MySQL database:  
```bash
mysql -u your_mysql_user -p
```

2. Select the database:  
```sql
USE yms_renual;
```

3. View the contents of the api_user table:
```sql
SELECT * FROM api_user;
```
This will display all users stored in the api_user table, including the one just created via the API.  

## License  
This project is licensed under the MIT License - see the LICENSE file for details.  
