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

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from . import managers


class Profile(models.Model):
    """A Profile encapsulates an authenticated user. One authed user has
       exactly one profile.
    """
    # Relations
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        verbose_name=_("user")
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


class Setup(models.Model):
    """ Setup contains the simulation setup like used topology and forcefield
    parameters.
    """
    #id = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=1000)
    pdb = models.CharField(max_length=4)
    program = models.CharField(max_length=20)
    program_version = models.CharField(max_length=10)
    topology = models.BinaryField()
    # TODO: replace with choices?
    topology_type = models.CharField(max_length=4)
    forcefield_name = models.CharField(max_length=20)
    forcefield_parameters = models.BinaryField()
    forcefield_parameters_type = models.CharField(max_length=4)


class Collection(models.Model):
    """ A collection is associated to one setup and owner.
    """
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    n_atoms = models.IntegerField(help_text='Number of atoms/particles in the simulation.')
    cumulative_length = models.PositiveIntegerField(default=0)
    setup = models.ForeignKey(Setup)
    owner = models.ForeignKey(Profile)


class Trajectory(models.Model):
    """Stores a trajectory file associated to a collection.
    Has a unique hash (sha512).
    Might refer to a parent trajectory from which the actual has been forked from.
    """
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    length = models.PositiveIntegerField()
    parent_traj = models.ForeignKey('self', blank=True, null=True)
    collection = models.ForeignKey(Collection)
    uri = models.CharField(max_length=1000)
    hash_sha512 = models.CharField(max_length=128, unique=True, blank=False)


@receiver(post_save, sender=Trajectory)
def update_cumulative_simulation_len(sender, created, instance, **kw):
    if created:
        assert isinstance(instance, Trajectory)
        instance.collection.cumulative_length += instance.length
        instance.collection.save()
        print "len:", instance.collection.cumulative_length
