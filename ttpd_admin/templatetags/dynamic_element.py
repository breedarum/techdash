# dynamic_element.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django import template

register = template.Library()

@register.simple_tag
def dynamic_element(form, prefix, el_type, suffix, *args, **kwargs):
    path = kwargs.get('path')
    form_key = f"{prefix}{el_type}{suffix}"

    if path == 'label_tag':
        return form[form_key].label_tag()

    if path == 'label':
        return form[form_key].label

    if path == 'id_for_label':
        return form[form_key].id_for_label

    return form[form_key]


