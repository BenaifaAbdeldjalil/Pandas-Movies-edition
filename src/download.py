# -*- coding: utf-8 -*- 
# -*- coding: utf-8 -*- 
import requests as rq
import json



def fetch_data(url,max_retries: int = 3):
    
    for attempt in range(1, max_retries + 1):
        try:

            response = rq.get(url, timeout=30)
                        # Vérifier que la requête a réussi
                            # Écrire directement la réponse JSON dans un fichier
            return response
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


def save_data(data,path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(f"{path}", "w", encoding="utf-8") as f:
                json.dump(data.json(), f, indent=4, ensure_ascii=False)
                

