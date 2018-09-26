# asset_inline_formset.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from django import template

register = template.Library()

@register.inclusion_tag('ttpd_admin/description_inline_formset.html', takes_context=True)
def description_inline_formset(context, prefix, formset_id):
    context_key = f"{prefix}{formset_id}"

    return {
      'formset': context[context_key]
    }


