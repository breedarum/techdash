# models.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from secrets import token_hex
from pathlib import Path
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User as BaseUser
from django.template.defaultfilters import slugify

class Commodities(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "commodity"
        verbose_name_plural = "commodities"

    def get_absolute_url(self):
        return reverse('ttpd_admin:commodities_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class Industries(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "industry"
        verbose_name_plural = "industries"

    def get_absolute_url(self):
        return reverse('ttpd_admin:industries_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class Sectors(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Industries, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "sector"
        verbose_name_plural = "sectors"

    def get_absolute_url(self):
        return reverse('ttpd_admin:sectors_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class ISPs(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey(Sectors, on_delete=models.CASCADE)
    specific_commodity = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                               limit_choices_to=models.Q(parent=None))

    class Meta:
        verbose_name = "isp"
        verbose_name_plural = "isps"

    def get_absolute_url(self):
        return reverse('ttpd_admin:isps_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class ProtectionLevels(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "protection level"
        verbose_name_plural = "protection levels"

    def __str__(self):
        return self.name

class ProtectionTypes(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "protection type"
        verbose_name_plural = "protection types"

    def get_absolute_url(self):
        return reverse('ttpd_admin:protection_types_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class AdopterTypes(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "adopter type"
        verbose_name_plural = "adopter types"

    def get_absolute_url(self):
        return reverse('ttpd_admin:adopter_type_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class PotentialAdopters(models.Model):
    name = models.CharField(max_length=255)
    adopter_type = models.ForeignKey(AdopterTypes, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "potential adopter"
        verbose_name_plural = "potential adopters"

    def get_absolute_url(self):
        return reverse('ttpd_admin:potential_adopters_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class Adopters(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=40)
    fax_number = models.CharField(max_length=40, null=True, blank=True)
    email_address = models.EmailField()
    adopter_type = models.ForeignKey(AdopterTypes, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "adopter"
        verbose_name_plural = "adopters"

    def __str__(self):
        return self.name

class AgencyTypes(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "agency type"
        verbose_name_plural = "agency types"

    def get_absolute_url(self):
        return reverse('ttpd_admin:agency_types_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class Agencies(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=40)
    fax_number = models.CharField(max_length=40, null=True, blank=True)
    agency_type = models.ForeignKey(AgencyTypes, on_delete=models.CASCADE, null=False)
    private_flag = models.BooleanField(default=False)
   
    class Meta:
        verbose_name = "agency"
        verbose_name_plural = "agencies"

    def get_absolute_url(self):
        return reverse('ttpd_admin:agencies_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class Generators(models.Model):
    AVAILABILITY_CHOICES = (
      ('active', 'Active'),
      ('retired', 'Retired'),
      ('deceased', 'Deceased')
    )

    title = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255)
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES, default='active')
    agency = models.ForeignKey(Agencies, on_delete=models.CASCADE, limit_choices_to={'private_flag': False})

    class Meta:
        verbose_name = "generator"
        verbose_name_plural = "generators"

    def get_absolute_url(self):
        return reverse('ttpd_admin:generators_update', kwargs={'pk': self.id})

    def __str__(self):
        title = ''
        # check if the entry has title or not, if it has append a space to it
        # for using in the entry's str representation
        if self.title is not None:
            title = f"{self.title} "

        return f"{title}{self.first_name} {self.last_name}"

class Regions(models.Model):
    name = models.CharField(max_length=80)
    region_roman = models.CharField(max_length=80)
    region_canonical = models.CharField(max_length=160)

    class Meta:
        verbose_name = "region"
        verbose_name_plural = "regions"

    def __str__(self):
        return self.region_canonical

class TechCategories(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                               limit_choices_to=models.Q(parent=None))

    class Meta:
        verbose_name = "technology category"
        verbose_name_plural = "technology categories"

    def get_absolute_url(self):
        return reverse('ttpd_admin:tech_categories_update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name

class FundingTypes(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "funding type"
        verbose_name_plural = "funding types"

    def __str__(self):
        return self.name

class ProtectionTypeStatus(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name = "protection status"
        verbose_name_plural = "protection statuses"

    def __str__(self):
        return self.name

class TechProtectionTypesMetadata(models.Model):
    application_number = models.CharField(max_length=255, blank=True)
    meta_serial_number = models.CharField(max_length=255, blank=True)
    date_of_filing = models.DateField(blank=True)
    status = models.ForeignKey(ProtectionTypeStatus, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology protection type metadata"
        verbose_name_plural = "technology protection type metadatas"

class TechStatus(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "technology status"
        verbose_name_plural = "technology statuses"

    def __str__(self):
        return self.name

class Technologies(models.Model):
    name = models.CharField(max_length=255)
    year = models.CharField(max_length=5, null=True, blank=True)
    description = models.TextField()
    protection_level = models.ForeignKey(ProtectionLevels, on_delete=models.CASCADE)
    est_ownership_cost = models.PositiveIntegerField(null=True, blank=True)
    region = models.ForeignKey(Regions, null=True, blank=True, on_delete=models.CASCADE)

    commodities = models.ManyToManyField(
      Commodities,
      through='TechnologyCommodities',
      through_fields=('technology', 'commodity')
    )

    industry_sector_isp = models.ManyToManyField(
      ISPs,
      through='TechnologyIndustrySectorISPs',
      through_fields=('technology', 'industry_sector_isp')
    )

    categories = models.ManyToManyField(
      TechCategories,
      through='TechnologyCategories',
      through_fields=('technology', 'tech_category')
    )

    generators = models.ManyToManyField(
      'Generators',
      through='TechnologyGenerators',
      through_fields=('technology', 'generator'),
      blank=True
    )

    owners = models.ManyToManyField(
      Agencies,
      through='TechnologyOwners',
      through_fields=('technology', 'owner'),
      blank=True
    )

    adopters = models.ManyToManyField(
      Adopters,
      through='TechnologyAdopters',
      through_fields=('technology', 'adopter'),
      blank=True
    )

    potential_adopters = models.ManyToManyField(
      PotentialAdopters,
      through='TechnologyPotentialAdopters',
      through_fields=('technology', 'potential_adopter'),
      blank=True
    )

    protection_types = models.ManyToManyField(
      ProtectionTypes,
      through='TechnologyProtectionTypes',
      through_fields=('technology', 'protection_type'),
      blank=True
    )

    statuses = models.ManyToManyField(
      TechStatus,
      through='TechnologyStatuses',
      through_fields=('technology', 'tech_status'),
      blank=True
    )

    class Meta:
        verbose_name = "technology"
        verbose_name_plural = "technologies"

    def get_absolute_url(self):
        return reverse('ttpd_admin:technologies_list')

    def __str__(self):
        return self.name

class TechnologyCommodities(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    commodity = models.ForeignKey(Commodities, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology commodity"
        verbose_name_plural = "technology commodities"

class TechnologyIndustrySectorISPs(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    industry_sector_isp = models.ForeignKey(ISPs, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology isp"
        verbose_name_plural = "technology isps"

class TechnologyCategories(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    tech_category = models.ForeignKey(TechCategories, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology category"
        verbose_name_plural = "technology categories"

class TechnologyGenerators(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    generator = models.ForeignKey(Generators, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology generators"
        verbose_name_plural = "technology generators"

class TechnologyOwners(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    owner = models.ForeignKey(Agencies, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology owner"
        verbose_name_plural = "technology owners"

class TechnologyAdopters(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    adopter = models.ForeignKey(Adopters, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology adopter"
        verbose_name_plural = "technology adopters"

class TechnologyPotentialAdopters(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    potential_adopter = models.ForeignKey(PotentialAdopters, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology potential adopter"
        verbose_name_plural = "technology potential adopters"

class TechnologyProtectionTypes(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    protection_type = models.ForeignKey(ProtectionTypes, on_delete=models.CASCADE)
    protection_type_meta = models.OneToOneField(
      TechProtectionTypesMetadata,
      on_delete=models.SET_NULL,
      null=True,
      blank=True
    )

    class Meta:
        verbose_name = "technology protection type"
        verbose_name_plural = "technology protection types"

class TechnologyStatuses(models.Model):
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    tech_status = models.ForeignKey(TechStatus, on_delete=models.CASCADE)
    year_complied = models.CharField(max_length=5, blank=True)

    class Meta:
        verbose_name = "technology status"
        verbose_name_plural = "technology statuses"

class Fundings(models.Model):
    investment_amount = models.PositiveIntegerField(blank=True)
    duration_start = models.DateField(blank=True)
    duration_end = models.DateField(blank=True)
    properties = models.TextField(blank=True)
    funding_type = models.ForeignKey(FundingTypes, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technologies, on_delete=models.CASCADE, related_name='fundings')
    donor = models.ForeignKey(Agencies, on_delete=models.CASCADE, related_name='fundings', blank=True)
    implementing_agencies = models.ManyToManyField(
      Agencies,
      through='FundingImplementors',
      through_fields=('funding', 'implementor'),
      related_name='funding_implementations',
      blank=True,
    )

    class Meta:
        verbose_name = "technology funding"
        verbose_name_plural = "technology fundings"

class FundingImplementors(models.Model):
    funding = models.ForeignKey(Fundings, on_delete=models.CASCADE)
    implementor = models.ForeignKey(Agencies, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "technology funding implementor"
        verbose_name_plural = "technology funding implementors"

# TODO: Re-implement the region field as mentioned in the discussion.

class User(BaseUser):

    class Meta:
        proxy = True

    def get_absolute_url(self):
        return reverse('ttpd_admin:users_update', kwargs={'pk': self.id})


