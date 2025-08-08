import pytest
import source.shapes as shapes


# a central location for sharing configurations, fixtures, and hooks across multiple test modules within a project
@pytest.fixture
def my_rectangle():
    return shapes.Rectangles(10, 20)


@pytest.fixture
def weird_rectangle():
    return shapes.Rectangles(5, 6)
