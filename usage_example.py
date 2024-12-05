"""Usage example for manage_robot_tasks"""

from manage_robot_tasks import Context, manage_robot_tasks


remaining_tasks: int = 30

max_assignments: dict[int, int] = {
    101: 1,
    202: 2,
    303: 3,
    404: 4,
    505: 5,
}

assignments: list[int | None] = []

context: Context = {}


while remaining_tasks:
    available_robots = manage_robot_tasks(
        [assignments[-1]] if assignments else [],
        max_assignments,
        context=context,
    )

    # If any robot is available, assign the task to it, else make a blank assignment
    if available_robots:
        assignments.append(available_robots[0])
        remaining_tasks -= 1
    else:
        assignments.append(None)
        # Break if there are (cooldown + 1) blank assignments, as robots can no longer take tasks.
        if len(assignments) > 5 and all(
            assignment is None for assignment in assignments[-6:]
        ):
            break

print(
    f"Assignments: {assignments if not remaining_tasks else assignments[:-6]}"
)
print(f"Number of remaining tasks: {remaining_tasks}")
