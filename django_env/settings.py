import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# --- SECURITY WARNING: keep the secret key used in production secret! ---
SECRET_KEY = 'your-secret-key-here' # Ganti dengan secret key yang aman di production

# --- SECURITY WARNING: don't run with debug turned on in production! ---
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'your-railway-app-name.up.railway.app'] # Tambahkan domain Railway Anda


# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplikasi Anda
    'user_app', # <-- Tambahkan baris ini
    # 'artist_app', # Tambahkan aplikasi lain jika sudah siap
    # 'payments',
    # 'music', # Atau 'playlists', dll.
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_env.urls' # Ganti dengan nama folder utama Anda jika berbeda

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # <-- Pastikan baris ini ada untuk mencari template di folder 'templates' level root
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_env.wsgi.application'


# --- Database ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Atau konfigurasi database lainnya seperti PostgreSQL
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# --- Password validation ---
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# --- Internationalization ---
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- Static files (CSS, JavaScript, Images) ---
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"] # Folder untuk static files development
STATIC_ROOT = BASE_DIR / "staticfiles" # Folder untuk static files production (akan di-generate oleh collectstatic)

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
