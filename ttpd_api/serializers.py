# serializers.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from rolepermissions.roles import assign_role
from rest_framework import serializers
from ttpd_admin.models import (
  AdopterTypes,
  Adopters,
  Agencies,
  Fundings,
  FundingTypes,
  ISPs,
  Industries,
  ProtectionTypes,
  TechCategories,
  Generators,
  TechStatus,
  TechnologyStatuses,
  Technologies,
  Fundings,
  User
)
class IndustriesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_industries_detail')

    class Meta:
        model = Industries
        fields = '__all__'

class ISPsSerializer(serializers.HyperlinkedModelSerializer):
    sector = serializers.ReadOnlyField(source='parent.name')
    industry = serializers.ReadOnlyField(source='parent.parent.name')

    class Meta:
        model = ISPs
        fields = ['name', 'sector', 'industry']

class ProtectionTypesSerializer(serializers.HyperlinkedModelSerializer):
    application_number = serializers.ReadOnlyField(source='protection_type_meta.application_number')
    meta_serial_number = serializers.ReadOnlyField(source='protection_type_meta.meta_serial_number')
    date_of_filing = serializers.ReadOnlyField(source='protection_type_meta.date_of_filing')
    status = serializers.ReadOnlyField(source='protection_type_meta.name')

    class Meta:
        model = ProtectionTypes
        fields = ['protection_type', 'application_number', 'meta_serial_number', 'date_of_filing', 'status']

class TechnologyCategoriesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technology_categories_detail')
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TechCategories
        fields = ['id', 'url', 'name', 'parent']

class AdoptersSerializer(serializers.HyperlinkedModelSerializer):
    adopter_type = serializers.ReadOnlyField(source='adopter_type.name')

    class Meta:
        model = Adopters
        fields = ['id', 'name', 'address', 'phone_number', 'fax_number', 'email_address', 'adopter_type']

class AgenciesSerializer(serializers.HyperlinkedModelSerializer):
    agency_type = serializers.ReadOnlyField(source='agency_type.name')

    class Meta:
        model = Agencies
        fields = ['id', 'name', 'address', 'phone_number', 'fax_number', 'agency_type', 'private_flag']

class FundingsSerializer(serializers.HyperlinkedModelSerializer):
    funding_type = serializers.ReadOnlyField(source='funding_type.name')
    donor = serializers.ReadOnlyField(source='donor.name')
    implementing_agencies = serializers.ReadOnlyField(source='implementing_agencies.name')

    class Meta:
        model = Fundings
        fields = ['id', 
                  'funding_type',  
                  'investment_amount',  
                  'duration_start',  
                  'duration_end',  
                  'donor',
                  'implementing_agencies']

class GeneratorsSerializer(serializers.HyperlinkedModelSerializer):
    agency = serializers.ReadOnlyField(source='agency.name')
    address = serializers.ReadOnlyField(source='agency.address')

    class Meta:
        model = Generators
        fields = ['id', 
                  'title', 
                  'first_name', 
                  'last_name', 
                  'expertise', 
                  'availability', 
                  'agency', 
                  'address']

class TechStatusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TechStatus
        fields = ['name']

    # override string representation
    def to_representation(self, instance):
        status_metadata = TechnologyStatuses.objects.filter(tech_status=instance)[0]

        return {
          'name': instance.name,
          'year_complied': status_metadata.year_complied
        }

class TechnologiesSerializerFirstLevel(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technologies_detail')
    protection_level = serializers.ReadOnlyField(source='protection_level.name')
    region = serializers.ReadOnlyField(source='region.region_normalized_canonical')
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    generators =serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
    industries = IndustriesSerializer(many=True, read_only=True)
    industry_sector_isps = ISPsSerializer(many=True, read_only=True)
    owners = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    statuses = TechStatusSerializer(many=True, read_only=True)

    class Meta:
        model = Technologies
        fields = [
          'id',
          'url',
          'name',
          'year',
          'description',
          'protection_level',
          'industries',
          'region',
          'categories',
          'industry_sector_isps',
          'generators',
          'owners',
          'statuses'
        ]

class TechnologiesSerializerSecondLevel(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technologies_detail')
    protection_level = serializers.ReadOnlyField(source='protection_level.name')
    region = serializers.ReadOnlyField(source='region.region_normalized_canonical')
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    generators = GeneratorsSerializer(many=True, read_only=True)
    industry_sector_isps = ISPsSerializer(many=True, read_only=True)
    owners = AgenciesSerializer(many=True, read_only=True)
    statuses = TechStatusSerializer(many=True, read_only=True)
   # adopters = serializers.SlugRelatedField(many=True, read_only=True, slug_field='adopter_type')
    
    class Meta:
        model = Technologies
        fields = [
          'id',
          'url',
          'name',
          'year',
          'description',
          'protection_level',
          'region',
          'categories',
          'industry_sector_isps',
          'generators',
          'owners',
          'statuses',
    #      'adopters'
        ]

class TechnologiesSerializerThirdLevel(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technologies_detail')
    protection_level = serializers.ReadOnlyField(source='protection_level.name')
    region = serializers.ReadOnlyField(source='region.region_normalized_canonical')
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    generators = GeneratorsSerializer(many=True, read_only=True)
    industry_sector_isps = ISPsSerializer(many=True, read_only=True)
    owners = AgenciesSerializer(many=True, read_only=True)
    statuses = TechStatusSerializer(many=True, read_only=True)
    adopters = AdoptersSerializer(many=True, read_only=True)
    fundings = FundingsSerializer(many=True, read_only=True)

    class Meta:
        model = Technologies
        fields = [
          'id',
          'url',
          'name',
          'year',
          'description',
          'protection_level',
          'region',
          'categories',
          'industry_sector_isps',
          'generators',
          'owners',
          'statuses',
          'adopters',
          'fundings',
        ]

class TechnologiesSearchSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technologies_detail')
    title = serializers.ReadOnlyField(source='name')
    region = serializers.ReadOnlyField(source='region.region_normalized_canonical')
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    industry_sector_isps = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    
    class Meta:
        model = Technologies
        fields = [
          'id',
          'url',
          'title',
          'year',
          'description',
          'region',
          'categories',
          'industry_sector_isps',
        ]

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
          'password': {'write_only': True}
        }

    def create(self, validated_data):
        instance = super(UsersSerializer, self).create(validated_data)

        # update the password to save the hash instead of the plaintext password
        instance.set_password(validated_data.get('password'))

        # TODO: activate the FIXME line below and remove this line and the next line. This is for the sake of DEMO
        #       only.
        instance.is_active = True

        # # FIXME: another field should be used to determine if user is allowed to login or not since django
        # #        documentation says that this field is used for marking the user as soft-deleted.
        # #
        # # do not make the user active immediately. user must be subjected for approval
        # instance.is_active = False

        # Make sure that this user is not a super user and cannot login to the admin interface
        instance.is_superuser = False
        instance.is_staff = False

        # assign level one and level two roles automatically to the user
        assign_role(instance, 'level_one_user')
        assign_role(instance, 'level_two_user')

        # finally, update the user data since we updated some fields
        instance.save()

        return instance


