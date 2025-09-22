# Sentry Configuration

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sentry',
        'USER': 'sentry',
        'PASSWORD': 'sentry123',
        'HOST': 'supabase-db',
        'PORT': '5432',
    }
}

# Redis configuration
REDIS_HOST = 'redis'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''

# Cache configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}

# Security configuration
SECRET_KEY = 'supersecretkeyforsentry'
SENTRY_URL_PREFIX = 'http://sentry.osint.local'
SENTRY_WEB_HOST = '0.0.0.0'
SENTRY_WEB_PORT = 9000
SENTRY_WEB_OPTIONS = {
    'workers': 3,
    'limit_request_line': 0,
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_PASSWORD = 'sentryemailpassword'
EMAIL_HOST_USER = 'sentry@osint.local'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = 'sentry@osint.local'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/sentry/sentry.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console', 'file'],
    },
    'loggers': {
        'sentry': {
            'level': 'INFO',
        },
        'sentry.errors': {
            'handlers': ['console'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# System configuration
SYSTEM_URL = 'http://sentry.osint.local'
SENTRY_FEATURES = {
    'auth:register': True,
}

# Performance configuration
SENTRY_RATELIMITER = 'sentry.ratelimits.redis.RedisRateLimiter'
SENTRY_BUFFER = 'sentry.buffer.redis.RedisBuffer'
SENTRY_QUOTAS = 'sentry.quotas.redis.RedisQuota'
SENTRY_TSDB = 'sentry.tsdb.redis.RedisTSDB'

# File storage configuration
SENTRY_FILESTORE = 'django.core.files.storage.FileSystemStorage'
SENTRY_FILESTORE_OPTIONS = {
    'location': '/var/lib/sentry/files',
}

# Timezone configuration
TIME_ZONE = 'UTC'
USE_TZ = True

# Internationalization
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = '/var/lib/sentry/static'

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/lib/sentry/media'

# Session configuration
SESSION_COOKIE_AGE = 1209600  # 2 weeks
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = 'sentrysid'
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_SECURE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = False