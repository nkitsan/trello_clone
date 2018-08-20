"""
Manager for adding, deleting and changing habits in the habit tracker
"""


from tasker.models import User, Habit


def create_habit(username, habit_name):
    user = User.objects.get(username=username)
    return user.habit_tracker.create(name=habit_name)


def set_habit_timeline(username, habit_id, timeline):
    habit = find_user_habit(username, habit_id)
    habit.timeline = timeline
    habit.save()


def change_habit_status(username, habit_id, status):
    habit = find_user_habit(username, habit_id)
    habit.status = status
    habit.save()


def change_habit_name(username, habit_id, new_name):
    habit = find_user_habit(username, habit_id)
    habit.name = new_name
    habit.save()


def delete_habit(username, habit_id):
    user = User.objects.get(username=username)
    user.habit_tracker.filter(id=habit_id).delete()


def find_user_habit(username, habit_id):
    user = User.objects.get(username=username)
    return user.habit_tracker.get(id=habit_id)
