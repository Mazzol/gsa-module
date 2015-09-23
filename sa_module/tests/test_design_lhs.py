"""Unit test class to test the implementation of LHS design generator
"""
import unittest
import env
import numpy as np
from samples import design_lhs

__author__ = "Damar Wicaksono"


class DesignLHSTestCase(unittest.TestCase):
    """Tests for design_lhs.py"""

    def setUp(self):
        """Test fixture build"""
        self.seed = 7893457     # Seed number
        self.n = 100            # Number of samples
        self.d = 20             # Number of dimension
        self.dm = design_lhs.create(self.n, self.d, self.seed)

    def test_is_n_other_than_integer_acceptable(self):
        """Is other than integer for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, 25.8, self.d, self.seed)

    def test_is_n_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, -100, self.d, self.seed)

    def test_is_d_other_than_integer_acceptable(self):
        """Is other than integer for the number of dimensions acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, "ab", self.seed)

    def test_is_d_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, -15, self.seed)

    def test_is_seed_other_than_integer_acceptable(self):
        """Is other than integer for the seed number accepatable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, self.d, 1.234)

    def test_is_n_negative_acceptable(self):
        """Is a negative value for the number of samples acceptable?"""
        self.assertRaises(TypeError, design_lhs.create, self.n, self.d, -123)

    def test_is_100_the_correct_num_samples(self):
        """Is 100 the number of generated samples?"""
        self.assertEqual(self.dm.shape[0], self.n)

    def test_is_20_the_correct_num_dimension(self):
        """Is 20 the number of dimension?"""
        self.assertEqual(self.dm.shape[1], self.d)

    def test_is_dm_repeatable(self):
        """Is the design matrix repeatable given the same seed number?"""
        new_seed = self.seed
        new_n = self.n
        new_d = self.d
        new_dm = design_lhs.create(new_n, new_d, new_seed)
        for i in range(self.dm.shape[0]):
            for j in range(self.dm.shape[1]):
                self.assertEqual(self.dm[i,j], new_dm[i,j])

    def test_is_dm_below_one(self):
        """Is the element values in the design matrix less than 1.0?"""
        for i in range(self.dm.shape[0]):
            for j in range(self.dm.shape[1]):
                self.assertLess(self.dm[i, j], 1.0)

    def test_is_dm_above_zero(self):
        """Is the element values in the design matrix greater than 0.0?"""
        for i in range(self.dm.shape[0]):
            for j in range(self.dm.shape[1]):
                self.assertGreater(self.dm[i,j], 0.0)

if __name__ == "__main__":
    unittest.main()