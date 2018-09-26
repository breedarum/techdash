# admin.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from functools import update_wrapper
from django.contrib import admin
# from django.contrib.auth.models import Group, User
# from django.contrib.auth.admin import GroupAdmin, UserAdmin
from ttpd_admin import urls
from .forms import AdminAuthenticationForm
from .views import (
  TechnologiesList
)

def wrap_perms(admin_site, view, cacheable=False):
    def wrapper(*args, **kwargs):
        return admin_site.admin_view(view, cacheable)(*args, **kwargs)

    wrapper.admin_site = admin_site
    return update_wrapper(wrapper, view)

class TtpdAdmin(admin.AdminSite):
    site_header = 'TTPD'
    site_title = 'TTPD Administration'
    index_title = 'TTPD Administration'
    index_template = 'ttpd_admin/technologies/index.html'
    login_form = AdminAuthenticationForm
    login_template = 'ttpd_admin/login.html'
    logout_template = 'ttpd_admin/logout.html'

    def __init__(self, name='admin'):
        admin.AdminSite.__init__(self, name=name)

    def get_urls(self):
        from django.conf.urls import url, include
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        # and django.contrib.contenttypes.views imports ContentType.
        from django.contrib.contenttypes import views as contenttype_views

        # Admin-site-wide views.
        urlpatterns = [
          url(r'^$', TechnologiesList.as_view(), name='index'),
          # url(r'^$', TechnologiesList.as_view(), name='technologies_list'),
          url(r'^login/$', self.login, name='login'),
          url(r'^logout/$', wrap_perms(self, self.logout), name='logout'),
          url(r'^password_change/$', wrap_perms(self, self.password_change, cacheable=True), name='password_change'),
          url(r'^password_change/done/$', wrap_perms(self, self.password_change_done, cacheable=True),
              name='password_change_done'),
          url(r'^jsi18n/$', wrap_perms(self, self.i18n_javascript, cacheable=True), name='jsi18n'),
          url(r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$', wrap_perms(self, contenttype_views.shortcut),
              name='view_on_site'),
        ]

        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
              url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
            ]

            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r'^(?P<app_label>' + '|'.join(valid_app_labels) + ')/$'
            urlpatterns += [
              url(regex, wrap_perms(self, self.app_index), name='app_list'),
            ]

        # return the dynamically assembled urls as well as the url patterns from the urls.py
        return urlpatterns + urls.urlpatterns

site = TtpdAdmin(name='ttpd_admin')

# class TechnologiesAdmin(admin.ModelAdmin):
#     fieldsets = (
#       (None, {
#         'fields': ('name', 'year', 'description', 'protection_level', 'est_ownership_cost', 'commercialization_mode'),
#       }),
#     )

#     # Custom templates (designed to be over-ridden in subclasses)
#     add_form_template = 'ttpd_admin/change_form.html'
#     # change_form_template = None
#     # change_list_template = None
#     # delete_confirmation_template = None
#     # delete_selected_confirmation_template = None
#     # object_history_template = None
#     # popup_response_template = None

# site.register(Group, GroupAdmin)
# site.register(User, UserAdmin)
# site.register(models.AgencyTypes)
# site.register(models.Agencies)
# site.register(models.CommercializationModes)
# site.register(models.Commodities)
# site.register(models.IndustrySectors)
# site.register(models.PotentialAdopters)
# site.register(models.ProtectionLevels)
# site.register(models.ProtectionTypes)
# site.register(models.TechCategories)
# site.register(models.TechStatus)
# site.register(models.TechnologyFundingTypes)
# site.register(models.TechnologyFundings)
# site.register(models.TechnologyGenerators)
# site.register(models.TechnologyProtectionStatus)
# site.register(models.Technologies, TechnologiesAdmin)


