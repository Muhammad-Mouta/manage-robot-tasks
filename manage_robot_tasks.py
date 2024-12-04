"""In a futuristic factory, a team of robots is responsible for various tasks, 
    but each robot has specific limitations based on its previous assignments. 
    This module manages these limitations while considering that tasks can arrive dynamically.
"""

from typing import NamedTuple, TypedDict
from utils import is_positive_int


MAX_UNIQUE_ROBOT_ID_COUNT = 100

DEFAULT_COOLDOWN = 3


class RobotRecord(NamedTuple):
    """Represents the status of robot assignments"""

    assignment_count: int
    first_assignment_index: int
    last_assignment_index: int


class Context(TypedDict):
    """Represents the context that can be passed to manage_robot_tasks"""

    robot_records: dict[int, RobotRecord]
    total_assignment_count: int


def manage_robot_tasks(
    assignments: list,
    max_assignments: dict,
    cooldown=DEFAULT_COOLDOWN,
    context: None | Context = None,
) -> list[int]:
    """Manages robot limitations while considering that tasks can arrive dynamically.

    Args:
        assignments (list): A dynamic list of robot IDs representing tasks assigned over time.
        max_assignments (dict):
            A dictionary defining maximum allowable assignments per robot.
        cooldown (optional):
            An integer representing the number of subsequent tasks a robot cannot be assigned
            after taking on a new task. Defaults to 3.
        context (None | Context):
            If provided, it is used in calculations and is updated in place with the new context.
            It is useful for caching the context between function calls to avoid recalculations.
            It can have the following items:
                - robot_records (dict[int, RobotRecord]):
                    A dict holding records that describe previous tasks of a robot.
                - total_assignment_count (int): The total number of assignments so far.
    Returns:
        list[int]:
            A filtered list of robots that still can take on tasks,
            maintaining the order of their original assignments.
    """

    # Ensure the number of unique robot IDs in assignments is less than 100.
    unique_robot_id_count = len(set(assignments))
    if unique_robot_id_count >= MAX_UNIQUE_ROBOT_ID_COUNT:
        raise ValueError(
            "You cannot have more than a 100 unique robots assigned in the (assignments) list"
        )

    # Iterate through (assignments) and form robot_records
    robot_records: dict[int, RobotRecord] = {}
    for i, robot_id in enumerate(assignments):
        if is_positive_int(robot_id):
            if robot_id in robot_records:
                robot_record = robot_records[robot_id]
                robot_records[robot_id] = RobotRecord(
                    robot_record.assignment_count + 1,
                    robot_record.first_assignment_index,
                    i,
                )
            else:
                robot_records[robot_id] = RobotRecord(1, i, i)

    # Iterate through (max_assignments) items, extract extra_robot_ids, and form the result
    min_cooldown_index = len(assignments) - (
        cooldown if is_positive_int(cooldown) else DEFAULT_COOLDOWN
    )
    extra_robot_ids = []
    result = []
    for robot_id, limit in max_assignments.items():
        if is_positive_int(robot_id) and is_positive_int(limit, nonzero=True):
            if robot_id in robot_records:
                robot_record = robot_records[robot_id]
                if (
                    robot_record.assignment_count < limit
                    and robot_record.last_assignment_index < min_cooldown_index
                ):
                    result.append(robot_id)
            else:
                extra_robot_ids.append(robot_id)

    # Sort (result) based on each robot ID's first occurrence in (assignments).
    # Also, extend it with (extra_robot_ids) if (unique_robot_id_count) permits it.
    result.sort(
        key=lambda robot_id: robot_records[robot_id].first_assignment_index
    )
    if unique_robot_id_count < MAX_UNIQUE_ROBOT_ID_COUNT - 1:
        result.extend(extra_robot_ids)

    return result
