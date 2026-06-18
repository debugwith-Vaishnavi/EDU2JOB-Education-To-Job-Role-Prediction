# Edu2Job Project Documentation

## Index

1. Overview
2. Architecture
3. Project Structure
4. Setup Instructions
5. API Endpoints
6. Database Schema
7. ML Pipeline
8. Frontend Features
9. Usage Guide
10. Dependencies
11. Configuration
12. Development
13. Notes

## Objectives

- Develop a web application that predicts job roles based on educational and professional inputs.
- Implement a machine learning pipeline to train and serve the model.
- Provide a RESTful API with authentication for secure access.
- Create a simple user-friendly frontend for interactions.
- Store prediction history for users.

## Flowchart

![Flowchart](flowchart.png)

## Overview

Edu2Job is a Django-based web application that uses machine learning to predict job roles based on user input data. It features a RandomForest classifier trained on a job role dataset, a REST API with JWT authentication, and a simple static HTML frontend.

## Architecture

- **Backend Framework**: Django (web framework)

- **Machine Learning**: Scikit-learn RandomForestClassifier

- **Database**: SQLite

- **Authentication**: JWT (djangorestframework-simplejwt)

- **Frontend**: HTML, CSS (Bootstrap), JavaScript

- **API**: Django REST Framework

## Project Structure

- `manage.py`: Django management script

- `edu2job`: Main Django project folder
  - `settings.py`: Django settings
  - `urls.py`: Main URL configuration

- `api`: Django app for API
  - `models.py`: Database models
  - `views.py`: API views
  - `serializers.py`: API serializers
  - `urls.py`: API URL patterns

- `frontend`: Static HTML files

- `artifacts`: ML model artifacts

- `train_pipeline.py`: ML training script

## Setup Instructions

### Prerequisites

- Python 3.8+

- Virtual environment tool

### Installation

1. Clone or download the project.
2. Create virtual environment:
   **Windows:**
   ```
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
   **Linux/Mac:**
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Prepare dataset:
   Place `JobRole.xlsx` in the project root (or update `DATA_PATH` in `train_pipeline.py`).
5. Train the model:
   ```
   python train_pipeline.py
   ```
6. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
7. Start the server:
   ```
   python manage.py runserver
   ```

The application will be available at http://127.0.0.1:8000/

## API Endpoints

Assuming standard DRF setup:

- `POST /api/token/`: Obtain JWT token (login)
- `POST /api/token/refresh/`: Refresh JWT token
- `POST /api/register/`: User registration
- `POST /api/predict/`: Job role prediction
- `GET /api/history/`: Prediction history
- `GET /api/profile/`: User profile

## Database Schema

- **User**: Django's built-in user model
- **PredictionHistory**: Stores prediction inputs and results
  - user (ForeignKey to User)
  - input_data (JSONField)
  - prediction (CharField)
  - created_at (DateTimeField)

## ML Pipeline

The `train_pipeline.py` script:

1. Loads the dataset from Excel
2. Preprocesses data (encoding categorical variables, handling missing values)
3. Splits data into train/test
4. Trains RandomForest model
5. Evaluates model
6. Saves model, encoder, and scaler to artifacts/
7. Generates training report

## Frontend Features

- **Login/Register**: User authentication
- **Dashboard**: Main page
- **Predict**: Form to input data for prediction
- **Result**: Display prediction result
- **History**: List of past predictions
- **Profile**: User profile management
- **Logout**: User logout

## Usage Guide

1. Register a new account or login.
2. Navigate to the Predict page.
3. Fill in the form with your educational and professional information.
4. Submit to get job role prediction.
5. View results and save to history.
6. Check history page for past predictions.

## Dependencies

From `requirements.txt` (assumed):

- Django
- djangorestframework
- djangorestframework-simplejwt
- scikit-learn
- pandas
- numpy
- openpyxl
- joblib
- matplotlib (for plots)

## Configuration

- Database: SQLite (db.sqlite3)
- Static files: Served from frontend/
- ML artifacts: Stored in artifacts/
- JWT settings: Configured in settings.py

## Development

- Run tests: `python manage.py test`
- Create superuser: `python manage.py createsuperuser`
- Admin panel: /admin/

## Notes

- The dataset path may need adjustment for local setup.
- The frontend is static, no dynamic rendering.
- API is RESTful with JWT auth.
