# pylint: skip-file

from manage_robot_tasks import (
    manage_robot_tasks,
)


def assert_result(
    assignments,
    max_assignments,
    expected,
    cooldown=3,
):
    result = manage_robot_tasks(
        assignments,
        max_assignments,
        cooldown,
    )
    assert len(result) == len(expected) and all(
        e1 == e2
        for e1, e2 in zip(
            result,
            expected,
        )
    )


def test_example():
    assert_result(
        [
            101,
            202,
            303,
            202,
            404,
            101,
            202,
        ],
        {
            101: 2,
            202: 1,
            303: 1,
            404: 1,
        },
        [303, 404],
    )
