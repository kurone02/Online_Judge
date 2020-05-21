def validate_statement_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extension = '.pdf'
    if not ext.lower() in valid_extension:
        raise ValidationError('Unsupported file extension!')