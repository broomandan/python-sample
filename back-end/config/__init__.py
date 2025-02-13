# config/__init__.py
import os

env = os.getenv('APP_ENV', 'development')
print(f'Loading {env} environment settings...')

if env == 'development':
    from config.development import *
elif env == 'uat':
    from config.uat import *
elif env == 'production':
    from config.production import *
else:
    raise ValueError(f"Unknown environment: {env}")