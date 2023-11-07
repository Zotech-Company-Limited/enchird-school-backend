import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_password(password):
    """Docstring for function."""
    if len(password) < 8:
        raise ValidationError(
            _("The password must be at least 8 characters"),
            code='password_no_length')

    if not re.findall('\d', password):
        raise ValidationError(
            _("The password must contain at least 1 digit, 0-9."),
            code='password_no_number',
        )

    if not re.findall('[A-Z]', password):
        raise ValidationError(
            _("The password must contain at least 1 uppercase letter, A-Z."),
            code='password_no_upper',
        )

    if not re.findall('[a-z]', password):
        raise ValidationError(
            _("The password must contain at least 1 lowercase letter, a-z."),
            code='password_no_lower',
        )

    if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        raise ValidationError(
            _("The password must contain at least one symbol" +
              "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
            code='password_no_symbol',
        )

    return password



