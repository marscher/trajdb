# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    length = models.IntegerField()
    n_atoms = models.IntegerField()
    setup_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'Collection'


class Collectionownership(models.Model):
    collection_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'CollectionOwnership'
        unique_together = (('collection_id', 'user_id'),)


class Groupmembership(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'GroupMembership'
        unique_together = (('group_id', 'user_id'),)


class Groups(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1)
    organisation = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Groups'


class Trajectory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent_traj = models.ForeignKey('self', blank=True, null=True)
    collection = models.ForeignKey(Collection)
    uri = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'Trajectory'

# TODO: check if it is valid to re-use the django internal user management here.
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=1)
    mail = models.CharField(max_length=1)
    password = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'User'
