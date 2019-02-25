# Generated by Django 2.1.5 on 2019-02-25 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20190224_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='metodo_pago',
            field=models.CharField(choices=[('Activa', 'Activa'), ('Anulada', 'Anulada')], default='Efectivo', error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, max_length=250, verbose_name='Metodo De Pago'),
        ),
    ]