# TP — Build a Python/Pandas Pipeline for Public Data (Studio Ghibli edition)

**Goal:** practice fetching public data from an API, cleaning it with pandas,
and exporting it into a clean, reusable folder structure — using the
**Studio Ghibli API**, which needs **no API key at all**.

**Level:** beginner/intermediate. Each step gives you the goal, hints, and a
code skeleton with `TODO`s — not a full solution. Try to fill it in yourself
before peeking at the hints.

**Tools:** Python 3.10+, VS Code, Git/GitHub.

**API used:** https://ghibli-api.vercel.app/api/films — no auth, no sign-up,
returns all 22 Studio Ghibli films as JSON in one single request.

---

## 0. Setup

### 0.1 Create the GitHub repo

```bash
git clone https://github.com/<your-username>/ghibli-data-pipeline.git
cd ghibli-data-pipeline
code .
```

### 0.2 Project skeleton

```
pandas-products-pipeline/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
├── src/
│   ├── __init__.py
│   ├── download.py
│   ├── clean.py
│   └── split.py
├── scripts/
│   ├── 01_download.py
│   ├── 02_clean.py
│   ├── 03_split.py
│   └── 04_check.py
├── requirements.txt
├── .gitignore
└── README.md
```

### 0.3 Virtual environment + dependencies

```bash
python -m venv venv
.\venv\Scripts\activate       # Windows: venv\Scripts\activate
```
project_structure_create.py


`requirements.txt`:
```
requests
pandas
pyarrow
```

echo requests >> requirements.txt
pandas >> requirements.txt  
pyarrow   python-dotenv >> requirements.txt


```bash
pip install -r requirements.txt 
or 
.\venv\Scripts\python.exe -m pip install requests
```

verification :
.\venv\Scripts\python.exe -m pip list 
Package            Version
------------------ ---------
certifi            2026.7.22
charset-normalizer 3.5.1
idna               3.20
pip                26.1.2
requests           2.34.2
urllib3            2.8.0


### 0.4 `.gitignore`

```
venv/
__pycache__/
data/raw/
data/processed/
```

No `.env` needed this time — no secret to hide.

### ✅ Checkpoint 0
- `git status` is clean, `venv` activated, `pandas`/`requests`/`pyarrow`
  installed.

---
Voici le même TP, adapté à l’API **DummyJSON Products**. Cette API retourne un objet JSON dont la clé `products` contient la liste des produits, avec aussi des métadonnées de pagination : `total`, `skip` et `limit`. Ton fichier exemple suit bien cette structure, avec des objets imbriqués comme `dimensions` et `meta`, ainsi que des listes comme `tags`, `reviews` et `images`. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)

# TP — Construire un pipeline Python/Pandas (DummyJSON Products)

**Objectif :** pratiquer le téléchargement de données depuis une API publique, le nettoyage avec pandas, la séparation en fichiers réutilisables et les contrôles de qualité.

**Niveau :** débutant/intermédiaire.

**Outils :** Python 3.10+, VS Code, Git/GitHub, pandas, requests, pyarrow.

**API utilisée :** [DummyJSON Products](https://dummyjson.com/products/) — aucune clé API nécessaire.

***

## 0. Setup

### 0.1 Créer le dépôt GitHub

```bash
git clone https://github.com/<ton-username>/pandas-products-pipeline.git
cd pandas-products-pipeline
code .
```

Si tu crées le projet en local avant GitHub :

```bash
mkdir pandas-products-pipeline
cd pandas-products-pipeline
git init
code .
```

### 0.2 Structure du projet

```text
pandas-products-pipeline/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
├── src/
│   ├── __init__.py
│   ├── download.py
│   ├── clean.py
│   └── split.py
├── scripts/
│   ├── 01_download.py
│   ├── 02_clean.py
│   ├── 03_split.py
│   └── 04_check.py
├── requirements.txt
├── .gitignore
└── README.md
```

### 0.3 Créer et activer le venv

Sous PowerShell / Windows :

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Vérifie l’interpréteur utilisé :

```powershell
python -c "import sys; print(sys.executable)"
```

Le chemin doit contenir :

```text
pandas-products-pipeline\venv\Scripts\python.exe
```

### 0.4 Dépendances

Crée le fichier `requirements.txt` :

```text
requests
pandas
pyarrow
```

Puis installe-les :

```powershell
python -m pip install -r requirements.txt
```

Vérification :

```powershell
python -m pip list
```

Tu dois voir au minimum :

```text
pandas
pyarrow
requests
```

### 0.5 Fichier `.gitignore`

```gitignore
venv/
__pycache__/
*.pyc

data/raw/
data/processed/
data/final/
```

Les données sont générées par le pipeline : il est donc cohérent de ne pas les pousser sur GitHub.

### ✅ Checkpoint 0

- Le venv est activé.
- `requests`, `pandas` et `pyarrow` sont installés.
- La structure des dossiers existe.
- `git status` n’affiche pas le dossier `venv/`.

***

## 1. Inspecter l’API

Ouvre cette URL dans ton navigateur :

```text
https://dummyjson.com/products/
```

La réponse est un objet JSON de ce type :

```json
{
  "products": [
    {
      "id": 1,
      "title": "Essence Mascara Lash Princess",
      "description": "The Essence Mascara Lash Princess...",
      "category": "beauty",
      "price": 9.99,
      "discountPercentage": 10.48,
      "rating": 2.56,
      "stock": 99,
      "tags": ["beauty", "mascara"],
      "brand": "Essence",
      "sku": "BEA-ESS-ESS-001",
      "weight": 4,
      "dimensions": {
        "width": 15.14,
        "height": 13.08,
        "depth": 22.99
      },
      "reviews": [
        {
          "rating": 3,
          "comment": "Would not recommend!",
          "date": "2025-04-30T09:41:02.053Z"
        }
      ],
      "meta": {
        "createdAt": "2025-10-09T14:47:01.588Z",
        "updatedAt": "2026-05-23T11:27:41.868Z"
      }
    }
  ],
  "total": 194,
  "skip": 0,
  "limit": 30
}
```

L’API retourne des produits dans `products`, mais également `total`, `skip` et `limit` pour la pagination. Les produits ont des colonnes simples, des dictionnaires imbriqués (`dimensions`, `meta`) et des listes (`tags`, `reviews`, `images`). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)

### Points à observer

| Champ | Type / problème potentiel | Traitement proposé |
|---|---|---|
| `id`, `stock`, `weight`, `minimumOrderQuantity` | Entiers, parfois à sécuriser | `pd.to_numeric(..., errors="coerce").astype("Int64")` |
| `price`, `rating`, `discountPercentage` | Décimaux | `pd.to_numeric(..., errors="coerce")` |
| `dimensions` | Objet JSON imbriqué | Aplatir avec `pd.json_normalize()` |
| `meta` | Objet JSON imbriqué | Aplatir avec `pd.json_normalize()` |
| `meta.createdAt`, `meta.updatedAt` | Dates ISO 8601 | `pd.to_datetime(..., utc=True)` |
| `tags` | Liste | Conserver en texte ou compter les tags |
| `reviews` | Liste d’objets | Calculer `nb_reviews` |
| `images` | Liste d’URLs | Calculer `nb_images` |
| `description`, `thumbnail`, `meta.qrCode` | Champs parfois inutiles pour une table analytique | Supprimer selon le besoin |

### ✅ Checkpoint 1

- Tu as constaté que la liste se trouve dans `data["products"]`.
- Tu as identifié les objets imbriqués : `dimensions` et `meta`.
- Tu as identifié les listes : `tags`, `reviews`, `images`.
- Tu sais qu’il ne faut pas faire directement `pd.DataFrame(data)`, car cela créerait seulement les colonnes `products`, `total`, `skip` et `limit`.

***

## 2. Step 1 — Download

**Objectif :** appeler l’API, télécharger les produits et sauvegarder la réponse brute dans `data/raw/products_raw.json`.

Pour apprendre la pagination plus tard, on conserve toute la réponse API brute, y compris `total`, `skip` et `limit`.

### `src/download.py`

```python
import json
import time
from pathlib import Path

import requests


API_URL = "https://dummyjson.com/products"
RAW_PATH = Path("data/raw/products_raw.json")


def fetch_products(max_retries: int = 3) -> dict:
    """Appelle l'API et retourne la réponse JSON brute."""

    for attempt in range(1, max_retries + 1):
        try:
            # TODO 1: appeler requests.get avec API_URL et timeout=30

            # TODO 2: déclencher une exception si le code HTTP est en erreur
            # Indice : response.raise_for_status()

            # TODO 3: récupérer response.json() dans une variable data

            # TODO 4: vérifier que la clé "products" existe dans data
            # Si elle n'existe pas, lever une ValueError explicite.

            # TODO 5: retourner data
            pass

        except requests.RequestException as error:
            print(f"Tentative {attempt}/{max_retries} échouée : {error}")

            if attempt < max_retries:
                # TODO : attendre avant la prochaine tentative
                # Indice : time.sleep(2 * attempt)
                pass

    raise RuntimeError("Impossible de télécharger les données après plusieurs tentatives.")


def save_raw(data: dict, path: Path = RAW_PATH) -> None:
    """Sauvegarde la réponse brute de l'API dans un fichier JSON."""

    path.parent.mkdir(parents=True, exist_ok=True)

    # TODO :
    # ouvrir path en écriture avec encoding="utf-8"
    # utiliser json.dump(...)
    # ajouter ensure_ascii=False et indent=2
```

### `scripts/01_download.py`

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)))

from src.download import fetch_products, save_raw


data = fetch_products()
save_raw(data)

print(f"Fichier brut sauvegardé.")
print(f"Produits téléchargés : {len(data['products'])}")
print(f"Total de produits annoncé par l'API : {data['total']}")
print(f"Limite API utilisée : {data['limit']}")
```

### Indices

- Utilise `requests.get(API_URL, timeout=30)`.
- Utilise `response.raise_for_status()` avant `response.json()`.
- `response.json()` retourne ici un dictionnaire, pas directement une liste.
- Utilise `json.dump(data, file, ensure_ascii=False, indent=2)`.
- L’API limite généralement la réponse initiale à une page ; le champ `total` peut être supérieur à `len(data["products"])`. Ton fichier d’exemple contient 30 produits et indique un total de 194. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)

### ✅ Checkpoint 2

Après :

```powershell
python scripts/01_download.py
```

tu dois avoir :

```text
data/raw/products_raw.json
```

et le script doit afficher le nombre de produits récupérés.

***

## 3. Step 2 — Cleaning

**Objectif :** charger la réponse JSON brute, extraire `products`, aplatir les objets imbriqués, convertir les types et sauvegarder une table propre.

### Règles de nettoyage

| Problème | Action |
|---|---|
| La réponse brute contient une clé `products` | Charger `data["products"]` |
| `dimensions` et `meta` sont imbriqués | Utiliser `pd.json_normalize(data["products"])` |
| Certains types peuvent être incohérents | Convertir explicitement les colonnes numériques |
| Dates sous forme de texte ISO | Convertir avec `pd.to_datetime(..., format="ISO8601", utc=True, errors="coerce")` |
| `tags`, `reviews`, `images` sont des listes | Produire des compteurs `nb_tags`, `nb_reviews`, `nb_images` |
| Doublons possibles | `drop_duplicates(subset="id")` |
| Colonnes techniques ou trop lourdes | Supprimer si elles ne servent pas à l’analyse |

### `src/clean.py`

```python
import json
from pathlib import Path

import pandas as pd


KEEP_COLS = [
    "id",
    "title",
    "category",
    "brand",
    "sku",
    "price",
    "discountPercentage",
    "rating",
    "stock",
    "weight",
    "minimumOrderQuantity",
    "availabilityStatus",
    "warrantyInformation",
    "shippingInformation",
    "dimensions.width",
    "dimensions.height",
    "dimensions.depth",
    "meta.createdAt",
    "meta.updatedAt",
    "tags",
    "reviews",
    "images",
]


def load_raw(path: str | Path) -> pd.DataFrame:
    """Charge le JSON brut et retourne un DataFrame de produits aplati."""

    # TODO 1 : convertir path en Path

    # TODO 2 : ouvrir le fichier JSON avec encoding="utf-8"

    # TODO 3 : charger json.load(file) dans data

    # TODO 4 : vérifier que "products" existe dans data

    # TODO 5 : retourner pd.json_normalize(data["products"])
    pass


def list_length(value) -> int:
    """Retourne la taille d'une liste ; retourne 0 si la valeur n'est pas une liste."""

    # TODO :
    # return len(value) if isinstance(value, list) else 0
    pass


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et prépare les données produits pour l'analyse."""

    # TODO 1 :
    # Conserver uniquement les colonnes de KEEP_COLS présentes dans df.
    # Indice : [column for column in KEEP_COLS if column in df.columns]

    # TODO 2 :
    # Travailler sur une copie du DataFrame.

    # TODO 3 :
    # Renommer les colonnes avec un dictionnaire, par exemple :
    #
    # "discountPercentage" -> "discount"
    # "dimensions.width" -> "dimension_width"
    # "dimensions.height" -> "dimension_height"
    # "dimensions.depth" -> "dimension_depth"
    # "meta.createdAt" -> "dt_creation"
    # "meta.updatedAt" -> "dt_update"

    # TODO 4 :
    # Convertir les colonnes entières :
    # id, stock, weight, minimumOrderQuantity
    #
    # Indice :
    # pd.to_numeric(df[column], errors="coerce").astype("Int64")

    # TODO 5 :
    # Convertir les décimaux :
    # price, discount, rating,
    # dimension_width, dimension_height, dimension_depth
    #
    # Indice :
    # pd.to_numeric(df[column], errors="coerce")

    # TODO 6 :
    # Convertir dt_creation et dt_update au format datetime UTC.
    #
    # Indice :
    # pd.to_datetime(
    #     df[column],
    #     format="ISO8601",
    #     utc=True,
    #     errors="coerce"
    # )

    # TODO 7 :
    # Créer les colonnes numériques :
    # creation_year
    # creation_month
    # update_year
    # update_month
    #
    # Indice :
    # df["dt_update"].dt.year.astype("Int64")
    # df["dt_update"].dt.month.astype("Int64")

    # TODO 8 :
    # Créer les compteurs :
    # nb_tags à partir de tags
    # nb_reviews à partir de reviews
    # nb_images à partir de images

    # TODO 9 :
    # Supprimer tags, reviews, images si tu veux une table analytique plate.

    # TODO 10 :
    # Supprimer les doublons selon id.

    # TODO 11 :
    # Trier par category puis title.

    # TODO 12 :
    # Réinitialiser l'index puis retourner df.
    pass


def save_clean(
    df: pd.DataFrame,
    csv_path: str | Path,
    parquet_path: str | Path,
) -> None:
    """Sauvegarde le DataFrame nettoyé en CSV et Parquet."""

    csv_path = Path(csv_path)
    parquet_path = Path(parquet_path)

    # TODO 1 : créer les dossiers parents des deux chemins

    # TODO 2 :
    # sauvegarder le CSV avec index=False et encoding="utf-8"

    # TODO 3 :
    # sauvegarder le Parquet avec index=False
    pass
```

### `scripts/02_clean.py`

```python
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)))

from src.clean import clean_products, load_raw, save_clean


df = load_raw("data/raw/products_raw.json")

print("Shape avant nettoyage :", df.shape)
print("Colonnes brutes :")
print(df.columns.tolist())

df_clean = clean_products(df)

save_clean(
    df_clean,
    "data/processed/products_clean.csv",
    "data/processed/products_clean.parquet",
)

print("\nShape après nettoyage :", df_clean.shape)
print("\nTypes des colonnes :")
print(df_clean.dtypes)

print("\nAperçu :")
print(df_clean.head())
```

### Indices

Pour convertir proprement les entiers :

```python
df[column] = (
    pd.to_numeric(df[column], errors="coerce")
    .astype("Int64")
)
```

Pour convertir les décimaux :

```python
df[column] = pd.to_numeric(df[column], errors="coerce")
```

Pour les dates :

```python
df["dt_update"] = pd.to_datetime(
    df["dt_update"],
    format="ISO8601",
    utc=True,
    errors="coerce"
)
```

Pour compter les valeurs des listes de façon robuste :

```python
df["nb_reviews"] = df["reviews"].apply(
    lambda value: len(value) if isinstance(value, list) else 0
)
```

Pour renommer :

```python
df = df.rename(columns=columns_mapping)
```

et non :

```python
df.rename(mapper=columns_mapping)
```

car il faut cibler explicitement les colonnes.

### ✅ Checkpoint 3

Après :

```powershell
python scripts/02_clean.py
```

tu dois avoir :

```text
data/processed/products_clean.csv
data/processed/products_clean.parquet
```

Contrôles attendus :

```python
df_clean["id"].is_unique
```

doit retourner :

```text
True
```

Et les types doivent être cohérents :

```text
id                       Int64
stock                    Int64
price                  float64
rating                 float64
dt_creation    datetime64[ns, UTC]
dt_update      datetime64[ns, UTC]
update_year              Int64
update_month             Int64
```

***

## 4. Step 3 — Split

**Objectif :** créer un fichier CSV par catégorie de produit.

Ici, le meilleur groupe est `category`, car les produits sont naturellement répartis en catégories telles que `beauty`, `fragrances`, `furniture` ou `groceries`. Ton échantillon contient notamment ces catégories. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)

### `src/split.py`

```python
import re
from pathlib import Path

import pandas as pd


def safe_filename(value: str) -> str:
    """Transforme une valeur en nom de fichier simple et sûr."""

    # TODO :
    # - convertir la valeur en str
    # - enlever les espaces inutiles
    # - mettre en minuscules
    # - remplacer les espaces par des underscores
    # - remplacer les caractères non alphanumériques par underscores
    # - retourner un nom propre
    pass


def split_by_group(
    df: pd.DataFrame,
    group_col: str,
    out_dir: str | Path,
) -> None:
    """Écrit un CSV par valeur distincte de group_col."""

    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # TODO 1 :
    # vérifier que group_col existe dans df.columns,
    # sinon lever une KeyError explicite.

    # TODO 2 :
    # parcourir df.groupby(group_col, dropna=False)

    # TODO 3 :
    # pour chaque groupe :
    # - construire un nom de fichier sûr
    # - sauvegarder le groupe en CSV avec index=False
    # - afficher le nom du groupe et le nombre de lignes
```

### `scripts/03_split.py`

```python
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)))

from src.split import split_by_group


df = pd.read_csv("data/processed/products_clean.csv")

split_by_group(
    df=df,
    group_col="category",
    out_dir="data/final/by_category",
)
```

### Exemple de résultat

```text
data/final/by_category/
├── beauty.csv
├── fragrances.csv
├── furniture.csv
├── groceries.csv
└── ...
```

### ✅ Checkpoint 4

Après :

```powershell
python scripts/03_split.py
```

tu dois avoir plusieurs fichiers dans :

```text
data/final/by_category/
```

Le nombre total de lignes dans tous les fichiers doit être égal au nombre de lignes dans `products_clean.csv`.

***

## 5. Bonus — Statistiques par catégorie

Crée un script `scripts/05_stats.py` ou ajoute ce bloc à la fin de `03_split.py` :

```python
import pandas as pd

df = pd.read_csv("data/processed/products_clean.csv")

stats = (
    df.groupby("category")
    .agg(
        nb_products=("id", "count"),
        avg_price=("price", "mean"),
        avg_rating=("rating", "mean"),
        total_stock=("stock", "sum"),
        avg_reviews=("nb_reviews", "mean"),
    )
    .sort_values("nb_products", ascending=False)
)

print(stats)
```

Tu peux aussi chercher :

```python
most_expensive = df.loc[df["price"].idxmax()]
print(most_expensive[["title", "category", "brand", "price"]])
```

Ou les produits avec peu de stock :

```python
low_stock = df[df["stock"] < 10]

print(low_stock[
    ["id", "title", "category", "stock", "availabilityStatus"]
])
```

***

## 6. Step 4 — Check

**Objectif :** vérifier automatiquement les sorties de ton pipeline.

Cette étape est importante dans une logique data engineering : elle permet de détecter rapidement une régression dans les données, la structure de l’API ou tes transformations.

### `scripts/04_check.py`

```python
import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/35551766/ec5da567-2ce1-4e00-997e-1d27f7c224b8/paste.txt?AWSAccessKeyId=ASIA2F3EMEYERYZYKOE2&Signature=%2Bmy6S2gmcZu6cRGqM15unbozPdc%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEFIaCXVzLWVhc3QtMSJHMEUCIEHruVV4imOPOXR1SIZ1TxyrVXPRK9JTusxYtmIIXMEtAiEAslelH2%2F3GovI2MwVStB%2FCmDR2dDM7GG9XiQ62qy44JQq%2BgQIGhABGgw2OTk3NTMzMDk3MDUiDLUecpVWVWTTOjTYGSrXBFSuc9GLiLAMtt%2BLWuJ1w2%2BMOO24j6dBHm8QFxqY2CcdHvQeKCO7cmp6kkM77A93c6stCxO23ToKZio9TSJVKTl80uTEH4fwQSdC0PSqXGSo972nKYjAYk78tJ4xFo2tKhyv6eywSqW842vtHb12tI6cUBM3k7NIuiSvRhV%2Fu592vV3rP7F%2FanohZtk0Ub1mI3ZK1Low%2B4FuH%2BwjtEVfHH1h9yi8Y5OUhxlHHWJEY7rMH3aW44HBFl32fPHwFapZmXOn%2Fd%2BlkOyRru7wCic0dFOZTpgXL6j2HZ3BhWn8MPrqjWgrM4WyMjC7orEbJAMAncPS2jHNpKWxrjHO3UJ35yvGNvDSDNmsGoZVXUlJ5e5TxEhjsPchhr5IL7bQr1nuvMZ9kQ%2B3lFRkW8dCnFXz2SDrSwHkLe%2F%2BnJ9nWd5xskUBd%2FVST2XfGQI3ZlCv6QsE4xIumy1yO5QcqYVQc%2FamUvnGb73vT9Oe569w772OCgixuFIIvJp35SSmrqytHEuN34qwV64J6Hy%2FSsTE9GnYqBQccVun1qRroH8rruxrLvXRaTXN1fGPai%2F21ACj55tcQQ3xboK3YZsHQUs32ElDM%2BTEn1uk%2BQa%2FX67IVL1KX1i8O5JlW7Lf2d0BbCRoLBzn%2FlImE%2BdMMrRt%2BOyavNIlGb47qAx1%2Ff585s%2BYJnDwGsdJv%2BBUCseDdNJadDnOjRHr1yiBJVMoFlfUfZfjGKmaMTfzAzbwzeC0e9w8Om%2BaOXuQ1dA81%2FhIhcIb07mgR%2F4HyMDkTve7Hie%2BZF3QFl8ByFLbpFUd0tzoMJDL49UGOpgBICgimGeVs8h4%2BJJtCUC1cURSyw0oeSFm2NVpoM43njkh4VfvGBILkSHJNFg0EfwwLOER4I9AZ87eDWSIcAKAypY6cYuoKgkRITUJSButlFVFxfPQFrKoFL8LDEPwYnnd%2FDTUjKQ2KLdR3hg3uu1Hxzbpkq4JnNCyD6EvTPzv5FbHt066DxRPRCemV4IRPIJsPegOma6Kn9c%3D&Expires=1790505827)))


CSV_PATH = Path("data/processed/products_clean.csv")
PARQUET_PATH = Path("data/processed/products_clean.parquet")
FINAL_DIR = Path("data/final/by_category")


def main() -> None:
    # TODO 1 : vérifier l'existence du CSV et du Parquet

    # TODO 2 : charger le CSV dans df_csv

    # TODO 3 : vérifier que le DataFrame n'est pas vide
    # Indice : assert not df_csv.empty

    # TODO 4 : vérifier l'unicité de id
    # Indice : assert df_csv["id"].is_unique

    # TODO 5 : définir les colonnes obligatoires
    required_columns = [
        "id",
        "title",
        "category",
        "price",
        "rating",
        "stock",
        "dt_creation",
        "dt_update",
        "nb_tags",
        "nb_reviews",
        "nb_images",
    ]

    # TODO 6 : vérifier que toutes les colonnes obligatoires sont présentes

    # TODO 7 : charger le Parquet dans df_parquet

    # TODO 8 : vérifier que CSV et Parquet ont la même shape
    # Indice : assert df_csv.shape == df_parquet.shape

    # TODO 9 : récupérer les fichiers CSV dans FINAL_DIR
    # Indice : list(FINAL_DIR.glob("*.csv"))

    # TODO 10 : sommer le nombre de lignes de tous les fichiers catégorie

    # TODO 11 : vérifier que ce total est égal à len(df_csv)

    # TODO 12 : afficher un résumé clair des contrôles réussis
    pass


if __name__ == "__main__":
    main()
```

### Résultat attendu

```powershell
python scripts/04_check.py
```

doit afficher quelque chose comme :

```text
✅ CSV chargé : 30 lignes
✅ Identifiants produits uniques
✅ Colonnes obligatoires présentes
✅ CSV et Parquet ont la même dimension
✅ Fichiers par catégorie : 30 lignes au total
✅ Tous les contrôles sont validés
```

### ✅ Checkpoint 5

- Le CSV et le Parquet existent.
- Le DataFrame nettoyé contient au moins un produit.
- La colonne `id` est unique.
- Tous les fichiers de `data/final/by_category/` réunis contiennent autant de lignes que le fichier propre.
- Les colonnes attendues sont présentes.

***

## 7. Common errors

| Erreur | Cause probable | Correction |
|---|---|---|
| `KeyError: 'products'` | Tu essaies de lire un JSON dont la structure n’est pas celle attendue | Affiche `data.keys()` et vérifie que tu charges bien le fichier brut DummyJSON |
| Colonnes `products`, `total`, `skip`, `limit` seulement | Tu as fait `pd.DataFrame(data)` | Utilise `pd.json_normalize(data["products"])` |
| `AttributeError: Can only use .dt accessor` | `dt_update` ou `dt_creation` est encore du texte / nombre | Convertis d’abord avec `pd.to_datetime(...)` |
| Dates devenues `NaT` | Tu as appliqué `pd.to_numeric()` à toutes les colonnes avant la conversion de date | Recharge le JSON brut et applique `pd.to_datetime()` uniquement aux dates |
| `ValueError: Cannot convert non-finite values` | Conversion directe en `int64` avec des valeurs manquantes | Utilise d’abord `pd.to_numeric(..., errors="coerce")`, puis `.astype("Int64")` |
| `ModuleNotFoundError: No module named 'src'` | Script lancé depuis un mauvais dossier | Lance depuis la racine du projet et conserve le bloc `sys.path.append(...)` |
| `No module named pyarrow` | `pyarrow` manque dans le venv | `python -m pip install pyarrow` |
| Erreur lors de `.apply(len)` | Une valeur de `reviews`, `tags` ou `images` n’est pas une liste | Utilise `len(x) if isinstance(x, list) else 0` |
| `FileNotFoundError` sur le JSON brut | `01_download.py` n’a pas encore été exécuté | Exécute les scripts dans l’ordre : download, clean, split, check |
| Fichiers par catégorie avec des noms invalides | Catégorie contenant un caractère spécial | Utilise une fonction `safe_filename()` |

***

## 8. Exécuter le pipeline

Depuis la racine du projet :

```powershell
python scripts/01_download.py
python scripts/02_clean.py
python scripts/03_split.py
python scripts/04_check.py
```

L’ordre est important :

1. **Download** : API → JSON brut.
2. **Cleaning** : JSON brut → CSV et Parquet propres.
3. **Split** : CSV propre → un CSV par catégorie.
4. **Check** : contrôles de qualité sur toutes les sorties.

***

## 9. Wrap-up GitHub

Lorsque ton pipeline fonctionne :

```powershell
git add .
git commit -m "Build DummyJSON products pandas pipeline"
git push
```

Ton `README.md` peut contenir :

```markdown
# DummyJSON Products Pipeline

Pipeline Python/Pandas pour télécharger, nettoyer, segmenter et contrôler
les données produits de l'API DummyJSON.

## Source

https://dummyjson.com/products/

## Exécution

```powershell
python scripts/01_download.py
python scripts/02_clean.py
python scripts/03_split.py
python scripts/04_check.py
```

## Outputs

- `data/raw/` : réponse API brute au format JSON
- `data/processed/` : données nettoyées aux formats CSV et Parquet
- `data/final/by_category/` : un fichier CSV par catégorie
```

***

## 10. Going further

Une fois le pipeline de base terminé, tu peux améliorer ton projet comme dans un vrai mini-projet de data engineering :

- Ajouter la pagination pour récupérer tous les produits annoncés par `total`, et pas seulement la première page.
- Ajouter une colonne `ingestion_timestamp` au moment du téléchargement.
- Créer une table séparée `reviews` en utilisant `explode()` sur la colonne `reviews`.
- Créer une table séparée `product_tags` avec une ligne par couple `product_id` / `tag`.
- Ajouter des tests `pytest` pour `clean_products()`.
- Ajouter un fichier de logs avec le module `logging`.
- Comparer une exécution à l’autre afin de détecter de nouveaux produits ou des changements de prix.
- Charger le fichier Parquet avec DuckDB :

```python
import duckdb

result = duckdb.sql("""
    SELECT
        category,
        COUNT(*) AS nb_products,
        ROUND(AVG(price), 2) AS avg_price
    FROM 'data/processed/products_clean.parquet'
    GROUP BY category
    ORDER BY nb_products DESC
""")

print(result)
```