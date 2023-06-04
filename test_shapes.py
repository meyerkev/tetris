import shapes

def test_q():
    q = shapes.get_shape("Q")
    assert q.width == 2
    assert q.height == 2
    assert q.tops == [2, 2]
    assert q.bottoms == [0, 0]

def test_s():
    s = shapes.get_shape("S")
    assert s.width == 3
    assert s.height == 2
    assert s.tops == [1, 2, 2]
    assert s.bottoms == [0, 0, 1]

def test_z():
    z = shapes.get_shape("Z")
    assert z.width == 3
    assert z.height == 2
    assert z.tops == [2, 2, 1]
    assert z.bottoms == [1, 0, 0]

def test_t():
    t = shapes.get_shape("T")
    assert t.width == 3
    assert t.height == 2
    assert t.tops == [2, 2, 2]
    assert t.bottoms == [1, 0, 1]

def test_i():
    i = shapes.get_shape("I")
    assert i.width == 4
    assert i.height == 1
    assert i.tops == [1, 1, 1, 1]
    assert i.bottoms == [0, 0, 0, 0]

def test_l():
    l = shapes.get_shape("L")
    assert l.width == 2
    assert l.height == 3
    assert l.tops == [3, 1]
    assert l.bottoms == [0, 0]

def test_j():
    j = shapes.get_shape("J")
    assert j.width == 2
    assert j.height == 3
    assert j.tops == [1, 3]
    assert j.bottoms == [0, 0]

def test_get_shape():
    assert shapes.get_shape("Q") == shapes.Q
    assert shapes.get_shape("S") == shapes.S
    assert shapes.get_shape("Z") == shapes.Z
    assert shapes.get_shape("T") == shapes.T
    assert shapes.get_shape("I") == shapes.I
    assert shapes.get_shape("L") == shapes.L
    assert shapes.get_shape("J") == shapes.J
    try:
        shapes.get_shape("A")
        assert False
    except ValueError:
        assert True