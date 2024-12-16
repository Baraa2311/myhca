from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Load environment variables from a .env file (for local development)
load_dotenv()

ENVIRONMENT = 'production'  # Should be set based on your environment (production or local)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')  # Ensure you have the correct key in your .env

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Allowed hosts for deployment (can add multiple)
ALLOWED_HOSTS = ['ALLOWED_HOSTS', 'hca.up.railway.app','localhost','127.0.0.1']

CSRF_TRUSTED_ORIGINS=['https://https://hca.up.railway.app/']

# Application definition
INSTALLED_APPS = [
    'accounts.apps.AccountsConfig',
    'clinic.apps.ClinicConfig',
    'admin_panel.apps.AdminPanelConfig',
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
]

CRISPY_TEMPLATE_PACK = 'bootstrap'

# Set the LOGIN_REDIRECT_URL for post-login redirection
LOGOUT_REDIRECT_URL = "home"
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

# Email settings (use a proper backend for production)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Change for production

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

# Database configuration using dj-database-url
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,  # Optional, sets the maximum connection lifetime in seconds
        ssl_require=True,  # Optional, enables SSL connection if required
    )
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

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # BASE_DIR refers to the root of your project

# Static files storage with WhiteNoise for Heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Allauth URL settings
LOGIN_URL = 'account:login'
LOGOUT_URL = 'account:logout'

# The `django-allauth` adapters for customization
ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

# Ensure we're using email for authentication
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Don't require username, use email instead
ACCOUNT_USERNAME_REQUIRED = False

# Ensure email is required
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'  # Ensure email is verified

# Log in the user after email confirmation
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Redirect after logout
ACCOUNT_LOGOUT_REDIRECT_URL = '/'

# The `django-allauth` settings for authenticated user redirection
ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/'  # Redirect to home after login

# Ensure username is not required (use email for login)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # Don't use username

WSGI_APPLICATION = 'h.wsgi.application'