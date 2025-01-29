# Travel Planner
A simple Django REST Framework (DRF) project designed to create and manage travel plans. This project serves as an example of building RESTful APIs with Django and is part of a Python backend development course.

### Features
- **User Management**: Create, retrieve, update, and delete users, including bio validation.
- **Travel Plans**: Manage travel plans with associated destinations and activities.
- **Activities**: Create and manage activities linked to travel plans.
- **Destinations**: Add destinations, with automated country determination for landmarks.
- **Comments**: Add comments to travel plans, destinations, or activities.
- **Authentication**: Token-based user authentication, including login and logout functionality.

### Requirements

*see requirements.txt file*

### Installation
1. Clone the repository:

    ```bash
    git clone <repository_url>
    cd travel-planner
    ```
2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Set up a PostgreSQL database. The database configuration should be defined in a .env file (not included in the repository). Ensure it contains the following keys:

    ```makefile
    DATABASE_NAME=<your_database_name>
    DATABASE_USER=<your_database_user>
    DATABASE_PASSWORD=<your_database_password>
    DATABASE_HOST=<your_database_host>
    DATABASE_PORT=<your_database_port>
    ```
4. Apply migrations:

    ```bash
    python manage.py migrate
    ```
5. Start the development server:

    ```bash
    python manage.py runserver
    ```
### API Endpoints
**Users**
- **GET** `/users/`: Retrieve all users.
- **POST** `/users/`: Create a new user.
- **GET** `/users/<id>/`: Retrieve a specific user.
- **PUT** `/users/<id>/`: Update a user.
- **DELETE** `/users/<id>/`: Delete a user.

**Travel Plans**
- **GET** `/travel-plans/`: Retrieve all travel plans.
- **POST** `/travel-plans/`: Create a new travel plan.
- **GET** `/travel-plans/<id>/`: Retrieve a specific travel plan.
- **PUT** `/travel-plans/<id>/`: Update a travel plan.
- **DELETE** `/travel-plans/<id>/`: Delete a travel plan.

**Activities**
- **GET** `/activities/`: Retrieve all activities.
- **POST** `/activities/`: Create a new activity.
- **GET** `/activities/<id>/`: Retrieve a specific activity.
- **PUT** `/activities/<id>/`: Update an activity.
- **DELETE** `/activities/<id>/`: Delete an activity.

**Destinations**
- **GET** `/destinations/`: Retrieve all destinations.
- **POST** `/destinations/`: Create a new destination (country auto-detected).
- **GET** `/destinations/<id>/`: Retrieve a specific destination.
- **PUT** `/destinations/<id>/`: Update a destination.
- **DELETE** `/destinations/<id>/`: Delete a destination.

**Comments**
- **GET** `/comments/`: Retrieve all comments.
- **POST** `/comments/`: Add a new comment.
- **GET** `/comments/<id>/`: Retrieve a specific comment.
- **PUT** `/comments/<id>/`: Update a comment.
- **DELETE** `/comments/<id>/`: Delete a comment.

**Authentication**
- **POST** `/login/`: Log in and retrieve an authentication token.
- **POST** `/logout/`: Log out and invalidate the token.

### Deployment
This project uses a PostgreSQL database. Configuration details are hidden in a .env file, which is not included in the repository. Ensure proper environment setup before deploying the project locally.

### Disclaimer
This project is for educational purposes only. It is not intended for production use and does not include a license. Contributions are not accepted.
