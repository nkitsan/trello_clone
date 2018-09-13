"""
This code provide responses in a dict format
for client requests about habits
"""
from tasker.libs.managers import user_manager, habit_tracker_manager


class Habit:

    def __init__(self, api):
        self.api = api

    def get_habits(self):
        """
        Returns short info about habits in the format
        {id_1: {'name':name_1}, id_2: {'name':name_2}, ...}
        """
        username = user_manager.get_username(self.api)
        habits = habit_tracker_manager.get_user_habits(username)
        response_habits = {}
        if not habits.exists():
            return {'error': 'user have no habits'}
        for habit in habits:
            response_habits[habit.id] = {'name': habit.name}
        return response_habits

    def post_habit(self, habit_name):
        """
        Creates a new habit with name in parameter habit_name
        and returns an info about it in format
        {id: {'name': name}}
        """
        username = user_manager.get_username(self.api)
        habit = habit_tracker_manager.create_habit(username, habit_name)
        return {habit.id: {'name': habit.name}}

    def delete_habit(self, habit_id):
        """
        Deletes the habit with id habit_id
        and returns empty dict
        """
        username = user_manager.get_username(self.api)
        habit = habit_tracker_manager.find_user_habit(username, habit_id)
        if habit is None:
            return {'error': 'user does not have this habit'}
        habit_tracker_manager.delete_habit(username, habit_id)
        return {}

    def get_habit(self, habit_id):
        """
        Returns a full info about the habit such as
        habit name, timeline, status
        and count(how many times user finished habit)
        """
        username = user_manager.get_username(self.api)
        habit = habit_tracker_manager.find_user_habit(username, habit_id)
        if habit is None:
            return {'error': 'user does not have this habit'}
        return {
            habit.id: {'name': habit.name, 'status': habit.status, 'timeline': habit.timeline, 'count': habit.count}}

    def put_habit(self, habit_id, habit_name, status, timeline):
        """
        Updates habit parameters such as name, status and timeline
        and returns a modified info in a full format
        """
        username = user_manager.get_username(self.api)
        habit = habit_tracker_manager.find_user_habit(username, habit_id)
        if habit is None:
            return {'error': 'user does not have this habit'}
        if habit_name is not None:
            habit_tracker_manager.change_habit_name(username, habit_id, habit_name)
        if status is not None:
            habit_tracker_manager.change_habit_status(username, habit_id, status)
        if timeline is not None:
            habit_tracker_manager.change_habit_timeline(username, habit_id, timeline)
        return self.get_habit(habit_id)
