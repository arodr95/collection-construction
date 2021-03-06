import unittest

from sorted_frozen_set import SortedFrozenSet


class TestConstruction(unittest.TestCase):

    def test_construct_empty(self):
        s = SortedFrozenSet([])

    def test_construct_nonempty_list(self):
        s = SortedFrozenSet([2, 4, 9])

    def test_construct_from_iterator(self):
        items = [2, 4, 9]
        iterator = iter(items)
        s = SortedFrozenSet(iterator)

    def test_construct_no_args(self):
        s = SortedFrozenSet()


class TestContainerProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedFrozenSet([3, 4, 6, 9])

    def test_positive_contained(self):
        self.assertTrue(3 in self.s)

    def test_negative_contained(self):
        self.assertFalse(5 in self.s)

    def test_positive_not_contained(self):
        self.assertTrue(7 not in self.s)

    def test_negative_not_contained(self):
        self.assertFalse(9 not in self.s)


class TestSizedProtocol(unittest.TestCase):

    def test_empty_with_default(self):
        s = SortedFrozenSet()
        self.assertEqual(len(s), 0)

    def test_empty(self):
        s = SortedFrozenSet([])
        self.assertEqual(len(s), 0)

    def test_one(self):
        s = SortedFrozenSet([38])
        self.assertEqual(len(s), 1)

    def test_multiple(self):
        s = SortedFrozenSet(range(17))
        self.assertEqual(len(s), 17)


class TestIterableProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedFrozenSet([7, 2, 1, 1, 9])

    def test_iter(self):
        iterator = iter(self.s)
        self.assertEqual(next(iterator), 1)
        self.assertEqual(next(iterator), 2)
        self.assertEqual(next(iterator), 7)
        self.assertEqual(next(iterator), 9)
        self.assertRaises(
            StopIteration,
            lambda: next(iterator)
        )

    def test_for_loop(self):
        expected = [1, 2, 7, 9]
        index = 0
        for item in expected:
            self.assertEqual(item, expected[index])
            index += 1


class TestSequenceProtocol(unittest.TestCase):

    def setUp(self):
        self.s = SortedFrozenSet([1, 4, 9, 13, 15])

    # Indexing
    def test_index_zero(self):
        self.assertEqual(self.s[0], 1)

    def test_index_four(self):
        self.assertEqual(self.s[4], 15)

    def test_index_one_beyond_end(self):
        with self.assertRaises(IndexError):
            self.s[5]

    def test_index_minus_one(self):
        self.assertEqual(self.s[-1], 15)

    def test_index_minus_five(self):
        self.assertEqual(self.s[-5], 1)

    def test_index_one_before_beginning(self):
        with self.assertRaises(IndexError):
            self.s[-6]

    # Slicing
    def test_slice_from_start(self):
        self.assertEqual(self.s[:2], SortedFrozenSet([1, 4]))

    def test_slice_to_end(self):
        self.assertEqual(self.s[3:], SortedFrozenSet([13, 15]))

    def test_slice_empty(self):
        self.assertEqual(self.s[10:], SortedFrozenSet())

    def test_slice_arbitrary(self):
        self.assertEqual(self.s[1:4], SortedFrozenSet([4, 9, 13]))

    def test_slice_step(self):
        self.assertEqual(self.s[0:5:2], SortedFrozenSet([1, 9, 15]))

    def test_slice_full(self):
        self.assertEqual(self.s[:], self.s)

    # Reversed
    def test_reversed(self):
        s = SortedFrozenSet([1, 3, 5, 7])
        r = reversed(s)
        self.assertEqual(next(r), 7)
        self.assertEqual(next(r), 5)
        self.assertEqual(next(r), 3)
        self.assertEqual(next(r), 1)
        self.assertRaises(
            StopIteration,
            lambda: next(r)
        )

    # Index
    def test_index_positive(self):
        s = SortedFrozenSet([1, 5, 8, 9])
        self.assertEqual(s.index(5), 1)

    def test_index_negative(self):
        s = SortedFrozenSet([1, 5, 8, 9])
        with self.assertRaises(ValueError):
            s.index(10)

    # Count
    def test_count_zero(self):
        s = SortedFrozenSet([1, 5, 7, 9])
        self.assertEqual(s.count(12), 0)

    def test_count_one(self):
        s = SortedFrozenSet([1, 5, 7, 9])
        self.assertEqual(s.count(9), 1)

    # Concatenation
    def test_add_disjoin(self):
        s = SortedFrozenSet([1, 2, 3])
        t = SortedFrozenSet([4, 5, 6])
        self.assertEqual(s + t, SortedFrozenSet([1, 2, 3, 4, 5, 6]))

    def test_add_equal(self):
        s = SortedFrozenSet([7, 8, 9])
        self.assertEqual(s + s, SortedFrozenSet([7, 8, 9]))

    def test_add_intersecting(self):
        s = SortedFrozenSet([1, 2, 3])
        t = SortedFrozenSet([3, 4, 5])
        self.assertEqual(s + t, SortedFrozenSet([1, 2, 3, 4, 5]))

    def test_add_type_error_left(self):
        s = SortedFrozenSet([1, 2, 3])
        t = (4, 5, 6)
        with self.assertRaises(TypeError):
            _ = s + t

    def test_add_type_error_right(self):
        s = (1, 2, 3)
        t = SortedFrozenSet([4, 5, 6])
        with self.assertRaises(TypeError):
            _ = s + t

    # Repetition
    def test_repetition_zero_right(self):
        s = SortedFrozenSet([1, 2, 3])
        self.assertEqual(s * 0, SortedFrozenSet())

    def test_repetition_negative_right(self):
        s = SortedFrozenSet([4, 5, 6])
        self.assertEqual(s * -1, SortedFrozenSet())

    def test_repetition_nonzero_right(self):
        s = SortedFrozenSet([7, 8, 9])
        self.assertEqual(s * 1000, s)

    def test_repetition_zero_left(self):
        s = SortedFrozenSet([1, 2, 3])
        self.assertEqual(0 * s, SortedFrozenSet())

    def test_repetition_negative_left(self):
        s = SortedFrozenSet([4, 5, 6])
        self.assertEqual(-1 * s, SortedFrozenSet())

    def test_repetition_nonzero_left(self):
        s = SortedFrozenSet([7, 8, 9])
        self.assertEqual(1000 * s, s)


class TestReprProtocol(unittest.TestCase):

    def test_repr_empty(self):
        s = SortedFrozenSet()
        self.assertEqual(repr(s), "SortedFrozenSet()")

    def test_repr_one(self):
        s = SortedFrozenSet([12, 18, 39])
        self.assertEqual(repr(s), "SortedFrozenSet([12, 18, 39])")


class TestEqualityProtocol(unittest.TestCase):

    def test_positive_equal(self):
        self.assertTrue(SortedFrozenSet([7, 8, 9]) == SortedFrozenSet([9, 8, 7]))

    def test_negative_equal(self):
        self.assertFalse(SortedFrozenSet([7, 8, 9]) == SortedFrozenSet([4, 5, 6]))

    def test_type_mismatch(self):
        self.assertFalse(SortedFrozenSet([1, 2, 3]) == [1, 2, 3])

    def test_identical(self):
        s = SortedFrozenSet([4, 5, 6])
        self.assertTrue(s == s)


class TestInequalityProtocol(unittest.TestCase):

    def test_positive_unequal(self):
        self.assertTrue(SortedFrozenSet([1, 2, 3]) != SortedFrozenSet([4, 5, 6]))

    def test_negative_unequal(self):
        self.assertFalse(SortedFrozenSet([7, 8, 9]) != SortedFrozenSet([7, 8, 9]))

    def test_type_mismatch(self):
        self.assertTrue(SortedFrozenSet([4, 5, 6]) != [4, 5, 6])

    def test_identical(self):
        s = SortedFrozenSet([1, 2, 3])
        self.assertFalse(s != s)


class TestHashableProtocol(unittest.TestCase):

    def test_equal_sets_have_same_hash_code(self):
        self.assertEqual(
            hash(SortedFrozenSet([5, 2, 1, 4])),
            hash(SortedFrozenSet([5, 2, 1, 4]))
        )


if __name__ == '__main__':
    unittest.main()