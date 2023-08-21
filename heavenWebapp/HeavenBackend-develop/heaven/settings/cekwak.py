from .base import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "heaven",
        "USER": "heaven",
        "PASSWORD": "mysql",
        "HOST": "BOOK-M6KATB2GGT.local",
        "PORT": "3306",
        "OPTIONS": {"init_command": 'SET sql_mode="STRICT_TRANS_TABLES"'},
    }
}
