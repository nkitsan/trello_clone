"""
This library provide JSON responses from client requests for habit
"""
from tasker.libs.managers import user_manager, habit_tracker_manager


def get_habits(api):
    username = user_manager.get_username(api)
    habits = habit_tracker_manager.get_user_habits(username)
    response_habits = {}
    if not habits.exists():
        return {'error': 'user have no habits'}
    for habit in habits:
        response_habits[habit.id] = {'name': habit.name}
    return response_habits


def post_habit(api, habit_name):
    username = user_manager.get_username(api)
    habit = habit_tracker_manager.create_habit(username, habit_name)
    return {habit.id: {'name': habit.name}}