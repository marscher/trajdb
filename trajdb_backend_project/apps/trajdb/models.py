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
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from . import managers

class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        verbose_name=_("user")
        )
    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
        default=0,
        verbose_name=_("interaction")
        )
    # Attributes - Optional
    # Object Manager
    objects = managers.ProfileManager()
 
    # Custom Properties
    @property
    def username(self):
        return self.user.username
 
    # Methods
 
    # Meta and String
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
        ordering = ("user",)
 
    def __str__(self):
        return self.user.username 

class Setup(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=1000)
    pdb = models.CharField(max_length=4)
    program = models.CharField(max_length=20)
    program_version = models.CharField(max_length=10)
    topology = models.BinaryField()
    topology_type = models.CharField(max_length=4) # TODO: replace with choices?
    forcefield_name = models.CharField(max_length=20)
    forcefield_parameters = models.BinaryField()
    forcefield_parameters_type = models.CharField(max_length=4)


class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    length = models.IntegerField()
    n_atoms = models.IntegerField()
    setup = models.ForeignKey(Setup)
    owner = models.ForeignKey(Profile)

class Collectionownership(models.Model):
    id = models.IntegerField(primary_key=True)
    collection_id = models.ForeignKey(Collection)
    profile_id = models.ForeignKey(Profile)

class Trajectory(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    parent_traj = models.ForeignKey('self', blank=True, null=True)
    collection = models.ForeignKey(Collection)
    uri = models.CharField(max_length=1000)


