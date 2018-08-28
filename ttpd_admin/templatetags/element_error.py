# element_error.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django import template

register = template.Library()

@register.inclusion_tag('ttpd_admin/form_error_message.html')
def element_error(form, field):
    return {'errors': form[field].errors}


