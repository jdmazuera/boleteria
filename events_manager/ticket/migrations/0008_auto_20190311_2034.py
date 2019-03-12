# Generated by Django 2.1.5 on 2019-03-12 01:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import events_manager.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0005_auto_20190311_2034'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('receipt', '0001_initial'),
        ('ticket', '0007_ticket_fecha_compra'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='date',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='estado',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='event',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='fecha_compra',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='iva',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='metodo_pago',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='propietario',
        ),
        migrations.AddField(
            model_name='ticket',
            name='creation_date',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True, verbose_name='Fecha De Creación'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='event_locality',
            field=models.ForeignKey(error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='event_locality', to='event.EventLocality', verbose_name='Localidad Evento'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='quantity',
            field=models.IntegerField(default=0, validators=[events_manager.core.validators.validator_greater_zero], verbose_name='Cantidad'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='receipt',
            field=models.ForeignKey(error_messages={'blank': 'El Campo No Puede Estar En Blanco', 'invalid': 'El Valor No Es Valido', 'invalid_choice': 'Opcion No Valida', 'unique': 'El Ticket Debe Ser Unico'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='receipt.Receipt', verbose_name='Factura'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='tax',
            field=models.FloatField(default=0, validators=[events_manager.core.validators.validator_greater_zero], verbose_name='Impuesto'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='total',
            field=models.FloatField(default=0, validators=[events_manager.core.validators.validator_greater_zero], verbose_name='Total'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='user_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario Creador'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='price',
            field=models.FloatField(default=0, validators=[events_manager.core.validators.validator_greater_zero], verbose_name='Precio'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='subtotal',
            field=models.FloatField(default=0, validators=[events_manager.core.validators.validator_greater_zero], verbose_name='Subtotal'),
        ),
    ]