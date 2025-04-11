from django.core.management import call_command
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "OnlineStore.settings")  
django.setup()

with open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", "--indent", "2", stdout=f)