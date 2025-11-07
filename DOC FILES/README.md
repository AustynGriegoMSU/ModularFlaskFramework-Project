# Simple Flask App

A basic Flask application that displays "Hello World". (FOR NOW)

## Setup
1. Setup Virtual Enviroment
   ```
   python -m venv .venv
   source .venv/bin/activate
   $env:FLASK_APP = "src.app" 
   ```

2. Install Flask/Dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   flask run
   ```

4. Open your browser and go to: http://127.0.0.1:5000

## Files

- `__init__.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `README.md` - This file