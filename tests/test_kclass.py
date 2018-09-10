import unittest

from kformat.kclass import kclass
from kformat.kproperty import AN, N


class TestKClass(unittest.TestCase):

    def test_kclass_init(self):

        @kclass
        class Other:
            n: N(5)
            an: AN(10)

        @kclass
        class Something:
            n: N(10)
            an: AN(20)
            other: Other
            filler: AN(100)

        sth = Something(
            123,
            'k-class',
            Other(456, 'subclass'),
            None
        )
        self.assertIsNotNone(sth)

    def test_kclass_to_bytes(self):
        _n, N.to_bytes = N.to_bytes, lambda s, v: b'N'
        _an, AN.to_bytes = AN.to_bytes, lambda s, v: b'AN'

        @kclass
        class Other:
            an: AN(10)
            n: N(5)

        @kclass
        class Something:
            a: N(10)
            b: AN(20)
            other: Other
            c: N(5)
            d: AN(10)

        sth = Something(1, 2, Other(3, 4), 5, 6)
        self.assertEqual(sth.bytes, b'NANANNNAN')

        # Reset to_bytes funcs to default
        N.to_bytes = _n
        AN.to_bytes = _an
