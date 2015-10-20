# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase

from . import models


class TestProfileModel(TestCase):

    def test_profile_creation(self):
        User = get_user_model()
        # New user created
        user = User.objects.create(
            username="test_user", password="test_pw")
        # Check that a Profile instance has been crated
        self.assertIsInstance(user.profile, models.Profile)
        # Call the save method of the user to activate the signal
        # again, and check that it doesn't try to create another
        # profile instace
        user.save()
        self.assertIsInstance(user.profile, models.Profile)


class TestTrajCreation(TestCase):

    def test_traj_creation(self):
        # cumulative length in collection trigger test
        User = get_user_model()
        user = User.objects.create(
            username="test_user", password="test_pw")
        user.save()

        setup = models.Setup(description="bla blah", pdb='x87d', program="gromacs",
                             program_version='4.93', topology=0x0,
                             topology_type='pdb', forcefield_name='amber99')
        setup.save()

        coll = models.Collection(n_atoms=10, setup=setup, owner=user.profile)
        coll.save()

        traj = models.Trajectory(name='foo', length=42, collection=coll,
                                 hash_sha512=('8f6d4153690222a53355aa6d50206dc2d'
                                              '2582eb9a8e3a1386a876c0cf9995e1ae0'
                                              '671d3d0e70ddef25881c9513245acd0e5'
                                              '3b9e3e85fcf799fde70c6d836e2bb'))
        traj.save()
        traj2 = models.Trajectory(name='foo2', length=23, collection=coll,
                                  hash_sha512=('2f6d4153690222a53355aa6d50206dc2d'
                                               '2582eb9a8e3a1386a876c0cf9995e1ae0'
                                               '671d3d0e70ddef25881c9513245acd0e5'
                                               '3b9e3e85fcf799fde70c6d836e2bb'))

        traj2.save()
        assert coll.cumulative_length == traj.length + traj2.length


class TestSetup(TestCase):
    def test_setup_creation(self):
        pass