# element_error.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django import template

register = template.Library()

@register.inclusion_tag('ttpd_admin/non_form_error_message.html', takes_context=True)
def non_element_error(context):
    return {'errors': context['form'].non_field_errors}


