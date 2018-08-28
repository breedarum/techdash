# roles.py
#
# Copyright(c) Exequiel Ceasar Navarrete <esnavarrete1@up.edu.ph>
# Licensed under MIT
# Version 1.0.0-alpha1

from rolepermissions.roles import AbstractUserRole
from funcy import project

DEFAULT_PERMS = {
  'create_user': True,
  'list_user': True,
  'update_user': True,
  'remove_user': True,
  'view_user': True,

  'create_adopters': True,
  'list_adopters': True,
  'update_adopters': True,
  'remove_adopters': True,
  'view_adopters': True,

  'create_agencies': True,
  'list_agencies': True,
  'update_agencies': True,
  'remove_agencies': True,
  'view_agencies': True,

  'create_agencytypes': True,
  'list_agencytypes': True,
  'update_agencytypes': True,
  'remove_agencytypes': True,
  'view_agencytypes': True,

  'create_commercializationmodes': True,
  'list_commercializationmodes': True,
  'update_commercializationmodes': True,
  'remove_commercializationmodes': True,
  'view_commercializationmodes': True,

  'create_commodities': True,
  'list_commodities': True,
  'update_commodities': True,
  'remove_commodities': True,
  'view_commodities': True,

  'create_industrysectors': True,
  'list_industrysectors': True,
  'update_industrysectors': True,
  'remove_industrysectors': True,
  'view_industrysectors': True,

  'create_potentialadopters': True,
  'list_potentialadopters': True,
  'update_potentialadopters': True,
  'remove_potentialadopters': True,
  'view_potentialadopters': True,

  'create_protectionlevels': True,
  'list_protectionlevels': True,
  'update_protectionlevels': True,
  'remove_protectionlevels': True,
  'view_protectionlevels': True,

  'create_protectiontypes': True,
  'list_protectiontypes': True,
  'update_protectiontypes': True,
  'remove_protectiontypes': True,
  'view_protectiontypes': True,

  'create_technologies': True,
  'list_technologies': True,
  'update_technologies': True,
  'remove_technologies': True,
  'view_technologies': True,

  'create_technologyfundingtypes': True,
  'list_technologyfundingtypes': True,
  'update_technologyfundingtypes': True,
  'remove_technologyfundingtypes': True,
  'view_technologyfundingtypes': True,

  'create_technologygenerators': True,
  'list_technologygenerators': True,
  'update_technologygenerators': True,
  'remove_technologygenerators': True,
  'view_technologygenerators': True,

  'create_technologyprotectionstatus': True,
  'list_technologyprotectionstatus': True,
  'update_technologyprotectionstatus': True,
  'remove_technologyprotectionstatus': True,
  'view_technologyprotectionstatus': True,

  'create_techstatus': True,
  'list_techstatus': True,
  'update_techstatus': True,
  'remove_techstatus': True,
  'view_techstatus': True,

  # User Levels which will be used only for the frontend facing application
  'level_one': True,
  'level_two': True,
  'level_three': True,
  'level_four': True # Existent only in IP Protected Data
}

class Admin(AbstractUserRole):
    available_permissions = DEFAULT_PERMS

class Staff(AbstractUserRole):
    available_permissions = project(DEFAULT_PERMS, [
      'create_technologies',
      'list_technologies',
      'update_technologies',
      'remove_technologies',
      'view_technologies'
    ])

class LevelOneUser(AbstractUserRole):
    available_permissions = project(DEFAULT_PERMS, [
      'list_technologies',
      'level_one'
    ])

class LevelTwoUser(AbstractUserRole):
    available_permissions = project(DEFAULT_PERMS, [
      'list_technologies',
      'level_one',
      'level_two'
    ])

class LevelThreeUser(AbstractUserRole):
    available_permissions = project(DEFAULT_PERMS, [
      'list_technologies',
      'level_one',
      'level_two',
      'level_three'
    ])

class LevelFourUser(AbstractUserRole):
    available_permissions = project(DEFAULT_PERMS, [
      'list_technologies',
      'level_one',
      'level_two',
      'level_three',
      'level_four'
    ])


