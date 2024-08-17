import os
from notion_client import Client

# Laden der Umgebungsvariablen aus GitHub Secrets
notion_api_key = os.getenv("NOTION_API_KEY")
database_a_id = os.getenv("DATABASE_A_ID")
database_b_id = os.getenv("DATABASE_B_ID")

# Notion API Initialisierung
notion = Client(auth=notion_api_key)

# Funktion, um die Einträge einer Datenbank zu holen
def get_database_entries(database_id):
    results = []
    response = notion.databases.query(database_id=database_id)
    results.extend(response['results'])
    return results

# Holen der Einträge beider Datenbanken
entries_a = get_database_entries(database_a_id)
entries_b = get_database_entries(database_b_id)

# Verknüpfen basierend auf dem Datum
for entry_a in entries_a:
    date_a = entry_a['properties']['Datum']['date']['start']
    
    for entry_b in entries_b:
        date_b = entry_b['properties']['Datum']['date']['start']
        
        if date_a == date_b:
            # Verknüpfe die Einträge
            notion.pages.update(
                entry_a['id'],
                properties={
                    "Relation zu Datenbank B": {
                        "relation": [{"id": entry_b['id']}]
                    }
                }
            )

print("Verknüpfung abgeschlossen.")
