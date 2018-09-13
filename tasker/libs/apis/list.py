"""
This code provide responses in a dict format
for client requests about lists
"""
from tasker.libs.managers import user_manager, public_task_manager


class List:

    def __init__(self, api):
        self.api = api

    def get_lists(self):
        """
        Returns a short info about lists in the format
        {id_1: {'name':name_1}, id_2: {'name':name_2}, ...}
        """
        username = user_manager.get_username(self.api)
        lists = public_task_manager.get_user_lists(username)
        response_lists = {}
        if not lists.exists():
            return {'error': 'user have no lists'}
        for public_list in lists:
            response_lists[public_list.id] = {'name': public_list.name}
        return response_lists

    def post_lists(self, list_name):
        """
        Creates a new list with a name list_name and
        returns if in the format {id: {'name':name}}
        """
        username = user_manager.get_username(self.api)
        public_list = public_task_manager.create_public_list(username, list_name)
        return {public_list.id: {'name': public_list.name}}

    def delete_list(self, list_id):
        """
        Deletes the list with the id list_id and
        returns empty dict
        """
        username = user_manager.get_username(self.api)
        lists = public_task_manager.get_user_lists(username)
        if not lists.filter(id=list_id).exists():
            return {'error': 'no such list'}
        public_task_manager.delete_public_list(username, list_id)
        return {}

    def post_list_params(self, list_id, new_user):
        """
        Adds the user access to the list and
        returns an empty dict
        """
        username = user_manager.get_username(self.api)
        user = user_manager.get_user(username)
        if user_manager.get_user(new_user) is None:
            return {'error': 'user is not exist'}
        if not user.lists.filter(id=list_id).exists():
            return {'error': 'no access to manage this list'}
        public_task_manager.add_public_list_user(username, new_user, list_id)
        return {}

    def put_list(self, list_id, list_name):
        """
        Changes a name of the list and
        returns {list_id: list_name}
        """
        username = user_manager.get_username(self.api)
        public_task_manager.change_public_list_name(username, list_id, list_name)
        return {list_id: list_name}

    def delete_list_params(self, list_id, new_user):
        """
        Deletes a user access to the list
        and returns an empty dict
        """
        username = user_manager.get_username(self.api)
        user = user_manager.get_user(username)
        if user_manager.get_user(new_user) is None:
            return {'error': 'user is not exist'}
        if not user.lists.filter(id=list_id).exists():
            return {'error': 'no access to manage this list'}
        public_task_manager.delete_public_list_user(username, new_user, list_id)
        return {}
