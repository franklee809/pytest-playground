import pytest
from source.school import Classroom, Teacher, Student, TooManyStudents


# -----------------------
# Fixtures
# -----------------------

@pytest.fixture
def hogwarts_teacher():
    return Teacher("Professor McGonagall")


@pytest.fixture
def hogwarts_students():
    # Starting with 3 Hogwarts students
    return [
        Student("Harry Potter"),
        Student("Hermione Granger"),
        Student("Ron Weasley")
    ]


@pytest.fixture
def transfiguration_class(hogwarts_teacher, hogwarts_students):
    return Classroom(hogwarts_teacher, hogwarts_students, "Transfiguration")


# -----------------------
# Tests
# -----------------------

@pytest.mark.parametrize("new_student_name", [
    "Neville Longbottom",
    "Luna Lovegood",
    "Draco Malfoy"
])
def test_add_student_success(transfiguration_class, new_student_name):
    """Adding a new student should increase the count."""
    start_count = len(transfiguration_class.students)
    transfiguration_class.add_student(Student(new_student_name))
    assert len(transfiguration_class.students) == start_count + 1
    assert transfiguration_class.students[-1].name == new_student_name


def test_add_student_too_many_students(transfiguration_class):
    """Adding beyond the limit should raise TooManyStudents."""
    # Fill up until the limit is reached (10 students total)
    while len(transfiguration_class.students) <= 10:
        transfiguration_class.students.append(
            Student(f"Extra Student {len(transfiguration_class.students)+1}"))

    with pytest.raises(TooManyStudents):
        transfiguration_class.add_student(Student("Cho Chang"))


@pytest.mark.parametrize("student_to_remove", [
    "Harry Potter",
    "Hermione Granger"
])
def test_remove_student(transfiguration_class, student_to_remove):
    """Removing an existing student should shrink the list."""
    start_count = len(transfiguration_class.students)
    transfiguration_class.remove_student(student_to_remove)
    assert len(transfiguration_class.students) == start_count - 1
    assert all(s.name != student_to_remove for s in transfiguration_class.students)


def test_remove_nonexistent_student_does_nothing(transfiguration_class):
    """Removing a non-existent student should not crash or change count."""
    start_count = len(transfiguration_class.students)
    transfiguration_class.remove_student("Lord Voldemort")
    assert len(transfiguration_class.students) == start_count


@pytest.mark.parametrize("new_professor", [
    "Professor Snape",
    "Professor Dumbledore"
])
def test_change_teacher(transfiguration_class, new_professor):
    """Changing the teacher should update the attribute."""
    transfiguration_class.change_teacher(Teacher(new_professor))
    assert transfiguration_class.teacher.name == new_professor


# -----------------------
# Custom markers
# -----------------------

@pytest.mark.magic
def test_hogwarts_theme(transfiguration_class):
    """Ensure the theme is properly Hogwarts-ish."""
    assert "Professor" in transfiguration_class.teacher.name
    assert any("Potter" in s.name for s in transfiguration_class.students)
