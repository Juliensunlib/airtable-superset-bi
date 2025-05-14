FROM apache/superset:latest

USER root

# Installation des dépendances pour l'ETL Airtable
COPY docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Revenir à l'utilisateur superset
USER superset
