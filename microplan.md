Phase 1: Python and Django Basics
- Follow Django Tutorial:
    - https://docs.djangoproject.com/en/5.0/intro/tutorial01/# through https://docs.djangoproject.com/en/5.0/intro/tutorial08/
- Create the virtual environment
    - python -m venv BitEquip
    - Step into virtual environment with: .\BitEquip\Scripts\activate
- Install Django: 
    - pip install django
- Create a New Django Project: 
    - django-admin startproject equipapi
- Step into project loop:
    - If not in dir, cd equipapi
    - If i need to run server, py manage.py runserver
        - devserver opens on http://127.0.0.1:8000/

Phase 2: Set up PostgreSQL:
- Download and Install PostgreSQL with pgAdmin
- Connect to PogSQL 
- Create new DB
- Name new DB -> equipapi
- Django requires psycopg2 to interact with PogSQL:
    - pip install psycopg2
- Set-up DB config in DATABASES at path /equipapi/settings.py 
- Run migrations to create necessary tables when init a Django app
    - Includes auth, session and admin tables
    - py manage.py migrate

Phase 3: Model Definition and Relationships:

class Vendor:
- Has shop
- Has name
- Has currency

class Shop:
- Has name
- Has vendor
- Has currency
- Has items
- Has method (withdraw):
    - takes itself and an amount as parameters
    - can only withdraw if the amount passed is less than the amount that the shop currently has

class Item:
- has Name 
- has itemType
- has stats
- has shops
- has cost
- has quantity
- has method (add_to_shop):
    - takes itself, shop and quantity as paramaters
    - adds item to shop

class Player(models.Model):
- has userid 
- has name
- has currency  
- has stat
- has inventory
- has equipped
- has method (purchase_item)
- has method (equip_item)(self, item):


class InventoryItem(models.Model):
- has player 
- has items 
    quantity 