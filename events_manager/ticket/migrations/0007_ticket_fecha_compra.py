# Generated by Django 2.1.5 on 2019-02-27 01:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_auto_20190224_2127'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='fecha_compra',
            field=models.DateField(default=django.utils.timezone.now, error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, verbose_name='Fecha Compra'),
        ),
    ]
