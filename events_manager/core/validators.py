from django.core.exceptions import ValidationError

def validator_greater_zero(value):
    if value < 0:
        raise ValidationError(
            'El Valor Debe Ser Mayor A 0'
        )