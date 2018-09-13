"""
This code provide responses in a dict format
for client requests about tasks in different
lists
"""
from tasker.libs.managers import user_manager, public_task_manager


class PublicTask:

    def __init__(self, api):
        self.api = api

    def get_public_tasks(self, list_id):
        """
        Returns a short info about tasks in list
         with id list_id in the format
        {id_1: {'name':name_1}, id_2: {'name':name_2}, ...}
        """
        username = user_manager.get_username(self.api)
        tasks = public_task_manager.get_list_tasks(username, list_id)
        response_tasks = {}
        if not tasks.exists():
            return {'error': 'user have no tasks in list'}
        for task in tasks:
            response_tasks[task.id] = {'name': task.task.name}
        return response_tasks

    def post_public_tasks(self, list_id, task_name):
        """
        Creates a new task with a name task_name
        in the list with id list_id and
        returns an info about task in the format
        {id: {'name':name}}
        """
        username = user_manager.get_username(self.api)
        public_task = public_task_manager.create_public_task(username, list_id, task_name)
        return {public_task.id: {'name': public_task.task.name}}

    def delete_public_task(self, list_id, task_id):
        """
        Deletes the task from the list with the id task_id
        and returns empty dict
        """
        username = user_manager.get_username(self.api)
        task = public_task_manager.get_list_task(username, list_id, task_id)
        if task is None:
            return {'error': 'this task was not found'}
        public_task_manager.delete_public_task(username, list_id, task_id)
        return {}

    def get_public_task(self, list_id, task_id):
        """
        Returns a full info in dict about task such as
        id, name, status, deadline, comments, subtasks
        and executors
        """
        username = user_manager.get_username(self.api)
        task = public_task_manager.get_list_task(username, list_id, task_id)
        if task is None:
            return {'error': 'this task was not found'}
        response_task = {task.id: {'name': task.task.name, 'status': task.task.status, 'deadline': task.task.deadline,
                                   'comments': {}, 'subtasks': {}, 'executors': []}}
        for comment in task.task.comments.all():
            response_task[task.id]['comments'].update({comment.id: comment.comment})
        for subtask in task.task.subtasks.all():
            response_task[task.id]['subtasks'].update({subtask.id: {'name': subtask.name, 'status': subtask.status}})
        for executor in task.executors.all():
            response_task[task.id]['executors'].append(executor.username)
        return response_task

    def post_public_task_params(self, list_id, task_id, comment, subtask, executor):
        """
        Creates a new repeat, subtask, comment or add
        an existing executor for task with task_id and
        returns full info about the modified task
        """
        username = user_manager.get_username(self.api)
        task = public_task_manager.get_list_task(username, list_id, task_id)
        if task is None:
            return {'error': 'this task was not found'}
        if comment is not None:
            public_task_manager.add_public_task_comment(username, list_id, task_id, comment)
        if subtask is not None:
            public_task_manager.add_public_task_subtask(username, list_id, task_id, subtask)
        if executor is not None:
            public_task_manager.add_task_executor(username, executor, list_id, task_id)
        return self.get_public_task(list_id, task_id)

    def put_public_task(self, list_id, task_id, name, status, deadline, subtask_id, subtask_status):
        """
        Updates task name, status, deadline and subtask status
        and returns a full modified data about the task
        """
        username = user_manager.get_username(self.api)
        task = public_task_manager.get_list_task(username, list_id, task_id)
        if task is None:
            return {'error': 'this task was not found'}
        if name is not None:
            public_task_manager.change_public_task_name(username, list_id, task_id, name)
        if status is not None:
            public_task_manager.change_public_task_status(username, list_id, task_id, status)
        if deadline is not None:
            public_task_manager.change_public_task_deadline(username, list_id, task_id, deadline)
        if subtask_id is not None:
            public_task_manager.change_public_task_subtask_status(username, list_id, task_id, subtask_id,
                                                                  subtask_status)
        return self.get_public_task(list_id, task_id)

    def delete_public_task_params(self, list_id, task_id, comment_id, subtask_id, executor):
        """
        Deletes comment, subtask or executor from the task
        and returns a full modified info about the task
        """
        username = user_manager.get_username(self.api)
        task = public_task_manager.get_list_task(username, list_id, task_id)
        if task is None:
            return {'error': 'this task was not found'}
        if comment_id is not None:
            public_task_manager.delete_public_task_comment(username, list_id, task_id, comment_id)
        if subtask_id is not None:
            public_task_manager.delete_public_task_subtask(username, list_id, task_id, subtask_id)
        if executor is not None:
            public_task_manager.delete_task_executor(username, executor, list_id, task_id)
        return self.get_public_task(list_id, task_id)