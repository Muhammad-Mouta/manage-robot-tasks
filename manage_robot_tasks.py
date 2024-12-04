"""
    In a futuristic factory, a team of robots is responsible for various tasks, 
    but each robot has specific limitations based on its previous assignments. 
    This module manages these limitations while considering that tasks can arrive dynamically.
"""

from utils import is_positive_int


MAX_UNIQUE_ROBOT_IDS = 100

DEFAULT_COOLDOWN = 3


def manage_robot_tasks(
    assignments: list,
    max_assignments: dict,
    cooldown=DEFAULT_COOLDOWN,
) -> list[int]:
    """In a futuristic factory, a team of robots is responsible for various tasks,
       but each robot has specific limitations based on its previous assignments.
       This function manages these limitations while considering that tasks can arrive dynamically.

    Args:
        assignments (list): A dynamic list of robot IDs representing tasks assigned over time.
        max_assignments (dict):
            A dictionary defining maximum allowable assignments per robot.
        cooldown (optional):
            An integer representing the number of subsequent tasks a robot cannot be assigned
            after taking on a new task. Defaults to 3.

    Returns:
        list[int]:
            A filtered list of robots that still can take on tasks,
            maintaining the order of their original assignments.
    """
    # Ensure the number of unique robot IDs in assignments is less than 100
    no_unique_robot_ids = len(set(assignments))
    if no_unique_robot_ids >= MAX_UNIQUE_ROBOT_IDS:
        raise ValueError(
            "You cannot have more than a 100 unique robots assigned in the (assignments) list"
        )

    # Count the number of tasks each robot has taken on
    # and store the index of its first occurrence
    robot_task_counts = {}
    for i, robot_id in enumerate(assignments):
        if is_positive_int(robot_id):
            if robot_id in robot_task_counts:
                first_occ, count = robot_task_counts[robot_id]
                robot_task_counts[robot_id] = (first_occ, count + 1)
            else:
                robot_task_counts[robot_id] = (i, 1)

    # Set the cooldown value and extract the robots on cooldown
    cooldown = cooldown if is_positive_int(cooldown) else DEFAULT_COOLDOWN
    robots_on_cooldown = set()
    for i in range(1, min(len(assignments), cooldown) + 1):
        robots_on_cooldown.add(assignments[-i])

    # Iterate through max_assignments items, form the result, and extract the extra robot IDs
    result = []
    extra_robot_ids = []
    for robot_id, limit in max_assignments.items():
        if is_positive_int(robot_id) and is_positive_int(limit, nonzero=True):
            if robot_id in robot_task_counts:
                first_occ, count = robot_task_counts[robot_id]
                if count < limit and robot_id not in robots_on_cooldown:
                    result.append(robot_id)
            else:
                extra_robot_ids.append(robot_id)

    # Sort the result based on each robot ID's first occurrence in the assignments
    # Also, append the extra robot_ids to the result if no_unique_robot_ids permits it
    return sorted(result, key=lambda rid: robot_task_counts[rid][0]) + (
        extra_robot_ids
        if no_unique_robot_ids < MAX_UNIQUE_ROBOT_IDS - 1
        else []
    )
