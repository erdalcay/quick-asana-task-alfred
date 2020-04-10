## Quick Asana Task

Alfred workflow to quickly create a new Asana task in your project.

### Installation 

- Create a blank workflow. 
- Right click on canvas, add `Inputs > Keyword`. Fill in the fields.
- Right click on canvas, add `Actions > Run Script`. Set language to `/bin/bash` and paste ```python task.py "$1"``` to the script field.
- Right click on canvas, add `Outputs > Post Notification`. Set title as `{query}`.
- Bind all the widgets.
- Go to workflow configuration, create 4 environment variables with below names and insert the values.

    ```workspace_id```,```project_id```,```user_id```,```auth_token```

- Right click on workflow name and select `Open in Finder`. 
- Create `task.py` and paste the code from [/task.py](https://github.com/erdalcay/quick-asana-task-alfred/blob/master/task.py)
- Install dependencies in the workflow folder using `pip`. 

That is all.

### Usage

Type in your keyword, provide a task name and a due date seperated by `::`

Example:

```
  quicktask TASK_NAME::DUE_DATE
```


```
  quicktask Buy Groceries::tomorrow
```

**Dates**

There are two options for the due date. A relative name or a date string in `yyyy-MM-dd` format.

Relative dates can be one of:

```
  ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'today', 'tomorrow']
```

Good luck!
