import os
import time
import requests
import pandas as pd
import schedule
from sqlalchemy import create_engine, text

# Configuration Airtable
AIRTABLE_API_KEY = os.environ.get('AIRTABLE_API_KEY', 'votre_api_key')
AIRTABLE_BASE_ID = os.environ.get('AIRTABLE_BASE_ID', 'votre_base_id')
AIRTABLE_TABLE_NAME = os.environ.get('AIRTABLE_TABLE_NAME', 'votre_table')

# Configuration PostgreSQL
DB_USER = os.environ.get('DB_USER', 'superset')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'superset')
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'superset')
DB_TABLE = os.environ.get('DB_TABLE', 'airtable_data')

def sync_airtable_to_postgres():
    print(f"Début de la synchronisation des données à {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Connexion à Airtable et récupération des données
        url = f'https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}'
        headers = {'Authorization': f'Bearer {AIRTABLE_API_KEY}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Lever une exception si la requête échoue
        data = response.json()
        
        if 'records' not in data or len(data['records']) == 0:
            print("Aucun enregistrement trouvé dans Airtable")
            return
        
        # Transformer les données en DataFrame
        records = [record['fields'] for record in data['records']]
        df = pd.DataFrame(records)
        
        # Connexion à PostgreSQL et insertion des données
        engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
        
        # Créer la table si elle n'existe pas
        with engine.connect() as conn:
            conn.execute(text(f"""
                CREATE TABLE IF NOT EXISTS {DB_TABLE} (
                    id SERIAL PRIMARY KEY
                )
            """))
        
        # Insérer ou mettre à jour les données
        df.to_sql(DB_TABLE, engine, if_exists='replace', index=False)
        
        print(f"Données synchronisées avec succès: {len(df)} enregistrements")
    
    except Exception as e:
        print(f"Erreur lors de la synchronisation: {e}")

def run_scheduler():
    # Exécuter immédiatement une première fois
    sync_airtable_to_postgres()
    
    # Puis planifier l'exécution toutes les heures
    schedule.every(1).hour.do(sync_airtable_to_postgres)
    
    # Boucle pour maintenir le planificateur actif
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    run_scheduler()
