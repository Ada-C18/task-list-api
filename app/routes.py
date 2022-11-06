from flask import Blueprint, jsonify, abort, make_response, request


tasks_bp = Blueprint('tasks', __name__, url_prefix="/tasks")

### Create a Task: Valid Task With `null` `completed_at`

# As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body
# so that I know I successfully created a Task that is saved in the database.

0️⃣
app.route('/', methods = ['POST'])
def task_completed_null:
    pass
#   return {
#     "title": "A Brand New Task",
#     "description": "Test Description",
#     "completed_at": NULL
#   }, "201", "CREATED"

1️⃣
# {
#   "task": {
#     "id": 1,
#     "title": "A Brand New Task",
#     "description": "Test Description",
#     "is_complete": false
#   }
# }



### Get Tasks: Getting Saved Tasks
# As a client, I want to be able to make a `GET` request to `/tasks` when there is at least one saved task and get this response:
2️⃣

# `200 OK`
# ```json
# [
#   {
#     "id": 1,
#     "title": "Example Task Title 1",
#     "description": "Example Task Description 1",
#     "is_complete": false
#   },
#   {
#     "id": 2,
#     "title": "Example Task Title 2",
#     "description": "Example Task Description 2",
#     "is_complete": false
#   }
# ]
# ```
app.route('/', methods = ['GET'])
def saved_tasks:
    pass 





3️⃣
### Get Tasks: No Saved Tasks
# As a client, I want to be able to make a `GET` request to `/tasks` when there are zero saved tasks and get this response:
# `200 OK`
# ```json
# []
# ```

app.route('/', methods = ['GET'])
def no_saved_tasks:
    pass 



4️⃣
### Get One Task: One Saved Task
# As a client, I want to be able to make a `GET` request to `/tasks/1` when there is at least one saved task and get this response:
# `200 OK`
# ```json
# {
#   "task": {
#     "id": 1,
#     "title": "Example Task Title 1",
#     "description": "Example Task Description 1",
#     "is_complete": false
#   }
# }
# ```
# app.route('/', methods = ['GET'])
def one_saved_tasks:
    pass 


5️⃣
### Update Task

# As a client, I want to be able to make a `PUT` request to `/tasks/1` when there is at least one saved task with this request body:

# ```json
# {
#   "title": "Updated Task Title",
#   "description": "Updated Test Description",
# }
# ```

# and get this response:

# `200 OK`

# ```json
# {
#   "task": {
#     "id": 1,
#     "title": "Updated Task Title",
#     "description": "Updated Test Description",
#     "is_complete": false
#   }
# }
# ```
# Note that the update endpoint does update the `completed_at` attribute. This will be updated with custom endpoints implemented in Wave 03.

app.route('/', methods = ['GET'])
def update_tasks:
    pass 


### Delete Task: Deleting a Task

# As a client, I want to be able to make a `DELETE` request to `/tasks/1` when there is at least one saved task and get this response:

# `200 OK`

# ```json
# {
#   "details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"
# }
# ```

app.route('/', methods = ['DELETE'])
def delete_tasks:
    pass 



# ### No matching Task: Get, Update, and Delete

# As a client, if I make any of the following requests:

#   * `GET` `/tasks/<task_id>`
#   * `UPDATE` `/tasks/<task_id>`
#   * `DELETE` `/tasks/<task_id>`

# and there is no existing task with `task_id`

# The response code should be `404`.

# You may choose the response body.

# Make sure to complete the tests for non-existing tasks to check that the correct response body is returned.
app.route('/', methods = ['DELETE'])
def no_matching_tasks:
    pass 


# ### Create a Task: Invalid Task With Missing Data

# #### Missing `title`

# As a client, I want to be able to make a `POST` request to `/tasks` with the following HTTP request body

# ```json
# {
#   "description": "Test Description",
#   "completed_at": null
# }
# ```

# and get this response:

# `400 Bad Request`

# ```json
# {
#   "details": "Invalid data"
# }
# ```

# so that I know I did not create a Task that is saved in the database.
app.route('/', methods = ['DELETE'])
def missing_title_input:
    pass 




# #### Missing `description` 
# If the HTTP request is missing `description`, we should also get this response:
# `400 Bad Request`

# ```json
# {
#   "details": "Invalid data"
# }
# ```
app.route('/', methods = ['DELETE'])
def missing_description:
    pass 


#### Missing `completed_at`
# If the HTTP request is missing `completed_at`, we should also get this response:
# `400 Bad Request`
# ```json0️⃣
# {
#   "details": "Invalid data"
# }
# ```
app.route('/', methods = ['DELETE'])
def missing_description:
    pass 