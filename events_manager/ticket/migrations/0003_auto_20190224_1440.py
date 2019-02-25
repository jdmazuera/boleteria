# Generated by Django 2.1.5 on 2019-02-24 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20190224_1353'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='name',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, verbose_name='Fecha'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='estado',
            field=models.CharField(choices=[('Activa', 'Activa'), ('Anulada', 'Anulada')], default='Activa', error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, max_length=250, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='event',
            field=models.ForeignKey(error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, on_delete=django.db.models.deletion.CASCADE, related_name='event_ticket', to='event.Event', verbose_name='Evento'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.FloatField(error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='propietario',
            field=models.ForeignKey(error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='propietario', to=settings.AUTH_USER_MODEL),
        ),
    ]
