from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.trajdb.filehandling.traj_storage import TrajStorage
from trajdb import settings
import os

fs = TrajStorage(settings.MEDIA_ROOT)

fs2 = TrajStorage(settings.MEDIA_ROOT)


def _upload_topology_file_path(instance, filename):
    # store topology file in the collection space
    import uuid
    _, ext = os.path.splitext(filename)
    new_fn = uuid.uuid5(uuid.NAMESPACE_DNS, filename).hex
    new_name = '/'.join((settings.TRAJ_SUBDIR, 'top', new_fn)) + ext
    return new_name


def _upload_trajectory_file_path(traj_inst, filename):
    _, ext = os.path.splitext(filename)
    coll = traj_inst.collection.id
    trajs_in_collection = Trajectory.objects.filter(
        collection__id=coll).count()

    count_nr = "{:0>6d}".format(trajs_in_collection)

    return '/'.join((settings.TRAJ_SUBDIR, traj_inst.collection.name,
                     traj_inst.collection.setup.name + "_" + count_nr + ext))


class Topology(models.Model):
    n_atoms = models.PositiveIntegerField(null=True)
    n_residues = models.PositiveIntegerField(null=True)
    n_chains = models.PositiveIntegerField(default=1)

    unitcell_vectors = models.CharField(max_length=200, blank=True, null=True)
    unitcell_angles = models.CharField(max_length=200, null=True)
    unitcell_volume = models.FloatField(
        help_text='box volume in [nm]^3', null=True)

    top_file = models.FileField(
        storage=fs2, upload_to=_upload_topology_file_path)
    pdb_id = models.CharField(max_length=4, blank=True, null=True,
                              help_text='if this topology is derived from an entry'
                              ' in protein database, please link it here.')
    #type = models.CharField(max_length=10, blank=True, null=True, default='pdb')

    def save(self, *args, **kw):
        if not self.pk:  # new object
            #print(self.top_file.name, self.top_file.path)
            instance = self
            import mdtraj

            # TODO: avoid this hack of symlinking the temporary file
            top_file_faked = instance.top_file.path
            top_file_real = instance.top_file.file.file.name
            os.symlink(top_file_real, top_file_faked)

            top = mdtraj.load(top_file_faked)

            instance.n_atoms = top.n_atoms
            instance.n_residues = top.n_residues
            instance.n_chains = top.n_chains

            instance.unitcell_volume = top.unitcell_volumes[0]
            instance.unitcell_vectors = top.unitcell_vectors
            instance.unitcell_angles = top.unitcell_angles

        super(Topology, self).save(*args, **kw)


# @receiver(post_save)
# def set_topology_attributes(sender, instance, *args, **kw):
#     import mdtraj
#     # TODO: handle errors (eg. non parseable file etc.)
#     top = mdtraj.load(instance.top_file.path)
#
#     update_args = dict(n_atoms =top.n_atoms,
#                    n_residues= top.n_residues,
#                    n_chains= top.n_chains,
#                    unitcell_volume= top.unitcell_volumes[0],
#                    unitcell_vectors= top.unitcell_vectors,
#                    unitcell_angles=top.unitcell_angles)
#
# #     instance.n_atoms = top.n_atoms
# #     instance.n_residues = top.n_residues
# #     instance.n_chains = top.n_chains
# #
# #     instance.volume = top.unitcell_volumes[0]
# #     instance.box_vectors = top.unitcell_vectors
# #     instance.box_angles = top.unitcell_angles
#
#     Topology.objects.filter(pk=instance.pk).update(**update_args)


class Setup(models.Model):
    """ Setup contains the simulation setup like used topology and forcefield
    parameters.
    """
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=1000)

    temperature = models.IntegerField(help_text="simulation temperature in K")

    program = models.CharField(max_length=20)
    program_version = models.CharField(max_length=10)

    water_model = models.CharField(max_length=20)

    topology = models.ForeignKey(Topology)

    forcefield_name = models.CharField(max_length=20)
    # TODO: make this another field?
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
    data = models.FileField(storage=fs, upload_to=_upload_trajectory_file_path)
    length = models.PositiveIntegerField(
        help_text='length in frames', default=0)
    parent_traj = models.ForeignKey('self', blank=True, null=True)
    collection = models.ForeignKey(Collection)

    uri = models.CharField(max_length=1000)
    # TODO: unique -> true + check
    hash_sha512 = models.CharField(max_length=128, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='trajectory')

    def save(self, *args, **kw):
        if not self.pk:  # new file
            import hashlib
            func = hashlib.sha512()
            for chunk in self.data.chunks():
                func.update(chunk)

            computed_hash = func.hexdigest()
            if not computed_hash == self.hash_sha512:
                # TODO: more django style exception handling?
                raise Exception("uploaded trajectory has different hash value than promised: "
                                "promised = \t\t%s\ncomputed on server side:\t%s"
                                % (self.hash_sha512, computed_hash))

        super(Trajectory, self).save(*args, **kw)


def determine_length(file):
    import mdtraj
    try:
        with mdtraj.open(file) as fh:
            return len(fh)
    except:
        raise


@receiver(post_save, sender=Trajectory)
def update_cumulative_simulation_len(sender, created, instance, **kw):
    # once we've (successfully) created a trajectory, increment the sum of frames
    # in the associated collection.
    if created:
        # determine length of file
        instance.length = determine_length(instance.data.path)
        # update cumulative length
        instance.collection.cumulative_length += instance.length
        instance.collection.save()

        # move_traj_data_to_collection_subfolder(instance)
