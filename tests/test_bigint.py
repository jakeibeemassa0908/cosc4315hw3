import infinitearithmetic._bigint as bigint

def test_fromstring():
    # Converts with nodesize of 1
    assert(bigint.fromstring('500', 1) == bigint.BigInt([0, 0, 5], 1))

    # Converts with nodesize of 2
    assert(bigint.fromstring('545', 2) == bigint.BigInt([45, 5], 2))

    # Converts with nodesize of 5
    assert(bigint.fromstring('123456', 5) == bigint.BigInt([23456, 1], 5))

    # Converts with nodesize of 10
    assert(bigint.fromstring('59832345678901', 10) == bigint.BigInt([2345678901, 5983], 10))