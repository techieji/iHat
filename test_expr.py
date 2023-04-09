from expr import Expr
import pytest

@pytest.mark.parametrize("tree, namespace, expected", [
    (['+', 1, 1], {}, 2),
    ('a', {'a': 1}, 1),
    (['+', 'a', 'b'], {'a': 2, 'b': 5}, 7),
    (['+', 1, 2, 3], {}, 6),
    (['-', 1, 2, 3], {}, -4),
    (['*', 1, 2, 3], {}, 6),
    (['/', 1, 2, 3], {}, 1/6),
    (['^', 2, 5], {}, 32),
    (['@', 4], {}, 2),
    (['+', 1, ['*', 2, 3]], {}, 7)
], ids = 'simple var varadd add sub mul div pow root nested'.split())
def test_evaluate(tree, namespace, expected):
    assert Expr._quick_construct(tree).evaluate(namespace) == expected

@pytest.mark.parametrize("tree, expected", [
    (1, 1),
    ('a', 'a'),
    (['+', 1, 1], 2),
    (['-', 1, 1], 0),
    (['*', 2, 1], 2),
    (['/', 1, 2], 0.5),
    (['^', 2, 5], 32),
    (['@', 4], 2),
    (['+', 1, 'a', 1], ['+', 'a', 2]),
    (['+', 'a', 1, 1], ['+', 'a', 2]),
    (['-', 1, 'a', 2], ['-', -1, 'a']),
    (['-', 'a', 1, 2], ['-', 'a', 3]),
    (['*', 2, 'a', 3], ['*', 'a', 6]),
    (['*', 'a', 2, 3], ['*', 'a', 6]),
    (['/', 6, 'a', 2], ['/', 3, 'a']),
    (['/', 'a', 2, 6], ['/', 'a', 12])
], ids = 'static variable add sub mul div pow root multiadd1 multiadd2 multisub1 multisub2 multimul1 \
          multimul2 multidiv1 multidiv2'.split())
def test_simplify(tree, expected):
    assert Expr._quick_construct(tree).simplify() == Expr._quick_construct(expected)
