import sys
import json
import requests
import datetime
import os

'''
Environment variables.
Need to be configured within the workflow settings.
'''
workspace_id = os.getenv('workspace_id')
project_id = os.getenv('project_id')
user_id = os.getenv('user_id')
token = os.getenv('auth_token')

def getDateStringForDueDate(due_day, relative_dates):
	'''
	Helper function to calculate the next weekday.
	@@ https://stackoverflow.com/questions/6558535/find-the-date-for-the-first-monday-after-a-given-a-date
	'''
	dateStringForWeekday = lambda dt, day: dt + datetime.timedelta(days=(day - dt.weekday() + 7) % 7)
	
	today = datetime.date.today()

	today_weekday_index = today.weekday()
	
	due_weekday_index = relative_dates.index(due_day)
	
	due_day_as_date = dateStringForWeekday(today, due_weekday_index)
	
	'''
		Bunch of ugly ifs
	'''
	if due_weekday_index > 6:
		if due_weekday_index == 7:
			due_weekday_index = today_weekday_index
		elif due_weekday_index == 8:
			due_weekday_index = today_weekday_index + 1
		due_day_as_date = dateStringForWeekday(today, due_weekday_index)
	elif today_weekday_index == due_weekday_index:
		due_day_as_date = datetime.date(today.year, today.month, today.day + 7)

	'''
		Convert the date object to the correct format: YYYY-MM-DD
	'''
	due_day_as_date = due_day_as_date.strftime("%Y-%m-%d")
	
	return due_day_as_date

try:
	task_details = sys.argv[1] 
	title, due_day = task_details.split('::')

	relative_dates = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'today', 'tomorrow']

	due = ''

	due_in_date_format = True
	
	try:
		datetime.datetime.strptime(due_day, '%Y-%m-%d')
	except ValueError as e:
		due_in_date_format = False	
	
	if due_in_date_format:
		due = due_day
	else:
		if due_day.lower() not in relative_dates:
			raise Exception('Due date error')
		due = getDateStringForDueDate(due_day.lower(), relative_dates)

	api_endpoint = "https://app.asana.com/api/1.0/tasks"

	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": "Bearer " + token
	}

	task = {
	  "data": {
	    "name": title,
	    "assignee": user_id,
	    "assignee_status": "upcoming",
	    "completed": False,
	    "due_on": due,
	    "projects": [
	      project_id
	    ],
	    "workspace": workspace_id
	  }
	}

	resp = requests.post(
			api_endpoint,
			headers=headers,
			data=json.dumps(task)
		)

	if resp.status_code == 201:
		print('A new task in your Asana project has been successfully created.')
	else:
		raise Exception('')

except Exception as e:
	if e.message == 'Due date error':
		print('Please provide a valid due date.')
	else:
		print('An error occured, please check your input and try again.')
