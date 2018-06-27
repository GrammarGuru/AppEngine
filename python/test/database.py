import os
os.chdir('..')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/auth.json'
from src.database import get_articles



print(get_articles())