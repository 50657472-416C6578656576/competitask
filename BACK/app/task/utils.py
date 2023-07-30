from app.task.schemas import TaskSchemaResponse


def tree_from_list(tasks: dict[str, list[TaskSchemaResponse]], parent_id: str | None = None):
    cur_tasks = tasks[parent_id]
    ret_tasks = []
    for task in cur_tasks:
        task.subtasks = tree_from_list(tasks, task.task_id)
        ret_tasks.append(task)
    return ret_tasks
