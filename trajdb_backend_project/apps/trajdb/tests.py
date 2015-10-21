# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from django.core.files import File

from . import models


class TestTrajCreation(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create(
            username="test_user", password="test_pw")
        user.save()
        with open('dummy', 'w') as fh:
            fh.write("dummy")
        self.file = File(open('dummy'), 'dummy')

        # cumulative length in collection trigger test

        setup = models.Setup(description="bla blah", pdb='x87d', program="gromacs",
                             program_version='4.93', topology=self.file,
                             topology_type='pdb', forcefield_name='amber99')
        setup.save()

        self.coll = models.Collection(
            n_atoms=10, setup=setup, owner=user.profile)
        self.coll.save()

    def test_traj_creation(self):
        traj = models.Trajectory(name='foo', data=self.file, length=42, collection=self.coll,
                                 hash_sha512=('8f6d4153690222a53355aa6d50206dc2d'
                                              '2582eb9a8e3a1386a876c0cf9995e1ae0'
                                              '671d3d0e70ddef25881c9513245acd0e5'
                                              '3b9e3e85fcf799fde70c6d836e2bb'))
        traj.save()
#         traj2 = models.Trajectory(name='foo2', data=self.file, length=23, collection=self.coll,
#                                   hash_sha512=('2f6d4153690222a53355aa6d50206dc2d'
#                                                '2582eb9a8e3a1386a876c0cf9995e1ae0'
#                                                '671d3d0e70ddef25881c9513245acd0e5'
#                                                '3b9e3e85fcf799fde70c6d836e2bb'))
# 
#         traj2.save()
#         assert self.coll.cumulative_length == traj.length + traj2.length


class TestSetup(TestCase):

    def test_setup_creation(self):
        pass
