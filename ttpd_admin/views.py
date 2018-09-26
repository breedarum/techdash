# views.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

import json
import base64
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import edit, ListView, DetailView
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.template.defaultfilters import slugify
from django.contrib.admin.models import ADDITION, CHANGE, DELETION, LogEntry
from django.contrib.contenttypes.models import ContentType
from rolepermissions.roles import assign_role, get_user_roles, remove_role
from rolepermissions.mixins import HasPermissionsMixin, HasRoleMixin
from stringcase import snakecase
from ttpd.roles import *
from .forms import (
  UsersForm,
  TechnologyForm,
  TechnologyReadinessStatusFormSet,
  TechnologyIpProtectionMetadataFormSet,
  TradeSecretIpProtectionFormSet,
  TechnologyFundingsFormSet,
  TechnologyAssetsFormSet,
  TechnologyFullDescriptionFormSet,
  UsersUpdateForm
)
from .models import (
  Industries,
  Sectors,
  ISPs,
  ProtectionTypes,
  ProtectionLevels,
  PotentialAdopters,
  AdopterTypes,
  Adopters,
  FundingTypes,
  AgencyTypes,
  Agencies,
  TechStatus,
  Generators,
  TechCategories,
  FundingTypes,
  TechStatus,
  Technologies,
  TechnologyIndustrySectorISPs,
  TechnologyCategories,
  TechnologyGenerators,
  TechnologyOwners,
  TechnologyAdopters,
  TechnologyPotentialAdopters,
  TechnologyProtectionTypes,
  TechnologyProtectionStatus,
  TechProtectionTypesMetadata,
  TechnologyStatuses,
  TechnologyAssets,
  TechnologyAssetTypes,
  TechnologyFullDescription,
  TechnologyFullDescriptionTypes,
  Fundings,
  FundingImplementors,
  User
)

class BaseAdminView(LoginRequiredMixin):
    """
    Base class for implementing reusable admin features across all admin views
    """
    login_url = reverse_lazy('ttpd_admin:login')

class LoggedCreateView(edit.CreateView):

    def post(self, request, *args, **kwargs):
        response = super(LoggedCreateView, self).post(request, *args, **kwargs)

        # log the user activity after a successful operation
        form = self.get_form()
        if form.is_valid():
            content_type = ContentType.objects.get_for_model(self.model)

            LogEntry.objects.log_action(
              request.user.id,
              content_type.id,
              self.object.id,
              str(self.object),
              ADDITION,
              f"Created {str(self.object)}"
            )

        return response

class LoggedUpdateView(edit.UpdateView):

    def post(self, request, *args, **kwargs):
        old_model_item = self.get_object()
        old_model_item_name = str(old_model_item)

        response = super(LoggedUpdateView, self).post(request, *args, **kwargs)

        # log the user activity after a successful operation
        form = self.get_form()
        if form.is_valid():
            content_type = ContentType.objects.get_for_model(self.model)

            LogEntry.objects.log_action(
              request.user.id,
              content_type.id,
              self.object.id,
              str(self.object),
              CHANGE,
              f"Updated {old_model_item_name} to {str(self.object)}"
            )

        return response

class LoggedDeleteView(edit.DeleteView):

    def post(self, request, *args, **kwargs):
        deleted_item = self.get_object()

        response = super(LoggedDeleteView, self).post(request, *args, **kwargs)

        # log the user activity after a successful operation
        if isinstance(response, HttpResponseRedirect):
            content_type = ContentType.objects.get_for_model(self.model)

            LogEntry.objects.log_action(
            request.user.id,
            content_type.id,
            None,
            str(deleted_item),
            DELETION,
            f"Deleted {str(deleted_item)}"
            )

        return response

class ActivityLogsList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = LogEntry
    template_name = 'ttpd_admin/activity-logs/index.html'
    paginate_by = 20

class IndustriesList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = Industries
    template_name = 'ttpd_admin/industries/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context

class IndustriesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = Industries
    fields = ['name']
    template_name = 'ttpd_admin/industries/form.html'
    success_url = reverse_lazy('ttpd_admin:industries_list')

class IndustriesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = Industries
    fields = ['name']
    template_name = 'ttpd_admin/industries/form.html'
    success_url = reverse_lazy('ttpd_admin:industries_list')

class IndustriesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = Industries
    template_name = 'ttpd_admin/industries/delete.html'
    success_url = reverse_lazy('ttpd_admin:industries_list')

class SectorsList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = Sectors
    template_name = 'ttpd_admin/industries-sectors/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class SectorsCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = Sectors
    fields = ['name', 'parent']
    template_name = 'ttpd_admin/industries-sectors/form.html'
    success_url = reverse_lazy('ttpd_admin:sectors_list')

class SectorsUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = Sectors
    fields = ['name', 'parent']
    template_name = 'ttpd_admin/industries-sectors/form.html'
    success_url = reverse_lazy('ttpd_admin:sectors_list')

class SectorsDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = Sectors
    template_name = 'ttpd_admin/industries-sectors/delete.html'
    success_url = reverse_lazy('ttpd_admin:sectors_list') 

class ISPsList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = ISPs
    template_name = 'ttpd_admin/industries-isp/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class ISPsCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = ISPs
    fields = ['name', 'parent', 'specific_commodity']
    template_name = 'ttpd_admin/industries-isp/form.html'
    success_url = reverse_lazy('ttpd_admin:isps_list')

class ISPsUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = ISPs
    fields = ['name', 'parent', 'specific_commodity']
    template_name = 'ttpd_admin/industries-isp/form.html'
    success_url = reverse_lazy('ttpd_admin:isps_list')

class ISPsDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = ISPs
    template_name = 'ttpd_admin/industries-isp/delete.html'
    success_url = reverse_lazy('ttpd_admin:isps_list') 
  
class ProtectionTypesList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = ProtectionTypes
    template_name = 'ttpd_admin/protection-types/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class ProtectionTypesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = ProtectionTypes
    fields = ['name']
    template_name = 'ttpd_admin/protection-types/form.html'
    success_url = reverse_lazy('ttpd_admin:protection_types_list')

class ProtectionTypesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = ProtectionTypes
    fields = ['name']
    template_name = 'ttpd_admin/protection-types/form.html'
    success_url = reverse_lazy('ttpd_admin:protection_types_list')

class ProtectionTypesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = ProtectionTypes
    template_name = 'ttpd_admin/protection-types/delete.html'
    success_url = reverse_lazy('ttpd_admin:protection_types_list')  

class FundingTypesList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = FundingTypes
    template_name = 'ttpd_admin/funding-types/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class FundingTypesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = FundingTypes
    fields = ['name']
    template_name = 'ttpd_admin/funding-types/form.html'
    success_url = reverse_lazy('ttpd_admin:funding_types_list')

class FundingTypesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = FundingTypes
    fields = ['name']
    template_name = 'ttpd_admin/funding-types/form.html'
    success_url = reverse_lazy('ttpd_admin:funding_types_list')

class FundingTypesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = FundingTypes
    template_name = 'ttpd_admin/funding-types/delete.html'
    success_url = reverse_lazy('ttpd_admin:funding_types_list')

class PotentialAdoptersList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = PotentialAdopters
    template_name = 'ttpd_admin/adopters-potential/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class PotentialAdoptersCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = PotentialAdopters
    fields = ['name', 'adopter_type']
    template_name = 'ttpd_admin/adopters-potential/form.html'
    success_url = reverse_lazy('ttpd_admin:potential_adopters_list')

class PotentialAdoptersUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = PotentialAdopters
    fields = ['name', 'adopter_type']
    template_name = 'ttpd_admin/adopters-potential/form.html'
    success_url = reverse_lazy('ttpd_admin:potential_adopters_list')

class PotentialAdoptersDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = PotentialAdopters
    template_name = 'ttpd_admin/adopters-potential/delete.html'
    success_url = reverse_lazy('ttpd_admin:potential_adopters_list')  

class AdopterTypesList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = AdopterTypes
    template_name = 'ttpd_admin/adopter-types/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class AdopterTypesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = AdopterTypes
    fields = ['name']
    template_name = 'ttpd_admin/adopter-types/form.html'
    success_url = reverse_lazy('ttpd_admin:adopter_types_list')

class AdopterTypesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = AdopterTypes
    fields = ['name']
    template_name = 'ttpd_admin/adopter-types/form.html'
    success_url = reverse_lazy('ttpd_admin:adopter_types_list')

class AdopterTypesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = AdopterTypes
    template_name = 'ttpd_admin/adopter-types/delete.html'
    success_url = reverse_lazy('ttpd_admin:adopter_types_list')  

class AdoptersList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = Adopters
    template_name = 'ttpd_admin/adopters/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class AdoptersCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = Adopters
    fields = ['name', 'address', 'phone_number', 'fax_number', 'email_address', 'adopter_type']
    template_name = 'ttpd_admin/adopters/form.html'
    success_url = reverse_lazy('ttpd_admin:adopters_list')

class AdoptersUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = Adopters
    fields = ['name', 'address', 'phone_number', 'fax_number', 'email_address', 'adopter_type']
    template_name = 'ttpd_admin/adopters/form.html'
    success_url = reverse_lazy('ttpd_admin:adopters_list')

class AdoptersDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = Adopters
    template_name = 'ttpd_admin/adopters/delete.html'
    success_url = reverse_lazy('ttpd_admin:adopters_list')  

    allowed_roles = [Admin]

class AgencyTypesList(BaseAdminView, HasRoleMixin, ListView):
    model = AgencyTypes
    template_name = 'ttpd_admin/agency-types/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class AgencyTypesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = AgencyTypes
    fields = ['name']
    template_name = 'ttpd_admin/agency-types/form.html'
    success_url = reverse_lazy('ttpd_admin:agencies_list')

class AgencyTypesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = AgencyTypes
    fields = ['name']
    template_name = 'ttpd_admin/agency-types/form.html'
    success_url = reverse_lazy('ttpd_admin:agencies_list')

class AgencyTypesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = AgencyTypes
    template_name = 'ttpd_admin/agency-types/delete.html'
    success_url = reverse_lazy('ttpd_admin:agencies_list')  

class AgenciesList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = Agencies
    template_name = 'ttpd_admin/agencies/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class AgenciesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = Agencies
    fields = ['name', 'agency_type', 'address', 'phone_number', 'fax_number', 'private_flag']
    template_name = 'ttpd_admin/agencies/form.html'
    success_url = reverse_lazy('ttpd_admin:agencies_list')

class AgenciesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = Agencies
    fields = ['name', 'agency_type', 'address', 'phone_number', 'fax_number', 'private_flag']
    template_name = 'ttpd_admin/agencies/form.html'
    success_url = reverse_lazy('ttpd_admin:agencies_list')

class AgenciesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = Agencies
    template_name = 'ttpd_admin/agencies/delete.html'
    success_url = reverse_lazy('ttpd_admin:agencies_list')  

class GeneratorsList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = Generators
    template_name = 'ttpd_admin/generators/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context
        
class GeneratorsCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    model = Generators
    fields = ['title', 'first_name', 'middle_name', 'last_name', 'availability', 'agency', 'expertise']
    template_name = 'ttpd_admin/generators/form.html'
    success_url = reverse_lazy('ttpd_admin:generators_list')

class GeneratorsUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = Generators
    fields = ['title', 'first_name', 'middle_name', 'last_name', 'availability', 'agency', 'expertise']
    template_name = 'ttpd_admin/generators/form.html'
    success_url = reverse_lazy('ttpd_admin:generators_list')

class GeneratorsDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = Generators
    template_name = 'ttpd_admin/generators/delete.html'
    success_url = reverse_lazy('ttpd_admin:generators_list')  

class TechCategoriesList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = TechCategories
    template_name = 'ttpd_admin/technology-categories/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context

class TechCategoriesCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    allowed_roles = [Admin]
    model = TechCategories
    fields = ['name', 'parent']
    template_name = 'ttpd_admin/technology-categories/form.html'
    success_url = reverse_lazy('ttpd_admin:tech_categories_list')

class TechCategoriesUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = TechCategories
    fields = ['name', 'parent']
    template_name = 'ttpd_admin/technology-categories/form.html'
    success_url = reverse_lazy('ttpd_admin:tech_categories_list')

class TechCategoriesDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = TechCategories
    template_name = 'ttpd_admin/technology-categories/delete.html'
    success_url = reverse_lazy('ttpd_admin:tech_categories_list')

class TechnologiesList(BaseAdminView, HasPermissionsMixin, ListView):
    required_permission = 'list_technologies'
    model = Technologies
    template_name = 'ttpd_admin/technologies/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context

class TechnologiesDetails(BaseAdminView, HasPermissionsMixin, DetailView):
    required_permission = 'list_technologies'
    model = Technologies 
    fields = [
          'name',
          'region',
          'categories',
          'industry_sector_isps',
          'protection_level',
          'year',
          'description',
          'owners',
          'generators',
          'adopters',
          'potential_adopters',
          'fundings',
          'statuses',

        ]
    template_name = 'ttpd_admin/technologies/details.html'

    def get_context_data(self, **kwargs):
        context = super(TechnologiesDetails, self).get_context_data(**kwargs)

        instance = self.get_object()
        context['industry_sector_isps'] = instance.industry_sector_isps.all()
        context['categories'] = instance.categories.all()
        context['owners'] = instance.owners.all()
        context['generators'] = instance.generators.all()
        context['adopters'] = instance.adopters.all()
        context['potential_adopters'] = instance.potential_adopters.all()
        context['protection_types'] = TechnologyProtectionTypes.objects.filter(technology=instance.id)
        context['fundings'] = instance.fundings.all()
        status_metadata = TechnologyStatuses.objects.filter(technology=instance.id)
        context['techstatuses'] = status_metadata.all();


        return context

class TechnologiesCreate(BaseAdminView, HasPermissionsMixin, LoggedCreateView):
    required_permission = 'create_technologies'
    model = Technologies
    form_class = TechnologyForm
    template_name = 'ttpd_admin/technologies/form.html'
    success_url = reverse_lazy('ttpd_admin:technologies_list')

    def get_context_data(self, **kwargs):
        context = super(TechnologiesCreate, self).get_context_data(**kwargs)

        # create formsets for status of readiness
        tech_statuses = TechStatus.objects.all()
        context['tech_statuses'] = tech_statuses
        context['tech_statuses_formset_prefix'] = 'tech_status_'

        for tech_status in tech_statuses:
            snake_status = snakecase(slugify(tech_status.name))
            context_key = f"{context['tech_statuses_formset_prefix']}{snake_status}"

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                context[context_key] = TechnologyReadinessStatusFormSet(self.request.POST, prefix=context_key)
            else:
                context[context_key] = TechnologyReadinessStatusFormSet(prefix=context_key)

        # create formsets for assets
        tech_asset_types = TechnologyAssetTypes.objects.all()
        context['tech_asset_types'] = tech_asset_types
        context['tech_assets_formset_prefix'] = 'tech_assets_'
        context['tech_asset_types_ip_protected'] = [
          'Narrative Advantages',
          'Technical Evidences',
          'Economic Evidences',
          'Market Study Summary',
          'Valuation Summary',
          'Freedom to Operate Summary',
          'Proposed Term Sheet',
          'Fairness Opinion Report',
          'Video Clips'
        ]

        for tech_asset_type in tech_asset_types:
            snake_asset_type = snakecase(slugify(tech_asset_type.name))
            context_key = f"{context['tech_assets_formset_prefix']}{snake_asset_type}"

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                context[context_key] = TechnologyAssetsFormSet(
                  self.request.POST,
                  self.request.FILES,
                  prefix=context_key
                )
            else:
                context[context_key] = TechnologyAssetsFormSet(prefix=context_key)

        # create formsets for full-description
        tech_fulldescription_types = TechnologyFullDescriptionTypes.objects.all()
        context['tech_fulldescription_types'] = tech_fulldescription_types
        context['tech_fulldescriptions_formset_prefix'] = 'tech_fulldescription_'

        for tech_fulldescription_type in tech_fulldescription_types:
            snake_fulldescription_type = snakecase(slugify(tech_fulldescription_type.name))
            context_key = f"{context['tech_fulldescriptions_formset_prefix']}{snake_fulldescription_type}"

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                context[context_key] = TechnologyFullDescriptionFormSet(
                  self.request.POST,
                  self.request.FILES,
                  prefix=context_key
                )
            else:
                context[context_key] = TechnologyFullDescriptionFormSet(prefix=context_key)

         # create formsets for technology_funding types
        technology_funding_types = FundingTypes.objects.all()
        context['technology_funding_types'] = technology_funding_types
        context['technology_funding_types_formset_prefix'] = 'tech_funding_'

        for funding_type in technology_funding_types:
            snake_funding_type = snakecase(slugify(funding_type.name))
            context_key = f"{context['technology_funding_types_formset_prefix']}{snake_funding_type}"

            # if the request method is "POST" pass it to the form set.
            # use different form set when the funding type is extension / commercialization
            if self.request.POST:
                context[context_key] = TechnologyFundingsFormSet(self.request.POST, prefix=context_key)

            else:
                context[context_key] = TechnologyFundingsFormSet(prefix=context_key)

        # create formsets for protection types
        # NOTE: since the model looped in this part can be added or revised according to the given document,
        #       some part of this code might not work well and may resolve to the default values!
        protection_types = ProtectionTypes.objects.all()
        context['technology_protection_types'] = protection_types
        context['technology_protection_types_formset_prefix'] = 'tech_prot_'

        protection_status_all_queryset = TechnologyProtectionStatus.objects.all()
        protection_status_no_rev_queryset = TechnologyProtectionStatus.objects.exclude(name='For Revival')

        for protection_type in protection_types:
            snake_protection_type = snakecase(slugify(protection_type.name))
            context_key = f"{context['technology_protection_types_formset_prefix']}{snake_protection_type}"

            # customize the query set to be used depending on the protection type
            protection_status_queryset = protection_status_no_rev_queryset
            if snake_protection_type == 'patent' or snake_protection_type == 'utility_model':
                protection_status_queryset = protection_status_all_queryset

            # customize the label for the meta_serial_number label depending on the protection type
            meta_serial_label = 'Registration Number'
            if snake_protection_type == 'patent':
                meta_serial_label = 'Patent Number'
            elif snake_protection_type == 'plant_variety_protection':
                meta_serial_label = 'PVP Number'

            # assemble the form's kwargs to be passed to the formset
            form_kwargs = {
              'meta_serial_label': meta_serial_label,
              'protection_status_queryset': protection_status_queryset
            }

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                if snake_protection_type != 'trade_secret':
                    context[context_key] = TechnologyIpProtectionMetadataFormSet(
                      self.request.POST,
                      prefix=context_key,
                      queryset=TechProtectionTypesMetadata.objects.none(),
                      form_kwargs=form_kwargs
                    )
                else:
                    context[context_key] = TradeSecretIpProtectionFormSet(
                      self.request.POST,
                      prefix=context_key
                    )
            else:
                if snake_protection_type != 'trade_secret':
                    context[context_key] = TechnologyIpProtectionMetadataFormSet(
                      prefix=context_key,
                      queryset=TechProtectionTypesMetadata.objects.none(),
                      form_kwargs=form_kwargs
                    )
                else:
                    context[context_key] = TradeSecretIpProtectionFormSet(prefix=context_key)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # initialize variable outside the try block to so that we will be able to reference it inside the except block
        technology = None

        # retrieve the protection level
        protection_level = form.cleaned_data.get('protection_level')

        # check if the formsets declared within the form is not valid.
        # if it is, mark the form as invalid immediately
        if not self.inline_formsets_valid(context):
            return super(TechnologiesCreate, self).form_invalid(form)

        # perform an atomic transaction to perfectly sync m2m relationships or rollback all at once when an error occurs
        try:
            try:
                with transaction.atomic():
                    technology = form.save(commit=False)

                    # save the technology
                    technology.save()

                    # save the categories
                    self.save_technology_categories(technology, form.cleaned_data.get('categories'))

                    # save the industry sectors
                    self.save_technology_industry_sector_isp(technology, form.cleaned_data.get('industry_sector_isps'))

                    # save the status of readiness data
                    self.save_status_of_readiness_data(technology, context)

                    # save the generators
                    self.save_technology_generators(technology, form.cleaned_data.get('generators'))

                    # save the owners
                    self.save_technology_owners(technology, form.cleaned_data.get('owners'))

                    # save the potential adopters
                    self.save_potential_adopters(technology, form.cleaned_data.get('potential_adopters'))

                    # save the technology fundings
                    self.save_technology_fundings(technology, context)

                    # restrict file types
                    self.save_assets(technology, context)

                    # restrict file types
                    self.save_full_description(technology, context)

                    # save the adopters and ip protection metadata only if the protection level is IP Protected
                    if protection_level.name.lower() == 'ip protected':
                        self.save_adopters(technology, form.cleaned_data.get('adopters'))
                        self.save_ip_protection_data(technology, context)

                    # store the reference of the technology to the object property
                    self.object = technology # pylint: disable=W0201

            except IntegrityError:
                # re-raise an exception but this time a new instance of different exception
                raise RuntimeError('An unknown error has occurred. Please try again later.')

        except RuntimeError as re:
            if technology is not None:
                technology.delete()

            # add a non-field error to show to the user
            form.add_error(None, re)

            return super(TechnologiesCreate, self).form_invalid(form)

        # since we are manually saving the object, we call the redirect not the parent class' form_valid method.
        return HttpResponseRedirect(self.get_success_url())

    def inline_formsets_valid(self, context):
        valid = True

        for tech_status in context['tech_statuses']:
            snake_status = snakecase(slugify(tech_status.name))
            context_key = f"{context['tech_statuses_formset_prefix']}{snake_status}"
            tech_status_form = context[context_key]

            # check if the inline formsets are valid or not
            if not tech_status_form.is_valid():
                valid = False

                break

        for protection_type in context['technology_protection_types']:
            snake_protection_type = snakecase(slugify(protection_type.name))
            context_key = f"{context['technology_protection_types_formset_prefix']}{snake_protection_type}"
            ip_protection_meta_form = context[context_key]

            # check if the inline formsets are valid or not
            if not ip_protection_meta_form.is_valid():
                valid = False

                break

        for funding_type in context['technology_funding_types']:
            snake_funding_type = snakecase(slugify(funding_type.name))
            context_key = f"{context['technology_funding_types_formset_prefix']}{snake_funding_type}"
            funding_type_form = context[context_key]

            # check if the inline formsets are valid or not
            if not funding_type_form.is_valid():
                valid = False

                break

        for tech_asset_type in context['tech_asset_types']:
            snake_asset_type = snakecase(slugify(tech_asset_type.name))
            context_key = f"{context['tech_assets_formset_prefix']}{snake_asset_type}"
            tech_asset_type_form = context[context_key]

            # check if the inline formsets are valid or not
            if not tech_asset_type_form.is_valid():
                valid = False

        for tech_fulldescription_type in context['tech_fulldescription_types']:
            snake_fulldescription_type = snakecase(slugify(tech_fulldescription_type.name))
            context_key = f"{context['tech_fulldescriptions_formset_prefix']}{snake_fulldescription_type}"
            tech_fulldescription_type_form = context[context_key]

            # check if the inline formsets are valid or not
            if not tech_fulldescription_type_form.is_valid():
                valid = False

        return valid

    def save_adopters(self, technology, cleaned_adopters):
        num_adopters = len(cleaned_adopters)

        if num_adopters > 0:
            adopters = []

            # create m2m adopter instance on the fly
            for adopter in cleaned_adopters:
                adopters.append(
                  TechnologyAdopters(technology=technology, adopter=adopter)
                )

            # add it all at once
            TechnologyAdopters.objects.bulk_create(adopters)

    def save_potential_adopters(self, technology, cleaned_potential_adopters):
        num_potential_adopters = len(cleaned_potential_adopters)

        if num_potential_adopters > 0:
            potential_adopters = []

            # create m2m potential adopter instance on the fly
            for potential_adopter in cleaned_potential_adopters:
                potential_adopters.append(
                  TechnologyPotentialAdopters(technology=technology, potential_adopter=potential_adopter)
                )

            # add it all at once
            TechnologyPotentialAdopters.objects.bulk_create(potential_adopters)

    def save_technology_owners(self, technology, cleaned_owners):
        num_owners = len(cleaned_owners)

        if num_owners > 0:
            owners = []

            # create m2m owner instance on the fly
            for owner in cleaned_owners:
                owners.append(TechnologyOwners(technology=technology, owner=owner))

            # add it all at once
            TechnologyOwners.objects.bulk_create(owners)

    def save_technology_generators(self, technology, cleaned_generators):
        num_generators = len(cleaned_generators)

        if num_generators > 0:
            generators = []

            # create m2m generator instance on the fly
            for generator in cleaned_generators:
                generators.append(TechnologyGenerators(technology=technology, generator=generator))

            # add it all at once
            TechnologyGenerators.objects.bulk_create(generators)

    def save_technology_industry_sector_isp(self, technology, cleaned_industry_sector_isps):
        num_industry_sectors = len(cleaned_industry_sector_isps)

        if num_industry_sectors > 0:
            industry_sector_isps = []

            # create m2m industry sector instance on the fly
            for industry_sector_isp in cleaned_industry_sector_isps:
                industry_sector_isps.append(
                  TechnologyIndustrySectorISPs(technology=technology, industry_sector_isp=industry_sector_isp)
                )

            # add it all at once
            TechnologyIndustrySectorISPs.objects.bulk_create(industry_sector_isps)


    def save_technology_categories(self, technology, cleaned_categories):
        num_categories = len(cleaned_categories)

        if num_categories > 0:
            categories = []

            # create m2m category instance on the fly
            for category in cleaned_categories:
                categories.append(TechnologyCategories(technology=technology, tech_category=category))

            # add it all at once
            TechnologyCategories.objects.bulk_create(categories)

    def save_technology_fundings(self, technology, context):
        technology_funding_implementors = []

        for funding_type in context['technology_funding_types']:
            snake_funding_type = snakecase(slugify(funding_type.name))
            context_key = f"{context['technology_funding_types_formset_prefix']}{snake_funding_type}"
            funding_type_form = context[context_key]

            if funding_type_form.is_valid():
                funding_type_form.instance = technology
                models = funding_type_form.save(commit=False)

                # set the funding type and append it to a list for bulk creation
                for index, funding_type_item in enumerate(models):
                    clean_data_ref = funding_type_form.cleaned_data[index]

                    # add relation to the funding type
                    funding_type_item.funding_type = funding_type

                    # TODO: bulk create does not work since we do need the reference to an existing funding
                    #       which have its pk been already set so we create here in the loop. This can be a
                    #       bottleneck since we are invoking possible multiple insert statements.
                    funding_type_item.save()

                    # create the objects for the implementors
                    for implementing_agency in clean_data_ref.get('implementing_agencies'):
                        technology_funding_implementors.append(
                          FundingImplementors(funding=funding_type_item, implementor=implementing_agency)
                        )

        # add all at once when there is m2m relationships to be created
        num_technology_funding_implementors = len(technology_funding_implementors)
        if num_technology_funding_implementors > 0:
            FundingImplementors.objects.bulk_create(technology_funding_implementors)

    def save_status_of_readiness_data(self, technology, context):
        statuses = []

        for tech_status in context['tech_statuses']:
            snake_status = snakecase(slugify(tech_status.name))
            context_key = f"{context['tech_statuses_formset_prefix']}{snake_status}"
            tech_status_form = context[context_key]

            if tech_status_form.is_valid():
                tech_status_form.instance = technology
                models = tech_status_form.save(commit=False)

                for status_item in models:
                    # add relation to the status of technology
                    status_item.tech_status = tech_status

                    statuses.append(status_item)

        # add all at once when there is m2m relationships to be created
        num_statuses = len(statuses)
        if num_statuses > 0:
            TechnologyStatuses.objects.bulk_create(statuses)

    # NOTE: since the model looped in this part can be added or revised according to the given document,
    #       some part of this code might not work well and may resolve to the default values!
    def save_ip_protection_data(self, technology, context):
        ip_protections = []

        for protection_type in context['technology_protection_types']:
            snake_protection_type = snakecase(slugify(protection_type.name))
            context_key = f"{context['technology_protection_types_formset_prefix']}{snake_protection_type}"
            ip_protection_meta_form = context[context_key]

            if ip_protection_meta_form.is_valid():
                if snake_protection_type == 'trade_secret':
                    for trade_secret_form in ip_protection_meta_form.forms:
                        is_trade_secret = trade_secret_form.cleaned_data.get('is_trade_secret')

                        # create an instance of the protection type if it is trade secret
                        if is_trade_secret is True:
                            ip_protections.append(
                              z(technology=technology, protection_type=protection_type)
                            )

                else:
                    # loop through all the ip protection metadata forms and create necessary objects
                    for meta_form in ip_protection_meta_form.forms:
                        application_num = meta_form.cleaned_data.get('application_number')
                        meta_serial_num = meta_form.cleaned_data.get('meta_serial_number')
                        filing_date = meta_form.cleaned_data.get('date_of_filing')
                        protection_status = meta_form.cleaned_data.get('status')

                        # create the object if all of the fields are filled up
                        if application_num and meta_serial_num and filing_date and protection_status:
                            ip_protection_meta = TechnologyProtectionTypesMetadata(
                              application_number=application_num,
                              meta_serial_number=meta_serial_num,
                              date_of_filing=filing_date,
                              status=protection_status
                            )

                            # TODO: bulk create does not work since we do need the reference to an existing metadata
                            #       which have its pk been already set so we create here in the loop. This can be a
                            #       bottleneck since we are invoking possible multiple insert statements.
                            ip_protection_meta.save()

                            # create the m2m relationship
                            ip_protections.append(
                              TechnologyProtectionTypes(
                                technology=technology,
                                protection_type=protection_type,
                                protection_type_meta=ip_protection_meta
                              )
                            )

        # add all at once when there is m2m relationships to be created
        num_ip_protections = len(ip_protections)
        if num_ip_protections > 0:
            TechnologyProtectionTypes.objects.bulk_create(ip_protections)

    def save_assets(self, technology, context):
        assets = []

        for tech_asset_type in context['tech_asset_types']:
            snake_asset_type = snakecase(slugify(tech_asset_type.name))
            context_key = f"{context['tech_assets_formset_prefix']}{snake_asset_type}"
            tech_asset_form = context[context_key]

            if tech_asset_form.is_valid():
                tech_asset_form.instance = technology
                models = tech_asset_form.save(commit=False)

                # loop through all the asset forms and create necessary objects
                for asset in models:
                    asset.asset_type = tech_asset_type

                    assets.append(asset)

        # add all at once when there is m2m relationships to be created
        num_assets = len(assets)
        if num_assets > 0:
            TechnologyAssets.objects.bulk_create(assets)

    def save_full_description(self, technology, context):
        fulldescriptions = []

        for tech_fulldescription_type in context['tech_fulldescription_types']:
            snake_fulldescription_type = snakecase(slugify(tech_fulldescription_type.name))
            context_key = f"{context['tech_fulldescriptions_formset_prefix']}{snake_fulldescription_type}"
            tech_fulldescription_form = context[context_key]

            if tech_fulldescription_form.is_valid():
                tech_fulldescription_form.instance = technology
                models = tech_fulldescription_form.save(commit=False)

                # loop through all the asset forms and create necessary objects
                for fulldescription in models:
                    fulldescription.description_type = tech_fulldescription_type

                    fulldescriptions.append(fulldescription)

        # add all at once when there is m2m relationships to be created
        num_fulldescriptions = len(fulldescriptions)
        if num_fulldescriptions > 0:
            TechnologyFullDescription.objects.bulk_create(fulldescriptions)

class TechnologiesUpdate(BaseAdminView, HasPermissionsMixin, LoggedUpdateView):
    required_permission = 'update_technologies'
    model = Technologies
    form_class = TechnologyForm
    template_name = 'ttpd_admin/technologies/form.html'
    success_url = reverse_lazy('ttpd_admin:technologies_list')

    def get_context_data(self, **kwargs):
        context = super(TechnologiesUpdate, self).get_context_data(**kwargs)
        technology = self.get_object()

        # WARNING: three formsets causes MultiValueDictKeyError
        # update the context data to include the formset context for technology readiness
        context.update(self.setup_technology_readiness_formset_context(technology))
        context.update(self.setup_technology_funding_formset_context(technology))
        context.update(self.setup_technology_ip_protection_formset_context(technology))
        context.update(self.setup_technology_assets_formset_context(technology))
        context.update(self.setup_technology_full_description_formset_context(technology))

        return context

    def setup_technology_readiness_formset_context(self, technology):
        context = {}

        # create formsets for status of readiness
        tech_statuses_related = TechnologyStatuses.objects.filter(technology=technology).select_related('tech_status')
        tech_statuses = TechStatus.objects.all()
        context['tech_statuses'] = tech_statuses
        context['tech_statuses_formset_prefix'] = 'tech_status_'

        for tech_status in tech_statuses:
            snake_status = snakecase(slugify(tech_status.name))
            context_key = f"{context['tech_statuses_formset_prefix']}{snake_status}"

            # check if the status of readiness matches the one related to the technology
            # if it is, create a queryset that filters the previously fetched data
            formset_queryset = None
            for tech_status_related in tech_statuses_related:
                if tech_status == tech_status_related.tech_status:
                    formset_queryset = tech_statuses_related.filter(tech_status=tech_status)

            # dynamically assemble the formset kwargs
            formset_kwargs = {
              'prefix': context_key
            }

            if formset_queryset != None:
                formset_kwargs['instance'] = technology
                formset_kwargs['queryset'] = formset_queryset

            # if the request method is "POST" pass its
            if self.request.POST:
                context[context_key] = TechnologyReadinessStatusFormSet(self.request.POST, **formset_kwargs)
            else:
                context[context_key] = TechnologyReadinessStatusFormSet(**formset_kwargs)

        return context

    def setup_technology_funding_formset_context(self, technology):
        context = {}

        # create formsets for technology_funding types
        tech_fundings_related = Fundings.objects.filter(technology=technology).select_related('funding_type')
        technology_funding_types = FundingTypes.objects.all()
        context['technology_funding_types'] = technology_funding_types
        context['technology_funding_types_formset_prefix'] = 'tech_funding_'

        for funding_type in technology_funding_types:
            snake_funding_type = snakecase(slugify(funding_type.name))
            context_key = f"{context['technology_funding_types_formset_prefix']}{snake_funding_type}"

            # check if the funding type matches the one related to the technology
            # if it is, create a queryset that filters the previously fetched data
            formset_queryset = None
            for tech_funding_related in tech_fundings_related:
                if funding_type == tech_funding_related.funding_type:
                    formset_queryset = tech_fundings_related.filter(funding_type=funding_type)

            # dynamically assemble the formset kwargs
            formset_kwargs = {
              'prefix': context_key
            }

            if formset_queryset != None:
                formset_kwargs['instance'] = technology
                formset_kwargs['queryset'] = formset_queryset

            # if the request method is "POST" pass it to the form set.
            # use different form set when the funding type is extension / commercialization
            if self.request.POST:
                if snake_funding_type != 'extension_commercialization':
                    context[context_key] = TechnologyFundingsFormSet(self.request.POST, **formset_kwargs)
                else:
                    context[context_key] = ExtensionAndCommercializationTechnologyFundingsFormSet(
                      self.request.POST,
                      **formset_kwargs
                    )
            else:
                if snake_funding_type != 'extension_commercialization':
                    context[context_key] = TechnologyFundingsFormSet(**formset_kwargs)
                else:
                    context[context_key] = ExtensionAndCommercializationTechnologyFundingsFormSet(**formset_kwargs)

        return context

    # NOTE: since the model looped in this part can be added or revised according to the given document,
    #       some part of this code might not work well and may resolve to the default values!
    def setup_technology_ip_protection_formset_context(self, technology):
        context = {}

        # create formsets for protection types
        protection_types = ProtectionTypes.objects.all()
        tech_protections_related = TechnologyProtectionTypes.objects.filter(technology=technology) \
            .select_related('protection_type', 'protection_type_meta')

        context['technology_protection_types'] = protection_types
        context['technology_protection_types_formset_prefix'] = 'tech_prot_'

        protection_status_all_queryset = TechnologyProtectionStatus.objects.all()
        protection_status_no_rev_queryset = TechnologyProtectionStatus.objects.exclude(name='For Revival')

        for protection_type in protection_types:
            snake_protection_type = snakecase(slugify(protection_type.name))
            context_key = f"{context['technology_protection_types_formset_prefix']}{snake_protection_type}"

            # customize the query set to be used depending on the protection type
            protection_status_queryset = protection_status_no_rev_queryset
            if snake_protection_type == 'patent' or snake_protection_type == 'utility_model':
                protection_status_queryset = protection_status_all_queryset

            # customize the label for the meta_serial_number label depending on the protection type
            meta_serial_label = 'Registration Number'
            if snake_protection_type == 'patent':
                meta_serial_label = 'Patent Number'
            elif snake_protection_type == 'plant_variety_protection':
                meta_serial_label = 'PVP Number'

            # check if the ip protection data matches the one related to the technology
            # if it is, create a queryset that filters the previously fetched data
            formset_queryset = None
            is_trade_secret = False
            for tech_protection_related in tech_protections_related:
                if (
                  protection_type == tech_protection_related.protection_type and
                  tech_protection_related.protection_type_meta is None
                ):
                    is_trade_secret = True

                if (
                  protection_type == tech_protection_related.protection_type and
                  tech_protection_related.protection_type_meta is not None
                ):
                    formset_queryset = TechProtectionTypesMetadata.objects.filter(
                      id=tech_protection_related.protection_type_meta.id
                    )

            # dynamically assemble the formset kwargs
            formset_kwargs = {
              'prefix': context_key
            }

            # set queryset and form_kwargs for all forms other than trade secret form
            if snake_protection_type != 'trade_secret':
                formset_kwargs['queryset'] = TechProtectionTypesMetadata.objects.none()
                formset_kwargs['form_kwargs'] = {
                  'meta_serial_label': meta_serial_label,
                  'protection_status_queryset': protection_status_queryset
                }

            # override the default queryset provided if the formset_queryset is not an empty value
            if formset_queryset != None and snake_protection_type != 'trade_secret':
                formset_kwargs['queryset'] = formset_queryset

            # set the initial data if the form where generating is for the trade secret
            if is_trade_secret is True and snake_protection_type == 'trade_secret':
                formset_kwargs['initial'] = [{'is_trade_secret': True}]

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                if snake_protection_type != 'trade_secret':
                    context[context_key] = TechnologyIpProtectionMetadataFormSet(
                      self.request.POST,
                      **formset_kwargs
                    )
                else:
                    context[context_key] = TradeSecretIpProtectionFormSet(
                      self.request.POST,
                      **formset_kwargs
                    )
            else:
                if snake_protection_type != 'trade_secret':
                    context[context_key] = TechnologyIpProtectionMetadataFormSet(**formset_kwargs)
                else:
                    context[context_key] = TradeSecretIpProtectionFormSet(**formset_kwargs)

        return context

    def setup_technology_assets_formset_context(self, technology):
        context = {}

        # create formsets for assets
        tech_assets_related = TechnologyAssets.objects.filter(technology=technology).select_related('asset_type')
        tech_asset_types = TechnologyAssetTypes.objects.all()
        context['tech_asset_types'] = tech_asset_types
        context['tech_assets_formset_prefix'] = 'tech_assets_'
        context['tech_asset_types_ip_protected'] = [
          'Narrative Advantages',
          'Technical Evidences',
          'Economic Evidences',
          'Market Study Summary',
          'Valuation Summary',
          'Freedom to Operate Summary',
          'Proposed Term Sheet',
          'Fairness Opinion Report',
          'Video Clips'
        ]

        for tech_asset_type in tech_asset_types:
            snake_asset_type = snakecase(slugify(tech_asset_type.name))
            context_key = f"{context['tech_assets_formset_prefix']}{snake_asset_type}"

            # check if the funding type matches the one related to the technology
            # if it is, create a queryset that filters the previously fetched data
            formset_queryset = None
            for tech_asset_related in tech_assets_related:
                if tech_asset_type == tech_asset_related.asset_type:
                    formset_queryset = tech_assets_related.filter(asset_type=tech_asset_type)

            # dynamically assemble the formset kwargs
            formset_kwargs = {
              'prefix': context_key
            }

            if formset_queryset != None:
                formset_kwargs['instance'] = technology
                formset_kwargs['queryset'] = formset_queryset

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                context[context_key] = TechnologyAssetsFormSet(
                  self.request.POST,
                  self.request.FILES,
                  **formset_kwargs
                )
            else:
                context[context_key] = TechnologyAssetsFormSet(**formset_kwargs)

        return context

    def setup_technology_full_description_formset_context(self, technology):
        context = {}

        # create formsets for full-description
        tech_fulldescriptions_related = TechnologyFullDescription.objects.filter(technology=technology).select_related('description_type')
        tech_fulldescription_types = TechnologyFullDescriptionTypes.objects.all()
        context['tech_fulldescription_types'] = tech_fulldescription_types
        context['tech_fulldescriptions_formset_prefix'] = 'tech_fulldescription_'

        for tech_fulldescription_type in tech_fulldescription_types:
            snake_fulldescription_type = snakecase(slugify(tech_fulldescription_type.name))
            context_key = f"{context['tech_fulldescriptions_formset_prefix']}{snake_fulldescription_type}"

            # check if the funding type matches the one related to the technology
            # if it is, create a queryset that filters the previously fetched data
            formset_queryset = None
            for tech_fulldescription_related in tech_fulldescriptions_related:
                if tech_fulldescription_type == tech_fulldescription_related.description_type:
                    formset_queryset = tech_fulldescriptions_related.filter(description_type=tech_fulldescription_type)

            # dynamically assemble the formset kwargs
            formset_kwargs = {
              'prefix': context_key
            }

            if formset_queryset != None:
                formset_kwargs['instance'] = technology
                formset_kwargs['queryset'] = formset_queryset

            # if the request method is "POST" pass it to the form set.
            if self.request.POST:
                context[context_key] = TechnologyFullDescriptionFormSet(
                  self.request.POST,
                  self.request.FILES,
                  **formset_kwargs
                )
            else:
                context[context_key] = TechnologyFullDescriptionFormSet(**formset_kwargs)

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        # initialize variable outside the try block to so that we will be able to reference it inside the except block
        technology = None

        # retrieve the protection level
        protection_level = form.cleaned_data.get('protection_level')

        # check if the formsets declared within the form is not valid.
        # if it is, mark the form as invalid immediately
        if not self.inline_formsets_valid(context):
            return super(TechnologiesUpdate, self).form_invalid(form)

        # perform an atomic transaction to perfectly sync m2m relationships or rollback all at once when an error occurs
        try:
            try:
                with transaction.atomic():
                    technology = form.save(commit=False)

                    # TODO: if protection level has changed from IP protected to Public, delete the protection metadata
                    #       and remove association of the adopters to the technology and also the advantages to existing
                    if form.has_changed():

                        # save the technology
                        technology.save()

                        # save the categories
                        if 'categories' in form.changed_data:
                            self.save_technology_categories(technology, form.cleaned_data.get('categories'))

                        # save the industry sectors
                        if 'industry_sectors' in form.changed_data:
                            self.save_technology_industry_sectors(technology, form.cleaned_data.get('industry_sectors'))

                        # save the generators
                        if 'generators' in form.changed_data:
                            self.save_technology_generators(technology, form.cleaned_data.get('generators'))

                        # save the owners
                        if 'owners' in form.changed_data:
                            self.save_technology_owners(technology, form.cleaned_data.get('owners'))

                        # save the potential adopters
                        if 'potential_adopters' in form.changed_data:
                            self.save_potential_adopters(technology, form.cleaned_data.get('potential_adopters'))

                        # save the adopters when ip protection is set to ip protected
                        if protection_level.name.lower() == 'ip protected' and 'adopters' in form.changed_data:
                            self.save_adopters(technology, form.cleaned_data.get('adopters'))

                    # save the status of readiness data
                    self.save_status_of_readiness_data(technology, context)

                    # save the technology fundings
                    self.save_technology_fundings(technology, context)

                    # save the technology assets
                    self.save_assets(technology, context)

                    # save the technology assets
                    self.save_full_description(technology, context)

                    if protection_level.name.lower() == 'ip protected':
                        self.save_ip_protection_data(technology, context)

                    # store the reference of the technology to the object property
                    self.object = technology # pylint: disable=W0201

            except IntegrityError:
                # re-raise an exception but this time a new instance of different exception
                raise RuntimeError('An unknown error has occurred. Please try again later.')

        except RuntimeError as re:
            # add a non-field error to show to the user
            form.add_error(None, re)

            return super(TechnologiesUpdate, self).form_invalid(form)

        # since we are manually saving the object, we call the redirect not the parent class' form_valid method.
        return HttpResponseRedirect(self.get_success_url())

    def inline_formsets_valid(self, context):
        valid = True

        for tech_status in context['tech_statuses']:
            snake_status = snakecase(slugify(tech_status.name))
            context_key = f"{context['tech_statuses_formset_prefix']}{snake_status}"
            tech_status_form = context[context_key]

            # check if the inline formsets are valid or not
            if not tech_status_form.is_valid():
                valid = False

                break

        for protection_type in context['technology_protection_types']:
            snake_protection_type = snakecase(slugify(protection_type.name))
            context_key = f"{context['technology_protection_types_formset_prefix']}{snake_protection_type}"
            ip_protection_meta_form = context[context_key]

            # check if the inline formsets are valid or not
            if not ip_protection_meta_form.is_valid():
                valid = False

                break

        for funding_type in context['technology_funding_types']:
            snake_funding_type = snakecase(slugify(funding_type.name))
            context_key = f"{context['technology_funding_types_formset_prefix']}{snake_funding_type}"
            funding_type_form = context[context_key]

            # check if the inline formsets are valid or not
            if not funding_type_form.is_valid():
                valid = False

                break

        for tech_asset_type in context['tech_asset_types']:
            snake_asset_type = snakecase(slugify(tech_asset_type.name))
            context_key = f"{context['tech_assets_formset_prefix']}{snake_asset_type}"
            tech_asset_type_form = context[context_key]

            # check if the inline formsets are valid or not
            if not tech_asset_type_form.is_valid():
                valid = False

        for tech_fulldescription_type in context['tech_fulldescription_types']:
            snake_fulldescription_type = snakecase(slugify(tech_fulldescription_type.name))
            context_key = f"{context['tech_fulldescriptions_formset_prefix']}{snake_fulldescription_type}"
            tech_fulldescription_type_form = context[context_key]

            # check if the inline formsets are valid or not
            if not tech_fulldescription_type_form.is_valid():
                valid = False

        return valid

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_technology_categories(self, technology, cleaned_categories):
        num_categories = len(cleaned_categories)

        if num_categories > 0:
            categories = []

            # clear all existing relationships first
            TechnologyCategories.objects.filter(technology=technology).delete()

            # create m2m category instance on the fly
            for category in cleaned_categories:
                categories.append(TechnologyCategories(technology=technology, tech_category=category))

            # add it all at once
            TechnologyCategories.objects.bulk_create(categories)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_technology_industry_sectors(self, technology, cleaned_industry_sectors):
        num_industry_sectors = len(cleaned_industry_sectors)

        if num_industry_sectors > 0:
            industry_sectors = []

            # clear all existing relationships first
            TechnologyIndustrySectors.objects.filter(technology=technology).delete()

            # create m2m industry sector instance on the fly
            for industry_sector in cleaned_industry_sectors:
                industry_sectors.append(
                  TechnologyIndustrySectors(technology=technology, industry_sector=industry_sector)
                )

            # add it all at once
            TechnologyIndustrySectors.objects.bulk_create(industry_sectors)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_technology_generators(self, technology, cleaned_generators):
        num_generators = len(cleaned_generators)

        if num_generators > 0:
            generators = []

            # clear all existing relationships first
            TechnologyGenerators.objects.filter(technology=technology).delete()

            # create m2m generator instance on the fly
            for generator in cleaned_generators:
                generators.append(TechnologyGenerators(technology=technology, generator=generator))

            # add it all at once
            TechnologyGenerators.objects.bulk_create(generators)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_potential_adopters(self, technology, cleaned_potential_adopters):
        num_potential_adopters = len(cleaned_potential_adopters)

        if num_potential_adopters > 0:
            potential_adopters = []

            # clear all existing relationships first
            TechnologyPotentialAdopters.objects.filter(technology=technology).delete()

            # create m2m potential adopter instance on the fly
            for potential_adopter in cleaned_potential_adopters:
                potential_adopters.append(
                  TechnologyPotentialAdopters(technology=technology, potential_adopter=potential_adopter)
                )

            # add it all at once
            TechnologyPotentialAdopters.objects.bulk_create(potential_adopters)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_technology_owners(self, technology, cleaned_owners):
        num_owners = len(cleaned_owners)

        if num_owners > 0:
            owners = []

            # clear all existing relationships first
            TechnologyOwners.objects.filter(technology=technology).delete()

            # create m2m owner instance on the fly
            for owner in cleaned_owners:
                owners.append(TechnologyOwners(technology=technology, owner=owner))

            # add it all at once
            TechnologyOwners.objects.bulk_create(owners)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_adopters(self, technology, cleaned_adopters):
        num_adopters = len(cleaned_adopters)

        if num_adopters > 0:
            adopters = []

            # clear all existing relationships first
            TechnologyAdopters.objects.filter(technology=technology).delete()

            # create m2m adopter instance on the fly
            for adopter in cleaned_adopters:
                adopters.append(
                  TechnologyAdopters(technology=technology, adopter=adopter)
                )

            # add it all at once
            TechnologyAdopters.objects.bulk_create(adopters)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_status_of_readiness_data(self, technology, context):
        statuses = []
        update_statuses = []
        del_statuses = []

        for tech_status in context['tech_statuses']:
            snake_status = snakecase(slugify(tech_status.name))
            context_key = f"{context['tech_statuses_formset_prefix']}{snake_status}"
            tech_status_form = context[context_key]

            # process the forms only if it has changed and it is valid
            if tech_status_form.is_valid() and tech_status_form.has_changed():
                tech_status_form.instance = technology
                models = tech_status_form.save(commit=False)

                for index, status_item in enumerate(models):
                    clean_data_ref = tech_status_form.cleaned_data[index]
                    is_enabled = clean_data_ref.get('enable', False)

                    if is_enabled is False and status_item.id is not None:
                        del_statuses.append(status_item.id)

                    if is_enabled is True and status_item.id is not None:
                        update_statuses.append(status_item)

                    if is_enabled is True and status_item.id is None:
                        # add relation to the status of technology
                        status_item.tech_status = tech_status

                        statuses.append(status_item)

        # delete items that are present in the list of items for deletion
        num_del_statuses = len(del_statuses)
        if num_del_statuses > 0:
            TechnologyStatuses.objects.filter(pk__in=del_statuses, technology=technology).delete()

        # saved changed items
        num_update_statuses = len(update_statuses)
        if num_update_statuses > 0:
            for update_status in num_update_statuses:
                update_status.save()

        # add all at once when there is m2m relationships to be created
        num_statuses = len(statuses)
        if num_statuses > 0:
            TechnologyStatuses.objects.bulk_create(statuses)

    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    def save_technology_fundings(self, technology, context):
        technology_funding_implementors = []

        del_technology_funding = []

        for funding_type in context['technology_funding_types']:
            snake_funding_type = snakecase(slugify(funding_type.name))
            context_key = f"{context['technology_funding_types_formset_prefix']}{snake_funding_type}"
            funding_type_form = context[context_key]

            # process the forms only if it has changed and it is valid
            if funding_type_form.is_valid() and funding_type_form.has_changed():
                funding_type_form.instance = technology
                models = funding_type_form.save(commit=False)

                # set the funding type and append it to a list for bulk creation
                for index, funding_type_item in enumerate(models):
                    clean_data_ref = funding_type_form.cleaned_data[index]

                    # mark the item for deletion since all fields are emptied and immediately skip to the next iteration
                    if (
                      funding_type.id is not None and
                      (funding_type_item.investment_amount is None or
                       funding_type_item.duration_start is None or
                       funding_type_item.duration_end)
                    ):
                        del_technology_funding.append(funding_type_item.id)

                        continue

                    # add relation to the funding type when it is not yet persisted on the database
                    if funding_type_item.id is None:
                        funding_type_item.funding_type = funding_type

                    # process additional fields
                    if snake_funding_type == 'extension_commercialization':
                        json_serialized = json.dumps({
                          'project_sites': clean_data_ref.get('project_sites')
                        }).encode()

                        # convert to a base64 encoded byte string to be saved to database
                        b64_serialized = base64.b64encode(json_serialized)

                        # covert the base64 encoded byte string to a regular string
                        funding_type_item.properties = b64_serialized.decode()

                    # TODO: bulk create does not work since we do need the reference to an existing funding
                    #       which have its pk been already set so we create here in the loop. This can be a
                    #       bottleneck since we are invoking possible multiple insert statements.
                    funding_type_item.save()

                    # clear all existing relationships first
                    FundingImplementors.objects.filter(funding=funding_type_item).delete()

                    # create the objects for the implementors
                    for implementing_agency in clean_data_ref.get('implementing_agencies'):
                        technology_funding_implementors.append(
                          FundingImplementors(funding=funding_type_item, implementor=implementing_agency)
                        )

        num_del_technology_funding = len(del_technology_funding)
        if num_del_technology_funding > 0:
            Fundings.objects.filter(pk__in=del_technology_funding, technology=technology).delete()

        # add all at once when there is m2m relationships to be created
        num_technology_funding_implementors = len(technology_funding_implementors)
        if num_technology_funding_implementors > 0:
            FundingImplementors.objects.bulk_create(technology_funding_implementors)


    # TODO: implement a diffing logic so that only items that needs to be added/removed are persisted
    # NOTE: since the model looped in this part can be added or revised according to the given document,
    #       some part of this code might not work well and may resolve to the default values!
    def save_ip_protection_data(self, technology, context):
        ip_protections = []
        del_ip_protections = []
        del_meta_protections = []

        for protection_type in context['technology_protection_types']:
            snake_protection_type = snakecase(slugify(protection_type.name))
            context_key = f"{context['technology_protection_types_formset_prefix']}{snake_protection_type}"
            ip_protection_meta_form = context[context_key]

            if ip_protection_meta_form.is_valid() and ip_protection_meta_form.has_changed():
                if snake_protection_type == 'trade_secret':
                    for trade_secret_form in ip_protection_meta_form.forms:
                        is_trade_secret = trade_secret_form.cleaned_data.get('is_trade_secret')

                        # create an instance of the protection type if it is trade secret
                        if is_trade_secret is True:
                            ip_protections.append(
                              TechnologyProtectionTypes(technology=technology, protection_type=protection_type)
                            )

                        # mark the reference of trade secret for deletion
                        if is_trade_secret is False:
                            del_ip_protections.append(
                              TechnologyProtectionTypes.objects.filter(
                                technology=technology,
                                protection_type=protection_type
                              )[0].id
                            )

                else:
                    models = ip_protection_meta_form.save(commit=False)

                    for meta_item in models:

                        # mark the item for deletion since all fields are emptied and
                        # immediately skip to the next iteration
                        if (
                          meta_item.id is not None and
                          (meta_item.application_number is None or
                           meta_item.meta_serial_number is None or
                           meta_item.date_of_filing is None or
                           meta_item.status is None)
                        ):
                            del_ip_protections.append(
                              TechnologyProtectionTypes.objects.filter(
                                technology=technology,
                                protection_type=protection_type
                              )[0].id
                            )

                            del_meta_protections.append(meta_item.id)

                            continue

                        # TODO: bulk create does not work since we do need the reference to an existing metadata
                        #       which have its pk been already set so we create here in the loop. This can be a
                        #       bottleneck since we are invoking possible multiple insert statements.
                        meta_item.save()

                        # check if the meta is already associated, if not create an association
                        meta_queryset = TechnologyProtectionTypes.objects.filter(
                          technology=technology,
                          protection_type=protection_type,
                          protection_type_meta=meta_item
                        )
                        num_result_meta_query_set = len(meta_queryset)
                        if num_result_meta_query_set == 0:
                            ip_protections.append(
                              TechnologyProtectionTypes(
                                technology=technology,
                                protection_type=protection_type,
                                protection_type_meta=meta_item
                              )
                            )

        # del_ip_protections = []
        num_del_meta_protections = len(del_meta_protections)
        if num_del_meta_protections > 0:
            TechProtectionTypesMetadata.objects.filter(pk__in=del_meta_protections).delete()

        num_del_ip_protections = len(del_ip_protections)
        if num_del_ip_protections > 0:
            TechnologyProtectionTypes.objects.filter(pk__in=del_ip_protections).delete()

        # add all at once when there is m2m relationships to be created
        num_ip_protections = len(ip_protections)
        if num_ip_protections > 0:
            TechnologyProtectionTypes.objects.bulk_create(ip_protections)

    def save_assets(self, technology, context):
        for tech_asset_type in context['tech_asset_types']:
            snake_asset_type = snakecase(slugify(tech_asset_type.name))
            context_key = f"{context['tech_assets_formset_prefix']}{snake_asset_type}"
            tech_asset_form = context[context_key]

            if tech_asset_form.is_valid() and tech_asset_form.has_changed():
                tech_asset_form.instance = technology
                models = tech_asset_form.save(commit=False)

                # loop through all the asset forms create association between the asset and the type
                for asset in models:
                    asset.asset_type = tech_asset_type

                # remove any marked for deletion objects
                for del_object in tech_asset_form.deleted_objects:
                    del_object.delete()

                # save any changed objects
                for changed_object in tech_asset_form.changed_objects:
                    changed_object.save()

                # save any new objects
                for new_object in tech_asset_form.new_objects:
                    new_object.save()

    def save_full_description(self, technology, context):
        for tech_fulldescription_type in context['tech_fulldescription_types']:
            snake_fulldescription_type = snakecase(slugify(tech_fulldescription_type.name))
            context_key = f"{context['tech_fulldescriptions_formset_prefix']}{snake_fulldescription_type}"
            tech_fulldescription_form = context[context_key]

            if tech_fulldescription_form.is_valid() and tech_fulldescription_form.has_changed():
                tech_fulldescription_form.instance = technology
                models = tech_fulldescription_form.save(commit=False)

                # loop through all the asset forms create association between the asset and the type
                for fulldescription in models:
                    fulldescription.description_type = tech_fulldescription_type

                # remove any marked for deletion objects
                for del_object in tech_fulldescription_form.deleted_objects:
                    del_object.delete()

                # save any changed objects
                for changed_object in tech_fulldescription_form.changed_objects:
                    changed_object.save()

                # save any new objects
                for new_object in tech_fulldescription_form.new_objects:
                    new_object.save()

class TechnologiesDelete(BaseAdminView, HasPermissionsMixin, LoggedDeleteView):
    required_permission = 'remove_technologies'
    model = Technologies
    template_name = 'ttpd_admin/technologies/delete.html'
    success_url = reverse_lazy('ttpd_admin:technologies_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            try:
                with transaction.atomic():

                    # delete categories associated to the technology
                    TechnologyCategories.objects.filter(technology=self.object).delete()

                    # delete industry sectors associated to the technology
                    TechnologyIndustrySectorISPs.objects.filter(technology=self.object).delete()

                    # delete generators associated to the technology
                    TechnologyGenerators.objects.filter(technology=self.object).delete()

                    # delete potential adopters associated to the technology
                    TechnologyPotentialAdopters.objects.filter(technology=self.object).delete()

                    # delete owners associated to the technology
                    TechnologyOwners.objects.filter(technology=self.object).delete()

                    # delete adopters associated to the technology
                    TechnologyAdopters.objects.filter(technology=self.object).delete()

                    # delete statuses associated to the technology
                    TechnologyStatuses.objects.filter(technology=self.object).delete()

                    # delete the associated assets to the technology
                    TechnologyAssets.objects.filter(technology=self.object).delete()

                    # delete the associated assets to the technology
                    TechnologyFullDescription.objects.filter(technology=self.object).delete()

                    # delete fundings associated to the technology
                    fundings = Fundings.objects.filter(technology=self.object)

                    for funding in fundings:
                        FundingImplementors.objects.filter(funding=funding).delete()

                    fundings.delete()

                    # delete protection types associated to the technology
                    protection_types = TechnologyProtectionTypes.objects.filter(technology=self.object) \
                        .select_related('protection_type_meta')

                    for protection_type in protection_types:
                        if protection_type.protection_type_meta is not None:
                            protection_type.protection_type_meta.delete()

                    protection_types.delete()

                    # delete the technology
                    self.object.delete()

            except IntegrityError:
                # re-raise an exception but this time a new instance of different exception
                raise RuntimeError('An unknown error has occurred. Please try again later.')

        except RuntimeError as re:
            return HttpResponseBadRequest(re)

        return HttpResponseRedirect(success_url)

# NOTE: if we need to customize the user model, a complete guide on the link is given below
#       <https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html>
class UsersProfile(BaseAdminView, HasPermissionsMixin, DetailView):
    required_permission = 'profile_users'
    model = User
    template_name = 'ttpd_admin/users/profile.html'
    
    fields = [
          'username',
          'first_name',
          'last_name',
          'is_staff',
          'last_login',
          'email_address'
        ]

    def get_context_data(self, **kwargs):
        context = super(UsersProfile, self).get_context_data(**kwargs)
        instance = self.get_object()
        return context

class UsersList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = User
    queryset = User.objects.filter(is_superuser=False, is_staff=True)
    template_name = 'ttpd_admin/users/index.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = ListView.get_context_data(self, **kwargs)
        context['pagination_item_ranges'] = range(1, (context['paginator'].num_pages + 1))
        return context

class UsersCreate(BaseAdminView, HasRoleMixin, LoggedCreateView):
    allowed_roles = [Admin]
    model = User
    form_class = UsersForm
    template_name = 'ttpd_admin/users/form.html'
    success_url = reverse_lazy('ttpd_admin:users_list')

    def form_valid(self, form):
        user = None

        # perform an atomic transaction to perfectly sync m2m relationships or rollback all at once when an error occurs
        try:
            try:
                with transaction.atomic():
                    user = form.save(commit=False)

                    # save the user to get an id for it
                    user.save()

                    # assign a role to the user
                    assign_role(user, form.cleaned_data.get('roles'))

                    # save the user since the assign_role will add the user to the group for the role assigned
                    user.save()

                    # store the reference of the user to the object property
                    self.object = user # pylint: disable=W0201

            except IntegrityError:
                # re-raise an exception but this time a new instance of different exception
                raise RuntimeError('An unknown error has occurred. Please try again later.')

        except RuntimeError as re:
            if user is not None:
                user.delete()

            # add a non-field error to show to the user
            form.add_error(None, re)

            return super(UsersCreate, self).form_invalid(form)

        # since we are manually saving the object, we call the redirect not the parent class' form_valid method.
        return HttpResponseRedirect(self.get_success_url())

class UsersUpdate(BaseAdminView, HasRoleMixin, LoggedUpdateView):
    allowed_roles = [Admin]
    model = User
    form_class = UsersUpdateForm
    template_name = 'ttpd_admin/users/form.html'
    success_url = reverse_lazy('ttpd_admin:users_list')

    def get_context_data(self, **kwargs):
        context = super(UsersUpdate, self).get_context_data(**kwargs)
        user = self.get_object()

        available_role_choices = context['form'].fields['roles'].choices
        user_roles = get_user_roles(user)

        matched_role = None
        for user_role in user_roles:
            # break immediately the outer loop if there is one already
            if matched_role is not None:
                break

            # loop through the available role choices and check if the user's role matches with the choices
            for role_choice in available_role_choices:
                if role_choice[0] != '' and role_choice[0] == user_role.get_name():
                    matched_role = user_role
                    break

        # set the initial value for the role field
        if matched_role is not None:
            context['user_role'] = matched_role
            context['form'].fields['roles'].initial = matched_role.get_name()

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user = None

        # perform an atomic transaction to perfectly sync m2m relationships or rollback all at once when an error occurs
        try:
            try:
                with transaction.atomic():
                    user = form.save(commit=False)

                    # check if there are any changes to the form
                    if form.has_changed():
                        initial_user_role = context.get('user_role', None)
                        new_role = form.cleaned_data.get('roles')

                        # save the user to get an id for it
                        user.save()

                        # remove the initial role from the user and assign the new one
                        if initial_user_role is not None and initial_user_role.get_name() != new_role:
                            remove_role(user, initial_user_role.get_name())

                            assign_role(user, form.cleaned_data.get('roles'))

                        # save the user since the assign_role will add the user to the group for the role assigned
                        user.save()

                    # store the reference of the user to the object property
                    self.object = user # pylint: disable=W0201

            except IntegrityError:
                # re-raise an exception but this time a new instance of different exception
                raise RuntimeError('An unknown error has occurred. Please try again later.')

        except RuntimeError as re:
            if user is not None:
                user.delete()

            # add a non-field error to show to the user
            form.add_error(None, re)

            return super(UsersUpdate, self).form_invalid(form)

        # since we are manually saving the object, we call the redirect not the parent class' form_valid method.
        return HttpResponseRedirect(self.get_success_url())

class UsersDelete(BaseAdminView, HasRoleMixin, LoggedDeleteView):
    allowed_roles = [Admin]
    model = User
    template_name = 'ttpd_admin/users/delete.html'
    success_url = reverse_lazy('ttpd_admin:users_list')

class RegisteredUsersList(BaseAdminView, HasRoleMixin, ListView):
    allowed_roles = [Admin]
    model = User
    queryset = User.objects.filter(is_superuser=False, is_staff=False)
    template_name = 'ttpd_admin/registered_users/index.html'
    paginate_by = 20