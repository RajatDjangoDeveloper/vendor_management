# Vendor Management System

## Overview

This project is a Vendor Management System built with Django and Django REST Framework. It manages vendor profiles, tracks purchase orders, and calculates vendor performance metrics.

## Features

1. Vendor Profile Management
2. Purchase Order Tracking
3. Vendor Performance Evaluation

## Setup Instructions

### Prerequisites

- Python 3.x
- Django
- Django REST Framework

### Installation

1. Clone the repository:

    ```bash
    git clone <your-repo-url>
    cd vendor_management
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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

5. Create a superuser:

    ```bash
    python manage.py createsuperuser
    ```

6. Run the server:

    ```bash
    python manage.py runserver
    ```

## API Endpoints

### Vendor Profile Management

- **Create a new vendor:** `POST /api/vendors/`
- **List all vendors:** `GET /api/vendors/`
- **Retrieve a specific vendor's details:** `GET /api/vendors/{vendor_id}/`
- **Update a vendor's details:** `PUT /api/vendors/{vendor_id}/`
- **Delete a vendor:** `DELETE /api/vendors/{vendor_id}/`

### Purchase Order Tracking

- **Create a purchase order:** `POST /api/purchase_orders/`
- **List all purchase orders:** `GET /api/purchase_orders/`
- **Retrieve details of a specific purchase order:** `GET /api/purchase_orders/{po_id}/`
- **Update a purchase order:** `PUT /api/purchase_orders/{po_id}/`
- **Delete a purchase order:** `DELETE /api/purchase_orders/{po_id}/`
- **Acknowledge a purchase order:** `POST /api/purchase_orders/{po_id}/acknowledge/`

### Vendor Performance Evaluation

- **Retrieve a vendor's performance metrics:** `GET /api/vendors/{vendor_id}/performance/`

## Running Tests

To run the test suite, use the following command:

```bash
python manage.py test


**loom videos **

1  -https://www.loom.com/share/62aa77f2dea349d488c758b65c46b89e?sid=d4e66833-a87d-4138-993d-cb403ec3d288
2 - https://www.loom.com/share/f5e07fcf0a0f4af4a042851e11c56319?sid=8ea436c7-e8ba-486d-b59f-a6d0f82b6a2f
