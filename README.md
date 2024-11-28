# manage-robot-tasks

## Problem Overview
In a futuristic factory, a team of robots is responsible for various tasks, but each robot has specific limitations based on its previous assignments. You must develop a function to manage these limitations while considering that tasks can arrive dynamically.

## Objective
Develop a function named manage_robot_tasks(assignments, max_assignments) where:
- assignments: A dynamic list of robot IDs representing tasks assigned over time.
- max_assignments: A dictionary defining maximum allowable assignments per robot, which may vary based on task type.
- cooldown: An integer representing the number of subsequent tasks a robot cannot be assigned after taking on a new task (default is 3).

## Requirements:
- If a robot is assigned to a task, it cannot take on a similar task for the next three assignments.
- The function should return a filtered list of robots that still can take on tasks, maintaining the order of their original assignments and accounting for dynamic changes in the input.
- The solution must gracefully handle invalid robot IDs and duplicate assignments.

## Example:
### For input:
assignments = [101, 202, 303, 202, 404, 101, 202]
max_assignments = {101: 2, 202: 1, 303: 1, 404: 1}
### The expected output should be:
[303, 404]

## Constraints:
- Each project team should have fewer than 100 robots assigned.
- The solution must work efficiently even with high volumes of data, ensuring scalability for large robot teams.
