import os
from firebase_admin import credentials
import firebase_admin

cred = os.getenv('GOOGLE_CREDENTIALS', None)

if cred is not None:
    with open('service-account.json', 'w+', encoding='utf-8') as f:
        f.write(cred)


cred = credentials.Certificate('service-account.json')
firebase_admin.initialize_app(cred, {
        'databaseURL': os.getenv('DATABASE_URL')
})