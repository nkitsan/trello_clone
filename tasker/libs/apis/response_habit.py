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


def delete_habit(api, habit_id):
    username = user_manager.get_username(api)
    habit = habit_tracker_manager.find_user_habit(username, habit_id)
    if habit is None:
        return {'error': 'user does not have this habit'}
    habit_tracker_manager.delete_habit(username, habit_id)
    return {}


def get_habit(api, habit_id):
    username = user_manager.get_username(api)
    habit = habit_tracker_manager.find_user_habit(username, habit_id)
    if habit is None:
        return {'error': 'user does not have this habit'}
    return {habit.id: {'name': habit.name, 'status': habit.status, 'timeline': habit.timeline}}


def put_habit(api, habit_id, habit_name, status, timeline):
    username = user_manager.get_username(api)
    habit = habit_tracker_manager.find_user_habit(username, habit_id)
    if habit is None:
        return {'error': 'user does not have this habit'}
    if habit_name is not None:
        habit_tracker_manager.change_habit_name(username, habit_id, habit_name)
    if status is not None:
        habit_tracker_manager.change_habit_status(username, habit_id, status)
    if timeline is not None:
        habit_tracker_manager.change_habit_timeline(username, habit_id, timeline)
    return get_habit(api, habit_id)
