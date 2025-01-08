from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

SITE_ID = 1

# Load environment variables from a .env file
load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment Variables
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # Secret Key
DEBUG = os.getenv('DEBUG', 'False') == 'True'
LOG = os.getenv('LOG', 'False') == 'True'
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')


# settings.py
STRIPE_TEST_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY')
STRIPE_TEST_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')

# Allowed Hosts
ALLOWED_HOSTS = ['hca.up.railway.app', 'localhost', '127.0.0.1']
CSRF_TRUSTED_ORIGINS = ['https://hca.up.railway.app']

# Email Configuration
USE_MAILJET = os.getenv('MAILJET_ON', 'False') == 'True'
print(USE_MAILJET)

DEFAULT_FROM_EMAIL = "admin@djangobookstore.com"

if USE_MAILJET:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'in-v3.mailjet.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv('MAILJET_API_KEY')
    EMAIL_HOST_PASSWORD = os.getenv('MAILJET_API_SECRET')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = [
    'jazzmin', 

    'notifications',
    # Local Apps
    'accounts.apps.AccountsConfig',
    'clinic.apps.ClinicConfig',
    'medical_records.apps.MedicalRecordsConfig',
    'coms.apps.ComsConfig',
    'appointments.apps.AppointmentsConfig',
    'doctor_panel.apps.DoctorPanelConfig',
    'diagnostics_and_prescriptions.apps.DiagnosticsAndPrescriptionsConfig',
    'payments.apps.PaymentsConfig',
    # Third-Party Apps
    'phonenumber_field',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'storages',   
    # Django Built-in Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

JAZZMIN_SETTINGS = {
    "site_title": "Biolink Admin",
    "site_header": "Biolink Admin Panel",
    "site_brand": "Biolink",
    "welcome_sign": "Welcome to the Biolink Admin Panel!",
    "show_sidebar": True,
    "navigation_expanded": True,
    "custom_css": None,
    "custom_js": None,
}

# Middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
]

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

# URL Configuration
ROOT_URLCONF = 'h.urls'
WSGI_APPLICATION = 'h.wsgi.application'

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Add your custom context processor
                'h.context_processors.common_data',
            ],
        },
    },
]

# Databases
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'local_db_name'),
            'USER': os.getenv('DB_USER', 'local_user'),
            'PASSWORD': os.getenv('DB_PASSWORD', 'local_password'),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }


USE_AWS = os.getenv('AWS3_ON', 'False') == 'True'
print(USE_AWS)


if USE_AWS:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_QUERYSTRING_AUTH = False  # Disables querystring in URLs

    # S3 Static and Media Files Storage
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # Static and Media URLs
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
    STATICC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'

    # STATIC_ROOT is not needed for AWS
    STATIC_ROOT = None
else:
    # Local Development Setup
    STATIC_URL = 'static/'
    STATICC_URL = 'static/'
    STATICFILES_DIRS = [BASE_DIR / "static"]

    # Set the STATIC_ROOT for local development (this will be used by `collectstatic`)
    STATIC_ROOT = BASE_DIR / "staticfiles"

    # Static files storage with WhiteNoise for Heroku
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap'
print(STATIC_URL)

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default Primary Key Field Type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication Settings
AUTH_USER_MODEL = 'accounts.UserBase'
LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'
LOGIN_REDIRECT_URL = 'custom_login_redirect'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'id'
ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Logging
if LOG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'app.log',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }