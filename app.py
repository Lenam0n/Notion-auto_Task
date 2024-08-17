import os
from notion_client import Client

# Laden der Umgebungsvariablen aus GitHub Secrets
notion_api_key = os.getenv("NOTION_API_KEY")
database_a_id = os.getenv("DATABASE_B_ID")
database_b_id = os.getenv("DATABASE_A_ID")

# Fehlerbehandlung: Sicherstellen, dass die IDs nicht leer sind
if not database_a_id or not database_b_id:
    raise ValueError("Die Datenbank-ID wurde nicht richtig gesetzt.")

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

# Funktion, um das Datum sicher abzurufen
def get_date(entry, property_name):
    try:
        # Überprüfen, ob die Eigenschaft vorhanden ist
        if property_name in entry['properties']:
            property_value = entry['properties'][property_name]
            
            # Überprüfen, ob das 'date'-Feld vorhanden ist und es nicht None ist
            if property_value.get('date') is not None:
                date_start = property_value['date'].get('start')
                if date_start is not None:
                    return date_start
                else:
                    return None
            else:
                return None
        else:
            return None
    except KeyError as e:
        return None


# Verknüpfen basierend auf dem Datum
for entry_a in entries_a:
    date_a = get_date(entry_a, 'Date')
    
    if date_a is None:
        continue  # Überspringen, wenn das Datum nicht gesetzt ist
    
    for entry_b in entries_b:
        date_b = get_date(entry_b, 'Date')
        
        if date_b is None:
            continue  # Überspringen, wenn das Datum nicht gesetzt ist
        
        if date_a == date_b:
            # Verknüpfe die Einträge
            notion.pages.update(
                entry_a['id'],
                properties={
                    "TASKS": {
                        "relation": [
                            {"id": entry_b['id']}
                        ]
                    }
                }
            )

print("Verknüpfung abgeschlossen.")
