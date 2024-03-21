# Flask REST APIs for Store Management

This repository contains a Flask application that provides RESTful APIs to manage stores, items, tags, and user authentication. The project is structured to facilitate easy development and extension of its core functionalities.

## Features

- **User Registration and Authentication**: Secure user creation and authentication using JWT tokens.
- **Store Management**: CRUD operations for managing stores.
- **Item Management**: CRUD operations for managing items within stores.
- **Tag Management**: CRUD operations for tagging items for better organization and searchability.
- **Email Notifications**: Background task processing for sending email notifications using Redis Queue (RQ).

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Redis server (for RQ background tasks)

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/amnotme/rest-apis-flask.git
    ```

2. Navigate into the project directory:
    ```bash
   cd rest-apis-flask
    ```

3. Install dependencies using Pipenv (or pip, and create a virtual environment if necessary):

    ```bash
    pipenv install
    ```
    or
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables by copying the `.env.example` to `.env` and modifying it with your settings:
    
    ```bash
    cp .env.example .env
    ```
5. (If applicable) Run database migrations:

    ```bash
    flask db upgrade
    
    ```
### Running the application

* Activate the virtual environment (if using Pipenv):
    ```bash
    pipenv shell
    ```
* Start the Flask Application
    ```bash
    flask run
    ```

### API Endpoints

The following sections describe the available CRUD operations for each resource. Replace `:id` with the actual ID of the resource.

**User Management**

* Register a new user: `POST /register `
  * Body: `{ "username": "user1", "password": "pass", "email": "user1@example.com" }`
* User login: `POST /login `
  * Body: `{ "username": "user1", "password": "pass" }`
* User logout: `POST /logout `
  * Requires valid JWT token.

**Store Management**

* Create a store: `POST /store`
  * Body: `{ "name": "My Store" }`
  * Requires authentication.
* Get a store: `GET /store/:id`
* Update a store: `PUT /store/:id`
  * Body:` { "name": "New Store Name" }`
  * Requires authentication.
* Delete a store:` DELETE /store/:id`
  * Requires authentication.
* List all stores: `GET /stores`

**Item Management**

* Create an item: `POST /item`
  * Body: `{ "name": "My Item", "price": 19.99, "store_id": 1 }`
  * Requires authentication.
* Get an item: `GET /item/:id`
* Update an item: `PUT /item/:id`
  * Body: `{ "name": "New Item Name", "price": 29.99 }`
  * Requires authentication.
* Delete an item: `DELETE /item/:id`
  * Requires authentication.
* List all items: `GET /items`

**Tag Management**

* Add a tag to an item: `POST /tag`
  * Body: `{ "name": "electronics", "item_ids": [1, 2, 3] }`
  * Requires authentication.
* Get all tags for an item: `GET /tags/item/:item_id`
* Update a tag: `PUT /tag/:id`
  * Body: `{ "name": "updated tag" }`
  * Requires authentication.
* Delete a tag: `DELETE /tag/:id`
  * Requires authentication.