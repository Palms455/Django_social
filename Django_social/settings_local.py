DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'OPTIONS': {
            'options': '-c search_path=social'
        },
    'NAME': 'social',
    'HOST': 'localhost',
    'PORT': '5432',
    'USER': 'postgres',
    'PASSWORD': '1514150'
    },
}


EMAIL_HOST_USER = 'palms1990@gmail.com'
EMAIL_HOST_PASSWORD = 'feldsher3301344'

