import pytest
from vapory.helpers import vectorize, format_if_necessary

def test_vectorize():
    assert vectorize([1, 2, 3]) == '<1,2,3>'
    assert vectorize((4, 5)) == '<4,5>'
    assert vectorize([1.5, -2.3]) == '<1.5,-2.3>'

def test_format_if_necessary():
    # Negative numbers get wrapped
    assert format_if_necessary(-3) == '( -3 )'
    assert format_if_necessary(-0.5) == '( -0.5 )'
    # Positive numbers unchanged
    assert format_if_necessary(5) == 5
    assert format_if_necessary(0) == 0
    # Lists/tuples become vectors
    assert format_if_necessary([1, 2]) == '<1,2>'
    assert format_if_necessary((3, 4, 5)) == '<3,4,5>'
    # Strings unchanged
    assert format_if_necessary("hello") == "hello"
    # Nested structures: only top level is vectorized
    assert format_if_necessary([1, -2, [3, 4]]) == '<1,-2,[3, 4]>'