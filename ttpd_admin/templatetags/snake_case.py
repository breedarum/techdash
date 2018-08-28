# snake_case.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django.template.defaulttags import register
from stringcase import snakecase

@register.filter
def snake_case(value):
    return snakecase(value)


