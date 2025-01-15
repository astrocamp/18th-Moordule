import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

allowed_hosts_env = os.getenv("ALLOWED_HOSTS", "*").split(",")
line_pay_hostname = os.getenv("HOSTNAME")
ALLOWED_HOSTS = allowed_hosts_env + [line_pay_hostname] + ['moordule.com', 'www.moordule.com'] 
# FIXME:確定部署沒問題，這段再刪除['https://a2a0-61-220-182-115.ngrok-free.app ']

CSRF_TRUSTED_ORIGINS = [f"https://{os.getenv('HOSTNAME')}"] 

AUTH_USER_MODEL = "users.CustomUser"
# Build paths inside the project like this: BASE_DIR / 'subdir'.
DEBUG = os.getenv("DEBUG", "True") == "True"

# 初始化環境變數
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = Path(__file__).resolve().parent.parent
# env = environ.Env(DEBUG=(bool, False))
# environ.Env.read_env(str(BASE_DIR / ".env"))
db_url = os.getenv("DATABASE_URL")
# AUTH_USER_MODEL = "users.CustomUser"
# DEBUG = env.bool("DEBUG", default=False)
LOGIN_URL = "users:signin"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "pages",
    "users",
    "shared",
    "activities",
    "cashflows",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "storages",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth 認證
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
    "allauth.account.middleware.AccountMiddleware",  # Add the account middleware:
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

ROOT_URLCONF = "moordule.urls"

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
                "shared.templatetags.navigation",
                # "shared.templatetags.meetup_components",
            ],
        },
    },
]

WSGI_APPLICATION = "moordule.wsgi.application"


SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": os.getenv("SOCIAL_AUTH_GOOGLE_CLIENT_ID"),
                "secret": os.getenv("SOCIAL_AUTH_GOOGLE_SECRET"),
                "settings": {
                    "scope": [
                        "profile",
                        "email",
                    ],
                    "auth_params": {
                        "access_type": "online",
                    },
                },
            },
        ],
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI = "http://moordule.com"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USERNAME"),
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

LINE_CHANNEL_ID = os.getenv("LINE_CHANNEL_ID")
LINE_CHANNEL_SECRET_KEY = os.getenv("LINE_CHANNEL_SECRET_KEY")
HOSTNAME = os.getenv("HOSTNAME")
LINE_REQUEST_URL = os.getenv("LINE_REQUEST_URL")
LINE_SANDBOX_URL = os.getenv("LINE_SANDBOX_URL")

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
MEDIA_URL = '/media/' 
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
        "OPTIONS": {
            "access_key": os.getenv("AWS_ACCESS_KEY_ID"),
            "secret_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
            "bucket_name": os.getenv("AWS_STORAGE_BUCKET_NAME"),
            "region_name": os.getenv("AWS_S3_REGION_NAME"),
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
AWS_S3_FILE_OVERWRITE = False 
AWS_DEFAULT_ACL = None
