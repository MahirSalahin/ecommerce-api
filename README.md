# E-commerce API

This is an E-commerce API built with Django and Django Rest Framework. It provides endpoints for managing products, collections, carts, and reviews. 
## Features

- **Products**: Manage products with CRUD operations.
- **Collections**: Group products into collections.
- **Carts**: Handle shopping carts and cart items.
- **Reviews**: Allow customers to review products.
- **Debug Toolbar**: Integrated Django Debug Toolbar for debugging.

## Project Structure

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/mahirsalahin/e-commerce-api.git
    cd e-commerce-api
    ```

2. **Install dependencies**:
    ```sh
    poetry install
    ```

3. **Set up environment variables**:
    Create a `.env` file in the root directory and add the following:
    ```env
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=your_database_name
    DB_USER=your_database_user
    DB_PASSWORD=your_database_password
    DB_HOST=localhost
    DB_PORT=port
    ```

4. **Apply migrations**:
    ```sh
    python manage.py migrate
    ```

5. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Usage

### API Endpoints

- **Products**: `/store/products/`
- **Collections**: `/store/collections/`
- **Carts**: `/store/carts/`
- **Reviews**: `/store/products/{product_id}/reviews/`

### Admin Panel

Access the admin panel at `/admin/`.


### Populate the DataBase
```sh
python manage.py generate_fake_data
