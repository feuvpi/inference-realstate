from .settings import *

# Development-specific settings
DEBUG = True

# More permissive CORS for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development (prints to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Cache backend for development (dummy cache)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Development-specific logging
LOGGING['handlers']['file']['level'] = 'DEBUG'
LOGGING['loggers']['property_valuation']['level'] = 'DEBUG'