import os
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

allowed_hosts_env = os.getenv('ALLOWED_HOSTS', '*').split(',')
line_pay_hostname =  os.getenv('HOSTNAME')
ALLOWED_HOSTS = allowed_hosts_env + [line_pay_hostname]

CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('HOSTNAME')}"]

 
AUTH_USER_MODEL = "users.CustomUser"
# Build paths inside the project like this: BASE_DIR / 'subdir'.
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

# 初始化環境變數
BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env(DEBUG=(bool, False))
# environ.Env.read_env(str(BASE_DIR / ".env"))
db_url = os.getenv("DATABASE_URL")
# AUTH_USER_MODEL = "users.CustomUser"
# DEBUG = env.bool("DEBUG", default=False)
LOGIN_URL = 'users:signin'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY =  os.getenv("SECRET_KEY")

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Django 內建 APP
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "pages",
    "users",
    "shared",
    "activities",
    "cashflows",
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google', 
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Django 預設認證
    'allauth.account.auth_backends.AuthenticationBackend',  # allauth 認證
]

SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware", # Add the account middleware:
]

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

ROOT_URLCONF = "pydev.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "builtins": [
                "shared.templatetags.common_components",
                # "shared.templatetags.meetup_components",
            ],
        },
    },
]

WSGI_APPLICATION = "pydev.wsgi.application"


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": os.getenv("GMAIL_CLIENT_ID"),
            "secret": os.getenv("GMAIL_API_SECRET"),
        },
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
    }
}


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Taipei"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


