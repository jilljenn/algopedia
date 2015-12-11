# Algopedia

Encyclopédie d'algos collaborative

## Installation

Avec Python 3, faites :

    python3 -m venv venv
    . venv/bin/activate
    pip install -r requirements.txt
    cd web
    ./manage.py migrate
    ./manage.py runserver

Techniquement, il faudrait insérer les données `SECRET_KEY` dans un fichier externe `secret.py` non commité, maaais booon…
