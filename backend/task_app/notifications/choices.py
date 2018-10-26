ASSIGNEE_TASK = 0
MOVE_PROGRESS = 1  # -- if user_A assignee task to user_B, and user_B changed or moved
                   # -- task progress, related user (user_A) must accept notifications
DEADLINE = 2
PENDING_TASK = 3
NOT_YET_ASSIGNEE = 4
COMMENT_TASK = 5
UPDATE_TASK = 6  # -- same as above, about related user
CREATED_PROJECT = 7

SUBJECT_CHOICES = (
    (ASSIGNEE_TASK, 'Assignee Task'),
    (MOVE_PROGRESS, 'Move Progress'),
    (DEADLINE, 'Deadline'),
    (PENDING_TASK, 'Pending Task'),
    (NOT_YET_ASSIGNEE, 'Not Yet Assignee'),
    (COMMENT_TASK, 'Comment Task'),
    (UPDATE_TASK, 'Update Task'),
    (CREATED_PROJECT, 'Created Project')
)
