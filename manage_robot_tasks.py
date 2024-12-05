"""In a futuristic factory, a team of robots is responsible for various tasks, 
    but each robot has specific limitations based on its previous assignments. 
    This module manages these limitations while considering that tasks can arrive dynamically.
"""

from typing import NamedTuple, NotRequired, TypedDict
from utils import is_positive_int


MAX_UNIQUE_ROBOT_ID_COUNT = 100

MAX_UNIQUE_ROBOT_ID_MESSAGE = f"The (assignments) list must have less than a {MAX_UNIQUE_ROBOT_ID_COUNT} unique robot IDs"  # pylint: disable=C0301

DEFAULT_COOLDOWN = 3


class RobotRecord(NamedTuple):
    """Represents the status of robot assignments"""

    assignment_count: int
    first_assignment_index: int
    last_assignment_index: int


class Context(TypedDict):
    """Represents the context that can be passed to manage_robot_tasks"""

    max_assignments: NotRequired[dict[int, int]]
    robot_records: NotRequired[dict[int, RobotRecord]]
    total_assignment_count: NotRequired[int]


def manage_robot_tasks(  # pylint: disable=R0912,R0914
    assignments: list,
    max_assignments: dict,
    cooldown=DEFAULT_COOLDOWN,
    *,
    context: None | Context = None,
) -> list[int]:
    """Manages robot limitations while considering that tasks can arrive dynamically.

    Args:
        assignments (list): A dynamic list of robot IDs representing tasks assigned over time.
        max_assignments (dict):
            A dictionary defining maximum allowable assignments per robot.
        cooldown (optional):
            An integer representing the number of subsequent tasks a robot cannot be assigned
            after taking on a new task. Defaults to DEFAULT_COOLDOWN.
        context (None | Context):
            If provided, it is used in calculations and is updated in place with the new context.
            It is useful for caching the context between function calls to avoid recalculations.
            It can have the following items:
                - max_assignments (dict[int, int]):
                    Holds the maximum number of tasks that can be assigned for each robot.
                - robot_records (dict[int, RobotRecord]):
                    Holds records that describe previous tasks of a robot.
                - total_assignment_count (int): The total number of assignments so far.
    Returns:
        list[int]:
            A filtered list of robots that still can take on tasks,
            maintaining the order of their original assignments.
    """

    # Ensure the number of unique robot IDs in
    # (context["robot_records"]) and (assignments) is less than MAX_UNIQUE_ROBOT_ID_COUNT.
    if context and "robot_records" in context:
        unique_robot_id_count = len(context["robot_records"]) + sum(
            0 if robot_id in context["robot_records"] else 1
            for robot_id in set(assignments)
        )
    else:
        unique_robot_id_count = len(set(assignments))
    if unique_robot_id_count >= MAX_UNIQUE_ROBOT_ID_COUNT:
        raise ValueError(MAX_UNIQUE_ROBOT_ID_MESSAGE)

    # Read the context if given
    if context:
        max_assignments = (
            (context["max_assignments"] | max_assignments)
            if "max_assignments" in context
            else max_assignments
        )
        robot_records = {
            robot_id: (
                robot_record
                if isinstance(robot_record, RobotRecord)
                else RobotRecord(*robot_record)
            )
            for robot_id, robot_record in (
                context["robot_records"] if "robot_records" in context else {}
            ).items()
        }
        prev_total_assignment_count = max(
            sum(
                robot_record.assignment_count
                for _, robot_record in robot_records.items()
            ),
            (
                context["total_assignment_count"]
                if "total_assignment_count" in context
                else 0
            ),
        )
    else:
        robot_records = {}
        prev_total_assignment_count = 0

    # Iterate through (assignments) and update robot_records
    for i, robot_id in enumerate(assignments):
        if is_positive_int(robot_id):
            actual_index = prev_total_assignment_count + i
            if robot_id in robot_records:
                robot_record = robot_records[robot_id]
                robot_records[robot_id] = RobotRecord(
                    robot_record.assignment_count + 1,
                    robot_record.first_assignment_index,
                    actual_index,
                )
            else:
                robot_records[robot_id] = RobotRecord(
                    1, actual_index, actual_index
                )

    # Iterate through (max_assignments) items, extract extra_robot_ids, form the result,
    # and the clean_max_assignments
    total_assignment_count = prev_total_assignment_count + len(assignments)
    min_cooldown_index = total_assignment_count - (
        cooldown if is_positive_int(cooldown) else DEFAULT_COOLDOWN
    )
    extra_robot_ids: list[int] = []
    result: list[int] = []
    clean_max_assignments: dict[int, int] = {}
    for robot_id, limit in max_assignments.items():
        if is_positive_int(robot_id) and is_positive_int(limit, nonzero=True):
            if robot_id in robot_records:
                robot_record = robot_records[robot_id]
                if robot_record.assignment_count < limit:
                    clean_max_assignments[robot_id] = limit
                    if robot_record.last_assignment_index < min_cooldown_index:
                        result.append(robot_id)
            else:
                extra_robot_ids.append(robot_id)

    # Sort (result) based on each robot first_assignment_index
    # Also, extend it with (extra_robot_ids) if (unique_robot_id_count) permits it.
    result.sort(
        key=lambda robot_id: robot_records[robot_id].first_assignment_index
    )
    if unique_robot_id_count < MAX_UNIQUE_ROBOT_ID_COUNT - 1:
        result.extend(extra_robot_ids)
        for extra_robot_id in extra_robot_ids:
            clean_max_assignments[extra_robot_id] = max_assignments[
                extra_robot_id
            ]

    # Update the context if given
    if context is not None:
        context["max_assignments"] = clean_max_assignments
        context["robot_records"] = robot_records
        context["total_assignment_count"] = total_assignment_count

    return result
