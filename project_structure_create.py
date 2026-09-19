import os
from pathlib import Path

folders = ["data","scripts","src","data/raw/","docs","data/processed/"
           ,"data/final/","data/final/by_director/"]

base = Path(".")  # dossier courant

# 1) folders creation
for f in folders:
    path = base / f
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"✅ Créé : {path}")
    else:
        print(f"⏭️  Existe déjà : {path}")

print("\nContenu actuel :", os.listdir())


# 2) files creation
files = ["scripts/01_download.py","scripts/02_clean.py",
         "scripts/03_split.py","scripts/04_check.py",
         "src/clean.py","src/download.py","src/split.py","docs/GUIDE.md","src/__init__.py",
         "requirements.txt",".gitignore","README.md","data/raw/.gitkeep",
         "data/final/by_director/.gitkeep"]

for fi in files:
    file = base/fi
    if file ==".gitignore":
        file.write_text("""# Environnements virtuels\n
                        .venv/\n
                        venv/\n
                        env/\n\n

                        # Cache Python\n
                        __pycache__/\n
                        *.py[cod]\n\n
                        ```
                        venv/
                        __pycache__/
                        data/raw/
                        data/processed/
                        ```

                        # Configuration locale\n
                        .env\n\n

                        # Fichiers système\n
                        .DS_Store\n
                        Thumbs.db\n\n

                        # Données générées\n
                        data/processed/*\n
                        data/final/*\n

                        # Conserver les dossiers dans Git\n
                        !data/raw/.gitkeep\n
                        !data/processed/.gitkeep\n
                        !data/final/by_director/.gitkeep\n

                        # Fichiers de développement\n
                        .vscode/\n
                        .idea/\n""", encoding="utf-8")
        print(f"✅ Fichier créé : { file.resolve() }")
    elif file.exists():
        print(f"⏭️  Le fichier { file } existe déjà")
    else:
        file.write_text("# -*- coding: utf-8 -*- \n", encoding="utf-8")
        print(f"✅ Fichier créé : { file.resolve() }")
