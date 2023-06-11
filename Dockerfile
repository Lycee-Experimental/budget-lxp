# Use a base image with Python and necessary dependencies
FROM python:3.11-slim-buster

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Installer les dépendances python
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code to the working directory
COPY . .

# Set the environment variables (if needed)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose the port on which the Flask app listens
EXPOSE 5000

# Lancer l'app Flask avec Gunicorn sur le port 5000 et recharger lorsque l'on modifie le code
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000", "--reload"]

