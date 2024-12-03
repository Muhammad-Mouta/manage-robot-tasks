# pylint: skip-file

import pytest
from manage_robot_tasks import (
    manage_robot_tasks,
)


def assert_result(
    assignments: list,
    max_assignments: dict,
    *,
    expected_result: list[int],
    cooldown=3,
):
    result = manage_robot_tasks(
        assignments,
        max_assignments,
        cooldown,
    )
    assert result == expected_result


def assert_result_in(
    assignments: list,
    max_assignments: dict,
    *,
    expected_results: list[list[int]],
    cooldown=3,
):
    result = manage_robot_tasks(
        assignments,
        max_assignments,
        cooldown,
    )
    assert any([result == expected for expected in expected_results])


def test_example():
    """Covers the example provided in the problem description"""
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
        expected_result=[],
    )


def test_base_case():
    """No robots on the team, so no robots can take on tasks."""
    assert_result([], {}, expected_result=[])


class TestAssignmentsCases:
    @staticmethod
    def test_empty_assignments_with_non_empty_max_assignments():
        """No robot has been assigned a task yet and all can take at least one task except 404, so, all are available except 404. Result is returned in any order."""
        assert_result_in(
            [],
            {101: 2, 202: 2, 303: 3, 404: 0},
            expected_results=[
                [101, 202, 303],
                [101, 303, 202],
                [202, 101, 303],
                [202, 303, 101],
                [303, 101, 202],
                [303, 202, 101],
            ],
        )

    @staticmethod
    def test_invalid_entries_graceful_handling():
        """In spite of the presence of non-positive-integer values in assignments, no errors are raised and the result is returned normally."""
        assert_result(
            [101, "_", 202, 101.101, "101"],
            {101: 2},
            cooldown=1,
            expected_result=[101],
        )

    @staticmethod
    def test_invalid_entries_getting_counted_as_assignments_1():
        """Even though “_” is an invalid entry, 101 is no longer on cooldown."""
        assert_result([101, "_"], {101: 2}, cooldown=1, expected_result=[101])

    @staticmethod
    def test_invalid_entries_getting_counted_as_assignments_2():
        """Even though “_” is an invalid entry, 101 is still on cooldown because cooldown = 2."""
        assert_result([101, "_"], {101: 2}, cooldown=2, expected_result=[])

    @staticmethod
    def test_invalid_entries_getting_counted_as_assignments_3():
        """Even though “_” is an invalid entry, the second assignment for 202 is invalid because it can have at most 1 assignment, however, it still counts."""
        assert_result(
            [101, 202, 202],
            {101: 2, 202: 1},
            cooldown=2,
            expected_result=[101],
        )

    @staticmethod
    @pytest.mark.parametrize(
        "assignments", [list(range(100)), list(range(123))]
    )
    def test_raising_and_error_for_a_100_or_more_unique_robot_ids(assignments):
        """No more than a 100 unique robot IDs can exist in assignments."""
        with pytest.raises(ValueError) as err:
            manage_robot_tasks(
                assignments,
                {},
            )
        assert (
            str(err.value)
            == "You cannot have more than a 100 unique robots assigned in the (assignments) list"
        )


class TestMaxAssignmentsCases:
    @staticmethod
    @pytest.mark.parametrize(
        "assignments",
        [[101, 202, 303], list(range(99))],
    )
    def test_empty_max_assignments(assignments):
        """No matter what the input for assignments is, all robot IDs within assignments are invalid and this is handled gracefully to return an empty list."""
        assert_result(assignments, {}, expected_result=[])

    @staticmethod
    def test_ignoring_invalid_max_assignments_keys():
        """In spite of the presence of invalid robot IDs as keys in max_assignments, they are ignored and the result is returned successfully."""
        assert_result(
            [101],
            {101: 5, "101": 0, "_": 5, 202: 5, 101.101: 5},
            cooldown=0,
            expected_result=[101, 202],
        )

    @staticmethod
    @pytest.mark.parametrize(
        "max_assignments",
        [
            {101: 0, 202: 2},
            {101: -1, 202: 2},
            {101: 1.5, 202: 2},
            {101: "1", 202: 2},
        ],
    )
    def test_a_robot_with_a_zero_or_non_positive_integer_max_assignments_value(
        max_assignments,
    ):
        """Robot 101 has never been assigned but is still not available because it has a zero or non-positive-integer max_assignments  value, so it is considered unavailable."""
        assert_result([], max_assignments, expected_result=[202])

    @staticmethod
    def test_deeming_robots_that_exceed_their_max_assignments_values_unavailable():
        """
        - 202 is not available because it was assigned 3 times and its `max_assignment` limit is 3.
        - 303 is not available because it was assigned twice, whereas its `max_assignment` limit is 2.
        """
        assert_result(
            [101, 101, 202, 202, 202, 303, 303],
            {101: 3, 202: 3, 303: 1},
            cooldown=0,
            expected_result=[101],
        )

    @staticmethod
    def test_extra_max_assignments_robot_ids_1():
        """Valid Robot IDs that exist in max_assignments but not in assignments are appended to the result list in any order."""
        assert_result_in(
            [101, 303, 202, 101, 505, 404, 303],
            {101: 3, 202: 3, 303: 3, 404: 1, 505: 1, 606: 1, 707: 3, 808: 3},
            cooldown=2,
            expected_results=[
                [101, 202, 606, 707, 808],
                [101, 202, 606, 808, 707],
                [101, 202, 707, 606, 808],
                [101, 202, 707, 808, 606],
                [101, 202, 808, 606, 707],
                [101, 202, 808, 707, 606],
            ],
        )

    @staticmethod
    def test_extra_max_assignments_robot_ids_2():
        """cooldown is 1000, so every robot that has been assigned before is on cooldown. However, since 99 unique robot IDs (0~99) exist in assignments, extra robot IDs in max_assignments are ignored."""
        assert_result(
            list(range(99)),
            {rid: 5 for rid in range(123)},
            cooldown=1000,
            expected_result=[],
        )


class TestCooldownCases:
    def test_empty_or_non_positive_integer_cooldown_1(cooldown):
        """We fall back to the cooldown default value of 3, which means 202, 303, and 404 are on cooldown."""
        assert_result(
            [101, 202, 303, 404],
            {101: 2, 202: 2, 303: 2, 404: 2},
            expected_result=[101],
        )

    @staticmethod
    @pytest.mark.parametrize("cooldown", [None, -5, "5", 1.01])
    def test_empty_or_non_positive_integer_cooldown_2(cooldown):
        """We fall back to the cooldown default value of 3, which means 202, 303, and 404 are on cooldown."""
        assert_result(
            [101, 202, 303, 404],
            {101: 2, 202: 2, 303: 2, 404: 2},
            cooldown=cooldown,
            expected_result=[101],
        )

    @staticmethod
    @pytest.mark.parametrize(
        "cooldown, expected_result",
        [
            (0, [101, 202, 303, 404]),
            (1, [101, 202, 303]),
            (2, [101, 202]),
            (3, [101]),
            (4, []),
            (5, []),
        ],
    )
    def test_valid_cooldown(cooldown, expected_result):
        """When valid cooldown values are specified, robots are restricted by them"""
        assert_result(
            [101, 202, 303, 404],
            {101: 2, 202: 2, 303: 2, 404: 2},
            cooldown=cooldown,
            expected_result=expected_result,
        )
