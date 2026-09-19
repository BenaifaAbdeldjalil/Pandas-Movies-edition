
import requests as rq
import json
from pathlib import Path
import pandas as pd


url="https://ghibli-api.vercel.app/api/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
base=Path("data/raw/films_raw.json")
max_retries=3
response = rq.get(url, timeout=30)

print(response.status_code)



for attempt in range(1, max_retries + 1):
    try:

        response = rq.get(url)
                            # Vérifier que la requête a réussi
        print(response.raise_for_status())
                                # Écrire directement la réponse JSON dans un fichier
        break
    except rq.exceptions.HTTPError as e:
                print(f"❌ Erreur HTTP : {e}")
    except rq.exceptions.Timeout:
        print("❌ Délai dépassé (timeout)")
    except rq.exceptions.RequestException as e:
        print(f"❌ Erreur réseau : {e}")
    except OSError as e:
        print(f"❌ Erreur d'écriture fichier : {e}")
        break
else:
    raise RuntimeError(
        f"Échec de la récupération après {max_retries} tentatives"
    )