# Generated by Django 2.1.5 on 2019-03-16 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event_locality', '0006_auto_20190315_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlocality',
            name='locality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='locality', to='locality.Locality', verbose_name='Localidad'),
        ),
    ]
