# dynamic_inline_formset.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django import template

register = template.Library()

@register.inclusion_tag('ttpd_admin/readiness_inline_formset.html', takes_context=True)
def readiness_inline_formset(context, prefix, formset_id, label=None):
    context_key = f"{prefix}{formset_id}"

    context_dict = {
      'formset': context[context_key],
      'custom_label': 'Enable?'
    }

    if label is not None:
        context_dict['custom_label'] = label

    return context_dict


