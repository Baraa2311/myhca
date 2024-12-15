


from pathlib import Path

import os



# Build paths inside the project like this: BASE_DIR / 'subdir'.

BASE_DIR = Path(__file__).resolve().parent.parent





# Quick-start development settings - unsuitable for production

# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/



# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = 'django-insecure-z8oj8oxyyly@f0#bs5iq3!4f!x^7h$5tsfu34pyxd)qeca)lob'



# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True



ALLOWED_HOSTS = []





# Application definition



INSTALLED_APPS = [

# my apps
   'accounts.apps.AccountsConfig',

    'clinic.apps.ClinicConfig',

    'admin_panel.apps.AdminPanelConfig',

    'medical_records.apps.MedicalRecordsConfig',
    
    'coms.apps.ComsConfig',
    
    'appointments.apps.AppointmentsConfig',
    
    'doctor_panel.apps.DoctorPanelConfig',
    
    'diagnostics_and_prescriptions.apps.DiagnosticsAndPrescriptionsConfig',


    # Other apps

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

CRISPY_TEMPLATE_PACK = 'bootstrap?'

# Set the LOGIN_REDIRECT_URL for post-login redirection

LOGOUT_REDIRECT_URL = "home"

SITE_ID = 1





AUTHENTICATION_BACKENDS = ("django.contrib.auth.backends.ModelBackend",

                           "allauth.account.auth_backends.AuthenticationBackend", )

# newspaper_project/settings.py

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



ACCOUNT_SESSION_REMEMBER = True  # new



MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.cache.UpdateCacheMiddleware',

    # Add allauth-specific middleware

    'allauth.account.middleware.AccountMiddleware',

    'django.middleware.common.BrokenLinkEmailsMiddleware',

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





# Database

# https://docs.djangoproject.com/en/5.1/ref/settings/#databases



DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}





# Password validation

# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators



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

# https://docs.djangoproject.com/en/5.1/topics/i18n/



LANGUAGE_CODE = 'en-us'



TIME_ZONE = 'UTC'



USE_I18N = True



USE_TZ = True





AUTH_USER_MODEL = 'accounts.UserBase'

# Static files (CSS, JavaScript, Images)

# https://docs.djangoproject.com/en/5.1/howto/static-files/



STATIC_URL = 'static/'

STATICFILES_DIRS = [BASE_DIR / "static"]  # new



# Default primary key field type

# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





# Configure the account settings for django-





# Allauth URL settings (you can modify this to match your app structure)

LOGIN_URL = 'account:login'

LOGOUT_URL = 'account:logout'



# The `django-allauth` adapters for customization

ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'



ACCOUNT_USER_MODEL_USERNAME_FIELD = 'name'

ACCOUNT_USERNAME_REQUIRED = False  # new



ACCOUNT_EMAIL_REQUIRED = True  # new





# Set the LOGIN_REDIRECT_URL for post-login redirection

LOGIN_REDIRECT_URL = 'custom_login_redirect'



# Configure the account settings for django-allauth

ACCOUNT_AUTHENTICATED_REDIRECT_URL = '/'  # Redirect to home after login

# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False  # Use ID as the username



ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # Ensure username isn't used

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

ACCOUNT_LOGOUT_REDIRECT_URL = '/'



# Specify your custom user model here

AUTH_USER_MODEL = 'accounts.UserBase'



# Allauth URL settings (you can modify this to match your app structure)

LOGIN_URL = 'account:login'

LOGOUT_URL = 'account:logout'



# The `django-allauth` adapters for customization

ACCOUNT_ADAPTER = 'accounts.adapters.CustomAccountAdapter'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'id'


