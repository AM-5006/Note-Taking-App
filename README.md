# Note-Taking-App

## Project Structure
The project is organized as follows:
```bash
|-- app.py
|-- apps
|   |-- Notes
|   |   |-- models.py
|   |   `-- views.py
|   `-- User
|       |-- models.py
|       `-- views.py
|-- config.py
|-- database
|   `-- database.py
`-- requirements.txt
```

* __app.py__: This is the main entry point of the Flask application.
* __apps__: This directory contains subdirectories for different modules of the application. Currently, there are two modules: Notes and User.
    * __Notes__:
        * __models.py__: Defines the data models for the Notes module.
        * __views.py__: Contains the routes for the Notes module.
    * __User__:
        * __models.py__: Defines the data models for the User module.
        * __views.py__: Contains the routes for the User module.
* __config.py__: Configuration file for the Flask application.
* __database__: This directory contains the database module.
  * __database.py__: Manages the database connection and configuration.


## Installation and Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/AM-5006/Note-Taking-App.git 
   ```
2. Navigate to the project directory:
   ```bash
   cd Note-Taking-App
   ```
3. Install the required packages using pip:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the development server:
   ```bash
   gunicorn app:app
   ```
The App should now be accessible at http://localhost:8000/

## API Documentation
#### User routes

* Retrieve Users
  - Endpoint: `/`
  - Method: GET
  - Response:
    * Success (200 OK):
      - ```json
        {
          "All Users": [
          {
            "name": "John Cena",
            "username": "johncena"
          },
          {
            "name": "Dave Batista",
            "username": "davebatista"
          }
          // ... other users
          ]
        }
        ```

* Register User
  - Endpoint: `/register`
  - Method: POST
  - Request Body:
    * ```json
      {
        "name": "John Cena",
        "username": "johncena",
        "password": "secretpassword"
      }
      ```
  - Response:
    * Success (201 Created):
      - ```json
        {
          "message": "User registered successfully"
        }
        ```
    * User Already Exists (400 Bad Request):
      - ```json
        {
          "message": "User already exists"
        }
        ```
* Login User
  - Endpoint: `/login`
  - Method: POST
  - Request Body:
    * ```json
      {
        "username": "johndoe",
        "password": "secretpassword"
      }
      ```
  - Response:
    * Success (200 OK):
      - ```json
        {
          "token": "<JWT_TOKEN>"
        }
        ```
    * Invalid Credentials (401 Unauthorized):
      - ```json
        {
          "message": "Invalid credentials"
        }
        ```

#### Notes routes
All endpoints in the Notes API require authentication through a valid JSON Web Token (JWT). Include the token in the header of your requests with the key Authorization: Bearer <JWT_TOKEN>.
__Request__:
  - Headers:
    * `Authorization: Bearer <JWT_TOKEN>`

* Create a Note
  - URL: `/notes`
  - Method: POST
  - Request Body:
    * ```json
      {
        "title": "Note Title",
        "content": "Note Content"
      }
      ```
  - Response:
    * Success (201 Created):
      ```json
      {
        "message": "Note created successfully"
      }
      ```
* Get User's Notes
  - URL: `/notes`
  - Method: GET
  - Response:
    * Success (200 OK):
      - ```json
        {
          "notes": [
            {
              "title": "Note 1",
              "content": "Content of Note 1"
            },
            {
              "title": "Note 2",
              "content": "Content of Note 2"
            }
            // ... other notes
          ]
        }
        ```
    * No Notes Found (200 OK):
      - ```json
        {
          "message": "No notes found"
        }
        ```

* Delete a Note
  - URL: `/notes/<note_id>`
  - Method: DELETE
  - Response:
    * Success (200 OK):
      - ```json
        {
          "message": "Note deleted successfully"
        }
        ```
    * Note Not Found (404 Not Found):
      - ```json
        {
          "message": "Note not found"
        }
        ```
* Update a Note
  - URL: `/notes/<note_id>`
  - Method: PATCH
  - Request Body:
    * ```json
      {
        "title": "Updated Note Title",
        "content": "Updated Note Content"
      }
      ```
  - Response:
    * Success (200 OK):
      - ```json
        {
          "title": "Updated Note Title",
          "content": "Updated Note Content"
        }
        ```
    * No Fields to Update (400 Bad Request):
      - ```json
        {
          "message": "No fields to update"
        }
        ```
    * Note Not Found (404 Not Found):json
      - ```
        {
          "message": "Note not found"
        }
        ```

#### Error Responses
* Token Missing (401 Unauthorized):
  - ```json
    {
      "message": "Token is missing"
    }
    ```
* Token Expired (401 Unauthorized):
  - ```json
    {
      "message": "Token has expired"
    }
    ```
* Invalid Token (401 Unauthorized):
  - ```json
    {
      "message": "Invalid token"
    }
    ```

## Contributing
If you would like to contribute to the project, please follow these steps:

1. Fork the repository on GitHub.
2. Clone your forked repository to your local machine.
3. Create a new branch for your feature or bug fix.
4. Make your changes and commit them with clear commit messages.
5. Push your changes to your fork on GitHub.
6. Create a pull request to the original repository.

## License
This project is licensed under the MIT License. See the `LICENSE.txt` file for more details.
