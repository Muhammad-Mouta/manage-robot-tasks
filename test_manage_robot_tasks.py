# pylint: skip-file

"""Contains tests for the manage_robot_tasks functions"""

from itertools import permutations
import pytest
from manage_robot_tasks import (
    manage_robot_tasks,
)

MAX_UNIQUE_ROBOT_ID_MESSAGE = (
    "The (assignments) list must have less than a 100 unique robot IDs"
)


class TestBasicCases:
    @staticmethod
    def test_example():
        """Covers the example provided in the problem description"""
        assert (
            manage_robot_tasks(
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
            )
            == []
        )

    @staticmethod
    def test_base_case():
        """No robots on the team, so no robots can take on tasks."""
        assert manage_robot_tasks([], {}) == []


class TestAssignmentsCases:
    @staticmethod
    def test_empty_assignments_with_non_empty_max_assignments():
        """No robot has been assigned a task yet and all can take at least one task except 404, so, all are available except 404. Result is returned in any order."""
        assert manage_robot_tasks([], {101: 2, 202: 2, 303: 3, 404: 0}) in [
            list(perm) for perm in permutations([101, 202, 303])
        ]

    @staticmethod
    def test_invalid_entries_graceful_handling():
        """In spite of the presence of non-positive-integer values in assignments, no errors are raised and the result is returned normally."""
        assert manage_robot_tasks(
            [101, "_", 202, 101.101, "101"],
            {101: 2},
            cooldown=1,
        ) == [101]

    @staticmethod
    @pytest.mark.parametrize(
        "invalid_entry, cooldown, expected_result",
        [
            ("_", 1, [101]),
            (202, 1, [101]),
            (1.00, 1, [101]),
            ("_", 2, [101]),
            ("_", 3, []),
        ],
    )
    def test_invalid_entries_getting_counted_as_assignments(
        invalid_entry, cooldown, expected_result
    ):
        """In spite of the presence of an invalid entry, it is counted as an assignment and affects the cooldown calculation."""
        assert (
            manage_robot_tasks(
                [101, 202, invalid_entry], {101: 2, 202: 1}, cooldown=cooldown
            )
            == expected_result
        )

    @staticmethod
    @pytest.mark.parametrize(
        "assignments", [list(range(100)), list(range(123))]
    )
    def test_raising_an_error_for_a_100_or_more_unique_robot_ids(assignments):
        """No more than a 100 unique robot IDs can exist in assignments."""
        with pytest.raises(ValueError) as err:
            manage_robot_tasks(
                assignments,
                {},
            )
        assert str(err.value) == MAX_UNIQUE_ROBOT_ID_MESSAGE


class TestMaxAssignmentsCases:
    @staticmethod
    @pytest.mark.parametrize(
        "assignments",
        [[101, 202, 303], list(range(99))],
    )
    def test_empty_max_assignments(assignments):
        """No matter what the input for assignments is, all robot IDs within assignments are invalid and this is handled gracefully to return an empty list."""
        assert manage_robot_tasks(assignments, {}) == []

    @staticmethod
    def test_ignoring_invalid_max_assignments_keys():
        """In spite of the presence of invalid robot IDs as keys in max_assignments, they are ignored and the result is returned successfully."""
        assert manage_robot_tasks(
            [101], {101: 5, "101": 0, "_": 5, 202: 5, 101.101: 5}, cooldown=0
        ) == [101, 202]

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
        assert manage_robot_tasks([], max_assignments) == [202]

    @staticmethod
    def test_deeming_robots_that_exceed_their_max_assignments_values_unavailable():
        """
        - 202 is not available because it was assigned 3 times and its `max_assignment` limit is 3.
        - 303 is not available because it was assigned twice, whereas its `max_assignment` limit is 2.
        """
        assert manage_robot_tasks(
            [101, 101, 202, 202, 202, 303, 303],
            {101: 3, 202: 3, 303: 1},
            cooldown=0,
        ) == [101]

    @staticmethod
    def test_extra_max_assignments_robot_ids_1():
        """Valid Robot IDs that exist in max_assignments but not in assignments are appended to the result list in any order."""
        assert manage_robot_tasks(
            [101, 303, 202, 101, 505, 404, 303],
            {101: 3, 202: 3, 303: 3, 404: 1, 505: 1, 606: 1, 707: 3, 808: 3},
            cooldown=2,
        ) in [
            [101, 202] + list(perm) for perm in permutations([606, 707, 808])
        ]

    @staticmethod
    def test_extra_max_assignments_robot_ids_2():
        """cooldown is 1000, so every robot that has been assigned before is on cooldown. However, since 99 unique robot IDs (0~99) exist in assignments, extra robot IDs in max_assignments are ignored."""
        assert (
            manage_robot_tasks(
                list(range(99)), {rid: 5 for rid in range(123)}, cooldown=1000
            )
            == []
        )

    @staticmethod
    def test_extra_max_assignments_robot_ids_3():
        """cooldown is 1000, so every robot that has been assigned before is on cooldown. However, since 99 unique robot IDs (0~99) exist in assignments, extra robot IDs in max_assignments are ignored."""
        assert manage_robot_tasks(
            list(range(98)), {rid: 5 for rid in range(101)}, cooldown=1000
        ) in [list(perm) for perm in permutations(range(98, 101))]


class TestCooldownCases:
    def test_empty_or_non_positive_integer_cooldown_1(cooldown):
        """We fall back to the cooldown default value of 3, which means 202, 303, and 404 are on cooldown."""
        assert manage_robot_tasks(
            [101, 202, 303, 404], {101: 2, 202: 2, 303: 2, 404: 2}
        ) == [101]

    @staticmethod
    @pytest.mark.parametrize("cooldown", [None, -5, "5", 1.01])
    def test_empty_or_non_positive_integer_cooldown_2(cooldown):
        """We fall back to the cooldown default value of 3, which means 202, 303, and 404 are on cooldown."""
        assert manage_robot_tasks(
            [101, 202, 303, 404],
            {101: 2, 202: 2, 303: 2, 404: 2},
            cooldown=cooldown,
        ) == [101]

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
        assert (
            manage_robot_tasks(
                [101, 202, 303, 404],
                {101: 2, 202: 2, 303: 2, 404: 2},
                cooldown=cooldown,
            )
            == expected_result
        )


# TODO: Update the returned context to contain the (max_assignments)
class TestContextCases:
    @staticmethod
    def test_not_passing_a_context():
        """No context passed, so the function works normally"""
        assert manage_robot_tasks(
            [101, 202, 303, 404, 505],
            {101: 2, 202: 1, 303: 2, 404: 2},
        ) == [101]

    @staticmethod
    def test_passing_none_as_context():
        """Context is None, which has no effect on the function result nor the context passed"""
        context = None
        assert manage_robot_tasks(
            [101, 202, 303, 404, 505],
            {101: 2, 202: 1, 303: 2, 404: 2},
            context=context,
        ) == [101]
        assert context is None

    @staticmethod
    def test_passing_empty_context():
        """An empty context dict is passed, so, there is no effect on the function result. However, the passed context is updated."""
        context = {}
        manage_robot_tasks(
            [101, 202, 303, 404, 505, 202],
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert context == {
            "max_assignments": {101: 2, 404: 2, 505: 2},
            "robot_records": {
                101: (1, 0, 0),
                202: (2, 1, 5),
                303: (1, 2, 2),
                404: (1, 3, 3),
                505: (1, 4, 4),
            },
            "total_assignment_count": 6,
        }

    @staticmethod
    def test_passing_context_max_assignments_only():
        """No previous assignments are assumed, so, the context max_assignments is used and robots that exceeded their limit are dropped in the updated context max_assignments"""
        context = {
            "max_assignments": {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
        }
        assert manage_robot_tasks(
            [101, 202, 303, 404, 505, 202],
            {},
            context=context,
        ) == [101]
        assert context == {
            "max_assignments": {101: 2, 404: 2, 505: 2},
            "robot_records": {
                101: (1, 0, 0),
                202: (2, 1, 5),
                303: (1, 2, 2),
                404: (1, 3, 3),
                505: (1, 4, 4),
            },
            "total_assignment_count": 6,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "assignments, expected_context",
        [
            (
                [],
                {
                    "max_assignments": {
                        101: 2,
                        404: 2,
                        505: 2,
                    },
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (1, 3, 3),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 6,
                },
            ),
            (
                ["_", 404],
                {
                    "max_assignments": {
                        101: 2,
                        505: 2,
                    },
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (2, 3, 7),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 8,
                },
            ),
        ],
    )
    def test_passing_robot_records_only(assignments, expected_context):
        """Since total_assignment_count is missing, it is calculated as the sum of robot assignment counts + len(assignments)."""
        context = {
            "robot_records": {
                101: (1, 0, 0),
                202: (2, 1, 5),
                303: (1, 2, 2),
                404: (1, 3, 3),
                505: (1, 4, 4),
            }
        }
        manage_robot_tasks(
            assignments,
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert context == expected_context

    @staticmethod
    @pytest.mark.parametrize(
        "assignments, expected_context",
        [
            (
                [],
                {
                    "max_assignments": {
                        101: 2,
                        202: 2,
                        303: 1,
                        404: 2,
                        505: 2,
                    },
                    "robot_records": {},
                    "total_assignment_count": 6,
                },
            ),
            (
                ["_", 404],
                {
                    "max_assignments": {
                        101: 2,
                        202: 2,
                        303: 1,
                        404: 2,
                        505: 2,
                    },
                    "robot_records": {
                        404: (1, 7, 7),
                    },
                    "total_assignment_count": 8,
                },
            ),
        ],
    )
    def test_passing_total_assignment_count_only(
        assignments, expected_context
    ):
        """Since robot_records are missing, it is assumed that all assignments are invalid so far and that robot_records is an empty dict."""
        context = {
            "total_assignment_count": 6,
        }
        manage_robot_tasks(
            assignments,
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert context == expected_context

    @staticmethod
    @pytest.mark.parametrize(
        "assignments, expected_context",
        [
            (
                [],
                {
                    "max_assignments": {
                        101: 2,
                        404: 2,
                        505: 2,
                    },
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (1, 3, 3),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 6,
                },
            ),
            (
                ["_", 404],
                {
                    "max_assignments": {
                        101: 2,
                        505: 2,
                    },
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (2, 3, 7),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 8,
                },
            ),
        ],
    )
    def test_passing_complete_context(assignments, expected_context):
        context = {
            "max_assignments": {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            "robot_records": {
                101: (1, 0, 0),
                202: (2, 1, 5),
                303: (1, 2, 2),
                404: (1, 3, 3),
                505: (1, 4, 4),
            },
            "total_assignment_count": 6,
        }
        manage_robot_tasks(
            assignments,
            {},
            context=context,
        )
        assert context == expected_context

    @staticmethod
    @pytest.mark.parametrize(
        "assignments, expected_context",
        [
            (
                [],
                {
                    "max_assignments": {101: 2, 404: 2, 505: 2},
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (1, 3, 3),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 6,
                },
            ),
            (
                ["_", 404],
                {
                    "max_assignments": {101: 2, 505: 2},
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (2, 3, 7),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 8,
                },
            ),
        ],
    )
    def test_passing_total_assignment_count_less_than_the_sum_of_robot_assignment_counts(
        assignments, expected_context
    ):
        """In this case, the total_assignment_count is pumped up to match the sum of robot_assignment_counts. This ensures consistency along the robot_records."""
        context = {
            "robot_records": {
                101: (1, 0, 0),
                202: (2, 1, 5),
                303: (1, 2, 2),
                404: (1, 3, 3),
                505: (1, 4, 4),
            },
            "total_assignment_count": 3,
        }
        manage_robot_tasks(
            assignments,
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert context == expected_context

    @staticmethod
    @pytest.mark.parametrize(
        "assignments, expected_context",
        [
            (
                [],
                {
                    "max_assignments": {101: 2, 404: 2, 505: 2},
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (1, 3, 3),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 9,
                },
            ),
            (
                ["_", 404],
                {
                    "max_assignments": {101: 2, 505: 2},
                    "robot_records": {
                        101: (1, 0, 0),
                        202: (2, 1, 5),
                        303: (1, 2, 2),
                        404: (2, 3, 10),
                        505: (1, 4, 4),
                    },
                    "total_assignment_count": 11,
                },
            ),
        ],
    )
    def test_passing_total_assignment_count_more_than_the_sum_of_robot_assignment_counts(
        assignments, expected_context
    ):
        """In this case, the total_assignment_count is treated normally."""
        context = {
            "robot_records": {
                101: (1, 0, 0),
                202: (2, 1, 5),
                303: (1, 2, 2),
                404: (1, 3, 3),
                505: (1, 4, 4),
            },
            "total_assignment_count": 9,
        }
        manage_robot_tasks(
            assignments,
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert context == expected_context

    @staticmethod
    @pytest.mark.parametrize(
        "robot_records",
        [
            {rid: (1, rid, rid) for rid in range(100)},
            {rid: (1, rid, rid) for rid in range(123)},
        ],
    )
    def test_raising_an_error_if_robot_records_exceed_100_items(robot_records):
        context = {
            "robot_records": robot_records,
        }
        with pytest.raises(ValueError) as err:
            manage_robot_tasks([], {}, context=context)
        assert str(err.value) == MAX_UNIQUE_ROBOT_ID_MESSAGE
        assert context == {
            "robot_records": robot_records,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "robot_records, assignments",
        [
            ({rid: (1, rid, rid) for rid in range(99)}, [99]),
            ({rid: (1, rid, rid) for rid in range(99)}, [99, 100, 101]),
            ({rid: (1, rid, rid) for rid in range(97)}, [99, 100, 101]),
        ],
    )
    def test_passing_assignments_that_would_exceed_the_100_unique_robot_ids(
        robot_records, assignments
    ):
        context = {
            "robot_records": robot_records,
        }
        with pytest.raises(ValueError) as err:
            manage_robot_tasks(
                assignments,
                {rid: 5 for rid in range(123)},
                context=context,
            )
        assert str(err.value) == MAX_UNIQUE_ROBOT_ID_MESSAGE
        assert context == {
            "robot_records": robot_records,
        }

    @staticmethod
    @pytest.mark.parametrize(
        "robot_records, assignments",
        [
            ({rid: (1, rid, rid) for rid in range(99)}, [55, 77]),
            ({rid: (1, rid, rid) for rid in range(97)}, [99, 100]),
        ],
    )
    def test_passing_assignments_that_would_not_exceed_the_100_unique_robot_ids(
        robot_records, assignments
    ):
        context = {
            "robot_records": robot_records,
        }
        manage_robot_tasks(
            assignments,
            {rid: 5 for rid in range(123)},
            context=context,
        )

    @staticmethod
    @pytest.mark.parametrize(
        "cooldown, expected_result", [(4, [101]), (5, []), (6, [])]
    )
    def test_increasing_cooldown_given_context(cooldown, expected_result):
        context = {}
        manage_robot_tasks(
            [101, 202, 303, 404, 505],
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert (
            manage_robot_tasks(
                [],
                {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
                context=context,
                cooldown=cooldown,
            )
            == expected_result
        )

    @staticmethod
    @pytest.mark.parametrize(
        "cooldown, expected_result",
        [(2, [101, 404]), (1, [101, 404, 505]), (0, [101, 404, 505])],
    )
    def test_decreasing_cooldown_given_context(cooldown, expected_result):
        context = {}
        manage_robot_tasks(
            [101, 202, 303, 404, 505, 202],
            {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
            context=context,
        )
        assert (
            manage_robot_tasks(
                [],
                {101: 2, 202: 2, 303: 1, 404: 2, 505: 2},
                context=context,
                cooldown=cooldown,
            )
            == expected_result
        )

    @staticmethod
    def test_merging_parameter_and_context_max_assignments():
        context = {"max_assignments": {101: 2, 202: 2, 404: 2}}
        assert manage_robot_tasks(
            [101, 202, 303, 505, 404, 202, 505],
            {202: 2, 303: 1, 404: 1, 505: 3, 606: 2},
            context=context,
        ) == [101, 606]
        assert "max_assignments" in context and context["max_assignments"] == {
            101: 2,
            505: 3,
            606: 2,
        }

    @staticmethod
    def test_cleaning_max_assignments():
        context = {
            "max_assignments": {
                101: 2,
                202: 2,
                404: 2,
                101.01: 3,
                "_": 4,
                1.01: 5,
                606: None,
                707: -5,
            }
        }
        assert manage_robot_tasks(
            [101, 202, 303, 505, 404, 202, 505],
            {202: 3.00, 505: 2, 101.01: 6, "_": 7, 1.01: 8, 606: 2, 707: None},
            context=context,
        ) == [101, 606]
        assert "max_assignments" in context and context["max_assignments"] == {
            101: 2,
            404: 2,
            606: 2,
        }


class TestRandomCases:
    @staticmethod
    def test_case_1():
        assert manage_robot_tasks(
            [101, 202, 303, 101, 404, 505, 505, 202, 303, 101, 707, 808, 909],
            {
                101: 5,
                202: 2,
                303: 2,
                404: 4,
                505: 1,
                606: 2,
                707: 3,
                808: 5,
                909: 1,
            },
            cooldown=3,
        ) == [101, 404, 606]

    @staticmethod
    def test_case_2():
        assert manage_robot_tasks(
            [101, 102, 303, "X", "_", 202, 404, 303, 808, 909, 505],
            {
                101: 3,
                102: 0,
                202: -1,
                303: 2,
                "404": 1,
                505: 1,
                808: 4,
                909: 2,
                606: 3,
            },
            cooldown=2,
        ) == [101, 808, 606]

    @staticmethod
    def test_case_3():
        assert manage_robot_tasks(
            [101, 202, 303, 101, 202, 303, 101, 202, 303],
            {
                101: 5,
                202: 3,
                303: 2,
                404: 4,
                505: 1,
                606: 3,
                707: 4,
            },
            cooldown=0,
        ) in [
            [101] + list(perm) for perm in permutations([404, 505, 606, 707])
        ]

    @staticmethod
    def test_case_4():
        assert manage_robot_tasks(
            [101, 101, 202, 202, 303, 303, 404, 404, 505, 505],
            {
                101: 1,
                202: 2,
                303: 2,
                404: 2,
                505: 2,
                606: 5,
            },
            cooldown=3,
        ) == [606]

    @staticmethod
    def test_case_5():
        assert manage_robot_tasks(
            [
                101,
                202,
                303,
                404,
                505,
                606,
                707,
                808,
                909,
                101,
                202,
                303,
                404,
                505,
                606,
            ],
            {
                101: 10,
                202: 5,
                303: 3,
                404: 7,
                505: 4,
                606: 8,
                707: 6,
                808: 9,
                909: 2,
            },
            cooldown=6,
        ) == [707, 808, 909]

    @staticmethod
    def test_case_6():
        assignments = [
            101,
            202,
            303,
            404,
            505,
            606,
            707,
            808,
            909,
            101,
            202,
            303,
            404,
            505,
            606,
            707,
            808,
            909,
            101,
            202,
            303,
            404,
            505,
            606,
            707,
            808,
            909,
            101,
            202,
            303,
            "INVALID",
            404,
            505,
            "_",
            606,
            707,
            808,
            909,
            "INVALID",
            "N/A",
            101,
            202,
            303,
            404,
            505,
            606,
            "X",
            707,
            808,
            909,
            101,
            202,
            303,
            404,
            None,
            505,
            606,
            707,
            808,
            909,
            101,
            "INVALID",
            303,
            404,
            505,
            606,
            707,
            808,
            "BAD_KEY",
            909,
            101,
            202,
            "INVALID",
            404,
            "?",
            606,
            707,
            "INVALID",
            808,
            909,
            101,
            202,
            303,
            404,
            505,
            606,
            "###",
            707,
            808,
            909,
        ]
        max_assignments = {
            101: 5,
            202: 3,
            303: 15,
            404: 6,
            505: 11,
            606: 7,
            707: 8,
            808: 2,
            909: 10,
            111: 3,
            112: 4,
            114: 2,
            "INVALID_KEY": 5,
            116: -1,
            117: 0,
            "": 5,
        }
        context = {}
        for i in range(0, len(assignments), 10):
            result = manage_robot_tasks(
                assignments[i : i + 10],
                max_assignments,
                cooldown=5,
                context=context,
            )
        assert result in [
            [303, 505] + list(perm) for perm in permutations([111, 112, 114])
        ]

    @staticmethod
    def test_case_7():
        assignments = []
        max_assignments = {i: i + 1 for i in range(100)}
        max_assignments[93] = max_assignments[95] = max_assignments[97] = 1000
        for i in range(99):
            assignments.extend([j for j in range(i, 99)])

        context = {"max_assignments": max_assignments}

        for i in range(0, len(assignments), 1000):
            result = manage_robot_tasks(
                assignments[i : i + 1000],
                {},
                context=context,
            )

        assert result == [93, 95]
