ASSIGNEE_TASK = 0
UN_ASSIGNEE_TASK = 1
MOVE_PROGRESS = 2  # -- if user_A assignee task to user_B, and user_B changed or moved
                   # -- task progress, related user (user_A) must accept notifications
DEADLINE = 3
PENDING_TASK = 4
NOT_YET_ASSIGNEE = 5
COMMENT_TASK = 6
UPDATE_TASK = 7  # -- same as above, about related user
CREATED_PROJECT = 8

SUBJECT_CHOICES = (
    (ASSIGNEE_TASK, 'Assignee Task'),
    (UN_ASSIGNEE_TASK, 'Un Assignee Task'),
    (MOVE_PROGRESS, 'Move Progress'),
    (DEADLINE, 'Deadline'),
    (PENDING_TASK, 'Pending Task'),
    (NOT_YET_ASSIGNEE, 'Not Yet Assignee'),
    (COMMENT_TASK, 'Comment Task'),
    (UPDATE_TASK, 'Update Task'),
    (CREATED_PROJECT, 'Created Project')
)
