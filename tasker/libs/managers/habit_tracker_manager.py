"""
Manager for adding, deleting and changing habits in the habit tracker
"""


from tasker.models import User, Habit
from tasker.libs.logger.logger import get_logs


@get_logs
def create_habit(username, habit_name):
    """
    Creates a new habit for an user

    :param username: an username of an user
    :param habit_name: a name of new habit
    :return: an essence of created habit
    """
    user = User.objects.get(username=username)
    return user.habit_tracker.create(name=habit_name)


@get_logs
def change_habit_timeline(username, habit_id, timeline):
    """
    Changes a habit timeline

    :param username: an username of an user
    :param habit_id: an id of a changing habit
    :param timeline:
    """
    habit = find_user_habit(username, habit_id)
    habit.timeline = timeline
    habit.save()


@get_logs
def change_habit_status(username, habit_id, status):
    """
    Changes a habit status

    :param username: an username of an user
    :param habit_id: an id of a changing habit
    :param status: a new value of status
    """
    habit = find_user_habit(username, habit_id)
    if status == 'F' and habit.status == 'NS' and habit.count < habit.timeline:
        habit.status = status
        habit.count += 1
        habit.save()
    elif status == 'NS' and habit.status == 'F' and habit.count < habit.timeline:
        habit.status = status
        habit.count -= 1
        habit.save()


@get_logs
def change_habit_name(username, habit_id, new_name):
    """
    Changes a habit name

    :param username: an username of an user
    :param habit_id: an id of a changing habit
    :param new_name: a value of new name
    """
    habit = find_user_habit(username, habit_id)
    habit.name = new_name
    habit.save()


@get_logs
def delete_habit(username, habit_id):
    """
    Deletes a habit

    :param username: an username of an user
    :param habit_id: an id of a habit to delete
    """
    user = User.objects.get(username=username)
    user.habit_tracker.filter(id=habit_id).delete()


@get_logs
def find_user_habit(username, habit_id):
    """
    Finds an user habit by id

    :param username: an username of an user
    :param habit_id: an id of a searched habit
    :return: an essence of a searched habit or None if habit was not found
    """
    user = User.objects.get(username=username)
    if user.habit_tracker.filter(id=habit_id).exists():
        return user.habit_tracker.get(id=habit_id)
    else:
        return None


@get_logs
def get_user_habits(username):
    user = User.objects.get(username=username)
    return user.habit_tracker.all()


@get_logs
def get_user_habit(username, habit_id):
    user = User.objects.get(username=username)
    if user.habit_tracker.filter(id=habit_id).exists():
        return user.habit_tracker.get(id=habit_id)
    return None