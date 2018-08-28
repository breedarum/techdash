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


