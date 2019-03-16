# Generated by Django 2.1.5 on 2019-03-16 02:56

from django.conf import settings
from django.db import migrations
import django.db.models.deletion
import django_currentuser.db.models.fields
import django_currentuser.middleware


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_auto_20190313_1226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='user_creator',
            field=django_currentuser.db.models.fields.CurrentUserField(default=django_currentuser.middleware.get_current_authenticated_user, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creador'),
        ),
    ]
