# serializers.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from rolepermissions.roles import assign_role
from rest_framework import serializers
from ttpd_admin.models import (
  Commodities,
  Industries,
  ProtectionLevels,
  TechCategories,
  Generators,
  TechStatus,
  Technologies,
  User
)

class CommoditiesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_commodities_detail')

    class Meta:
        model = Commodities
        fields = '__all__'

class IndustriesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_industries_detail')

    class Meta:
        model = Industries
        fields = '__all__'

class ProtectionLevelsSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_protection_levels_detail')

    class Meta:
        model = ProtectionLevels
        fields = '__all__'

class TechnologyCategoriesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technology_categories_detail')
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TechCategories
        fields = ['id', 'url', 'name', 'parent']

class GeneratorsSerializer(serializers.HyperlinkedModelSerializer):
    agency = serializers.ReadOnlyField(source='agency.name')

    class Meta:
        model = Generators
        fields = ['id', 'title', 'first_name', 'last_name', 'availability', 'agency']

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

class TechnologiesSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api_technologies_detail')
    protection_level = serializers.ReadOnlyField(source='protection_level.name')
    region = serializers.ReadOnlyField(source='region.region_normalized_canonical')
    categories = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    commodities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    generators = GeneratorsSerializer(many=True, read_only=True)
    industry_sector_isps = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
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
          'region',
          'categories',
          'commodities',
          'industry_sector_isps',
          'generators',
          'owners',
          'statuses'
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


