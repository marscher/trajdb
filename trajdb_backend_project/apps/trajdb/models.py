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
from django.db.models.signals import post_save
from django.dispatch import receiver

from .traj_storage import TrajStorage


class Setup(models.Model):
    """ Setup contains the simulation setup like used topology and forcefield
    parameters.
    """
    description = models.CharField(max_length=1000)
    pdb = models.CharField(max_length=4)

    program = models.CharField(max_length=20)
    program_version = models.CharField(max_length=10)

    water_model = models.CharField(max_length=20)

    topology = models.BinaryField()
    topology_type = models.CharField(max_length=8)

    forcefield_name = models.CharField(max_length=20)
    forcefield_parameters = models.BinaryField()
    forcefield_parameters_type = models.CharField(max_length=4)

    run_script = models.TextField(blank=True, null=True,
                                  help_text='optional script to run a simulation with this setup')

    owner = models.ForeignKey('auth.User')

    def runable(self):
        """ is this Setup runable? """
        return self.run_script is not None


class Collection(models.Model):
    """ A collection is associated to one setup and owner.
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    n_atoms = models.IntegerField(
        help_text='Number of atoms/particles in the simulation.')
    cumulative_length = models.PositiveIntegerField(default=0, blank=True)
    setup = models.ForeignKey(Setup)
    owner = models.ForeignKey('auth.User', related_name='collection')


class MetaCollection(models.Model):
    """ allows to create further abstract collections. A collection can be
    part of none or many meta collections. A meta collection contains multiple collections."""

    name = models.CharField(max_length=100)
    collection = models.ManyToManyField(Collection)
    owner = models.ForeignKey('auth.User')


class Trajectory(models.Model):
    """Stores a trajectory file associated to a collection.
    Has a unique hash (sha512).
    Can refer to a parent trajectory from which the actual has been forked from.
    """
    name = models.CharField(max_length=255)
    data = models.FileField()#storage=TrajStorage, blank=True, null=True)
    length = models.PositiveIntegerField(help_text='length in frames', default=0)
    parent_traj = models.ForeignKey('self', blank=True, null=True)
    collection = models.ForeignKey(Collection)

    uri = models.CharField(max_length=1000)
    hash_sha512 = models.CharField(max_length=128, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='trajectory')


@receiver(post_save, sender=Trajectory)
def update_cumulative_simulation_len(sender, created, instance, **kw):
    # once we've (successfully) created a trajectory, increment the sum of frames
    # in the associated collection.
    if created:
        instance.collection.cumulative_length += instance.length
        # TODO: determine length with mdtraj etc.
        instance.length = 0
        instance.collection.save()
