from django.db import connection
from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def setup_postgres(connection, **kwargs):
    if connection.vendor == 'postgresql':
        with connection.cursor() as cursor:
            cursor.execute("SET TIME ZONE 'UTC'")