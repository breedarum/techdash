# dynamic_element_error.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django import template

register = template.Library()

@register.inclusion_tag('ttpd_admin/form_error_message.html')
def dynamic_element_error(form, prefix, el_type, suffix):
    form_key = f"{prefix}{el_type}{suffix}"

    return {'errors': form[form_key].errors}


