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

context: Context = {"max_assignments": max_assignments}


while remaining_tasks:
    available_robots = manage_robot_tasks(
        [assignments[-1]] if assignments else [],
        {},
        context=context,
    )

    if available_robots:
        assignments.append(available_robots[0])
        remaining_tasks -= 1
    elif context["max_assignments"]:  # Robots can still take tasks
        assignments.append(None)
    else:
        break


print("=======")
print(f"Assignments: {assignments}")
print("-----")
print(f"Remaining Tasks: {remaining_tasks}")
print("-----")
print(f"Final Context: {context}")
print("=======")
