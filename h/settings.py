from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv
import os

# Load environment variables from a .env file (for local development)
load_dotenv()

MAILJET_API_KEY = os.getenv('MAILJET_API_KEY')
MAILJET_API_SECRET = os.getenv('MAILJET_API_SECRET')

USE_MAILJET = os.getenv('USE_MAILJET', 'False') == 'True'

print(USE_MAILJET)

if USE_MAILJET:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'in-v3.mailjet.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = MAILJET_API_KEY  # Use the Mailjet API key as the username
    EMAIL_HOST_PASSWORD = MAILJET_API_SECRET  # Use the Mailjet API secret as the password
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # This will print the email to the console





ENVIRONMENT = 'production'  # Should be set based on your environment (production or local)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # Ensure you have the correct key in your .env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'
LOG = os.getenv('LOG', 'False') == 'True'

# Allowed hosts for deployment (can add multiple)
ALLOWED_HOSTS = ['ALLOWED_HOSTS', 'hca.up.railway.app','localhost','127.0.0.1']

CSRF_TRUSTED_ORIGINS=['https://https://hca.up.railway.app/']

# Application definition
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'clinic.apps.ClinicConfig',
    'medical_records.apps.MedicalRecordsConfig',
    'coms.apps.ComsConfig',
    'appointments.apps.AppointmentsConfig',
    'doctor_panel.apps.DoctorPanelConfig',
    'diagnostics_and_prescriptions.apps.DiagnosticsAndPrescriptionsConfig',

    'phonenumber_field',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'storages',
 
    ]

CRISPY_TEMPLATE_PACK = 'bootstrap'

# Set the LOGIN_REDIRECT_URL for post-login redirection
LOGOUT_REDIRECT_URL = "home"
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)



ACCOUNT_SESSION_REMEMBER = True  # Enable session remember

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

ROOT_URLCONF = 'h.urls'

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
            ],
        },
    },
]




STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Path for collected static files

# Determine if the app is in production or development
ENVIRONMENT=os.getenv('ENVIRONMENT')
if ENVIRONMENT == 'production':
    DATABASES = {
        'default': dj_database_url.config(
            default=os.getenv('DATABASE_URL'),
            conn_max_age=600,  # Optional, sets the maximum connection lifetime in seconds
            ssl_require=True,  # Optional, enables SSL connection if required
        )
    }
else:  # Development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'local_db_name'),  # Replace with your local database name
            'USER': os.getenv('DB_USER', 'local_user'),  # Replace with your local database user
            'PASSWORD': os.getenv('DB_PASSWORD', 'local_password'),  # Replace with your local database password
            'HOST': os.getenv('DB_HOST', 'localhost'),  # Local database host
            'PORT': os.getenv('DB_PORT', '5432'),  # Local database port
        }
    }



# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



# Custom user model
AUTH_USER_MODEL = 'accounts.UserBase'

USE_AWS3 = os.getenv('USE_AWS3', 'False') == 'True'


if USE_AWS3:
    # AWS Credentials
    AWS_ACCESS_KEY_ID =     os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', default='us-east-1')  # Specify your region
    AWS_QUERYSTRING_AUTH = False  # Makes files publicly accessible via a URL
    # Storage settings
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # Media files
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'   # Static files

    # Static and media URLs
    STATIC_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/static/'
    MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/media/'
else:
    # Static files (CSS, JavaScript, Images)
    STATIC_URL = 'static/'

    STATICFILES_DIRS = [BASE_DIR / "static"] 

    # Static files storage with WhiteNoise for Heroku
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth URL settings
LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'

# The `django-allauth` adapters for customization
ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'




# Don't require username, use id instead
ACCOUNT_USERNAME_REQUIRED = False

# Ensure email is required
ACCOUNT_EMAIL_REQUIRED = True

# Log in the user after email confirmation
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Redirect after logout
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# The `django-allauth` settings for authenticated user redirection
ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/'  # Redirect to home after login

# Ensure username is not required (use email for login)
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'id'
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

WSGI_APPLICATION = 'h.wsgi.application'