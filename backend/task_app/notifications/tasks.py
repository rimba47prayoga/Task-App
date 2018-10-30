from datetime import date, timedelta

from celery.schedules import crontab
from celery.task import periodic_task
from django.contrib.auth.models import User

from task.choices import TaskChoices
from task.models import Task
from .choices import DEADLINE, PENDING_TASK, NOT_YET_ASSIGNEE
from .models import Notifications


class TaskAppSchedule(object):

    @staticmethod
    @periodic_task(run_every=(crontab(hour=23, minute=12)),
                   name="task_schedule_push_notifications",
                   ignore_result=True)
    def push_notifications():
        today = date.today()
        last_two_day = today - timedelta(days=2)
        filter_kwargs = {
            'deadline__range': [last_two_day, today],
            'progress__in': [TaskChoices.TODO, TaskChoices.IN_PROGRESS]
        }

        deadlines = Task.objects.filter(**filter_kwargs)
        filter_kwargs = {
            'deadline__gt': today,
            'progress__in': [TaskChoices.TODO, TaskChoices.IN_PROGRESS]
        }
        pending_task = Task.objects.filter(**filter_kwargs)
        result = []
        if deadlines.exists():
            for task in deadlines:
                deadline_date = task.deadline.strftime('%d, %b %Y')
                if task.assignee:
                    message = f'Please complete this task {task.branch_name}, ' \
                              f'the deadline will be ended at {deadline_date}.'

                    notification_id = Notifications.generate_notification_id(
                        user_id=task.assignee_id,
                        subject=DEADLINE,
                        branch_name=task.branch_name
                    )
                    notification = Notifications()
                    notification.notification_id = notification_id
                    notification.subject = DEADLINE
                    notification.title = 'Complete your deadline.'
                    notification.message = message
                    notification.user = task.assignee
                    notification.save()
                else:
                    users = User.objects.all()
                    message = f'Task {task.branch_name} not yet assigned, but the ' \
                              f'deadline will be ended at {deadline_date}'
                    for user in users:
                        notification_id = Notifications.generate_notification_id(
                            user_id=user.id,
                            subject=[DEADLINE, NOT_YET_ASSIGNEE],
                            branch_name=task.branch_name
                        )
                        notification = Notifications()
                        notification.notification_id = notification_id
                        notification.subject = NOT_YET_ASSIGNEE
                        notification.title = f'Please assign this task ' \
                                             f'{task.branch_name}.'
                        notification.message = message
                        notification.user = user
                        notification.save()
            result.append("Successfully pushed deadline notifications.")
        else:
            result.append("Deadline does not exist.")

        if pending_task.exists():
            for task in pending_task:
                if task.assignee:
                    message = f"Please update the deadline date, " \
                              f"Task {task.branch_name} is out of deadline."
                    notification_id = Notifications.generate_notification_id(
                        user_id=task.assignee_id,
                        subject=PENDING_TASK,
                        branch_name=task.branch_name
                    )
                    notification = Notifications()
                    notification.notification_id = notification_id
                    notification.subject = PENDING_TASK
                    notification.title = f'Task {task.branch_name} is out of deadline.'
                    notification.message = message
                    notification.user = task.assignee
                    notification.save()
                else:
                    users = User.objects.all()
                    message = f"Task {task.branch_name} is never assigned, " \
                              f"but this task was out of deadline."
                    for user in users:
                        notification_id = Notifications.generate_notification_id(
                            user_id=user.id,
                            subject=[PENDING_TASK, NOT_YET_ASSIGNEE],
                            branch_name=task.branch_name
                        )
                        notification = Notifications()
                        notification.notification_id = notification_id
                        notification.subject = NOT_YET_ASSIGNEE
                        notification.title = f'Task {task.branch_name} is out of deadline.'
                        notification.message = message
                        notification.user = user
                        notification.save()
            result.append("Successfully pushed pending task notifications.")
        else:
            result.append("Pending task does not exists")
        return ", ".join(result)
