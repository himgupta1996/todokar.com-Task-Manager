from application.db_schema import User, Course, Enrollment, ToDoTask, UserTaskAssociation
from application.apihandlers.AbstractApiHandler import *
import application.constants as global_constants
# from flask import render_template

class ToDoAllApiHandler(AbstractApiHandler):
	def __init__(self, *args, **kargs):
		super(ToDoAllApiHandler, self).__init__(*args, **kargs)

	def _get_user_task_information(self, match_dict):
		tasks = list(User.objects.aggregate(*[
		    {
		        '$lookup': {
		            'from': 'user_task_association', 
		            'localField': 'user_id', 
		            'foreignField': 'user_id', 
		            'as': 'e1'
		        }
		    }, {
		        '$unwind': {
		            'path': '$e1', 
		            'includeArrayIndex': 'e1_id', 
		            'preserveNullAndEmptyArrays': False
		        }
		    }, {
		        '$lookup': {
		            'from': 'to_do_task', 
		            'localField': 'e1.task_id', 
		            'foreignField': 'task_id', 
		            'as': 'e2'
		        }
		    }, {
		        '$unwind': {
		            'path': '$e2', 
		            'preserveNullAndEmptyArrays': False
		        }
		    }, {
		        '$match': match_dict
		    }
		]))
		return tasks

	def get(self):

		match_dict = {'user_id': self.user_id}
		total_tasks = self._get_user_task_information(match_dict)

		for task in total_tasks:
			if task["e2"]["status"] == Constants.IN_PROGRESS_STATUS:			
				date_added = datetime.strptime(task["e2"]["date_added"], '%Y-%m-%d')
				date_current = datetime.today()
				days_difference = (date_current-date_added).days
				task["e2"]["days_taken"] = days_difference+1

		return render_template("selfDevelopmentTools/todo_all.html", todo = True, todo_all = True, total_tasks = total_tasks)