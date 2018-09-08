#Daily Tracker
Are you crazy fan of git? Or maybe you fan of geeky stuff, which you can make with your console or terminal? Daily Tracker is thing, which make your dreams come true. It helps you to plan the most important projects and events of your life in the style of geeks from Silicon Valley.

###Installation
To install the program, firstly you should download the repository. Change the directory to some folder, that will contain the project and enter the following:

	git clone https://bitbucket.org/nkitsan/lab02

Than type:

	sudo pip3 install .

After that, you will be able to use Daily Tracker from any directory by the keyword 'tasker'.

###Usage
You can learn more about operations on each of entities type by typing --help, for example:

	tasker --help

###Start working
First of all you need to create a new user on the website, get your api-key and connect it to your console app:

	tasker login --api='the value of your api key'

###Working with tasker:
In Daily Tracker you can add tasks to the private list called 'Weekly Task', create public lists and share it with friends or teammates. Also you can create calendar events and establish your habits.

	tasker add_task --name='My first task in Daily Traker'

or

	tasker add_task --list_id=1 --name='My first task in Daily Traker'

Also to task you can add deadline, subtask, comment or change status of task. To add this elemnts to tasks in lists add --list_id

	tasker change_task --task_id=1 --deadline='2018-09-21 15:00' --status='IP'
	tasker add_subtask --task_id=1 --subtask='my first subtask'
	tasker add_comment --task_id=1 --text='My first comment'

To add your first event:

	tasker add_event --name='My first event' --date='14-09-2018 16:00'

To add new habit:

	tasker add_habit -name='My first habit'

More info about each command:
	tasker command --help
