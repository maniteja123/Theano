__docformat__ = "restructuredtext en"

import sys
import unittest
import numpy 

from theano.tensor.randomstreams import RandomStreams, raw_random
from theano.compile import Module, Method, Member

from theano import tensor
from theano import compile, gof


class T_RandomStreams(unittest.TestCase):
    def test_basics(self):
        m = Module()
        m.random = RandomStreams(234)
        m.fn = Method([], m.random.uniform((2,2)))
        m.gn = Method([], m.random.normal((2,2)))
        made = m.make()
        made.random.initialize()

        fn_val0 = made.fn()
        fn_val1 = made.fn()

        gn_val0 = made.gn()

        rng_seed = numpy.random.RandomState(234).randint(2**30)
        rng = numpy.random.RandomState(int(rng_seed)) #int() is for 32bit

        #print fn_val0
        numpy_val0 = rng.uniform(size=(2,2))
        numpy_val1 = rng.uniform(size=(2,2))
        #print numpy_val0

        assert numpy.all(fn_val0 == numpy_val0)
        assert numpy.all(fn_val1 == numpy_val1)

    def test_seed_in_initialize(self):
        m = Module()
        m.random = RandomStreams(234)
        m.fn = Method([], m.random.uniform((2,2)))
        made = m.make()
        made.random.initialize(seed=888)

        fn_val0 = made.fn()
        fn_val1 = made.fn()

        rng_seed = numpy.random.RandomState(888).randint(2**30)
        rng = numpy.random.RandomState(int(rng_seed))  #int() is for 32bit

        #print fn_val0
        numpy_val0 = rng.uniform(size=(2,2))
        numpy_val1 = rng.uniform(size=(2,2))
        #print numpy_val0

        assert numpy.all(fn_val0 == numpy_val0)
        assert numpy.all(fn_val1 == numpy_val1)

    def test_seed_fn(self):
        m = Module()
        m.random = RandomStreams(234)
        m.fn = Method([], m.random.uniform((2,2)))
        made = m.make()
        made.random.initialize(seed=789)

        made.random.seed(888)

        fn_val0 = made.fn()
        fn_val1 = made.fn()

        rng_seed = numpy.random.RandomState(888).randint(2**30)
        rng = numpy.random.RandomState(int(rng_seed))  #int() is for 32bit

        #print fn_val0
        numpy_val0 = rng.uniform(size=(2,2))
        numpy_val1 = rng.uniform(size=(2,2))
        #print numpy_val0

        assert numpy.all(fn_val0 == numpy_val0)
        assert numpy.all(fn_val1 == numpy_val1)

    def test_getitem(self):

        m = Module()
        m.random = RandomStreams(234)
        out = m.random.uniform((2,2))
        m.fn = Method([], out)
        made = m.make()
        made.random.initialize(seed=789)

        made.random.seed(888)

        rng = numpy.random.RandomState()
        rng.set_state(made.random[out.rng].get_state())

        fn_val0 = made.fn()
        fn_val1 = made.fn()
        numpy_val0 = rng.uniform(size=(2,2))
        numpy_val1 = rng.uniform(size=(2,2))
        assert numpy.all(fn_val0 == numpy_val0)
        assert numpy.all(fn_val1 == numpy_val1)

    def test_setitem(self):

        m = Module()
        m.random = RandomStreams(234)
        out = m.random.uniform((2,2))
        m.fn = Method([], out)
        made = m.make()
        made.random.initialize(seed=789)

        made.random.seed(888)

        rng = numpy.random.RandomState(823874)
        made.random[out.rng] = numpy.random.RandomState(823874)

        fn_val0 = made.fn()
        fn_val1 = made.fn()
        numpy_val0 = rng.uniform(size=(2,2))
        numpy_val1 = rng.uniform(size=(2,2))
        assert numpy.all(fn_val0 == numpy_val0)
        assert numpy.all(fn_val1 == numpy_val1)


if __name__ == '__main__':
    from theano.tests import main
    main("test_randomstreams")
