from core.services.base_service import BaseService
from notifications.choices import *
from notifications.tasks import NotificationTask
from task.choices import TaskChoices
from task.models import Task


class CreateTaskService(BaseService):

    def execute(self):
        task = Task()
        task.project = self.payload.get('project')
        task.title = self.payload.get('title')
        task_type = self.payload.get('task_type')
        task.task_type = task_type
        task.label = self.payload.get('label')
        task.priority = self.payload.get('priority')
        task.branch = Task.generate_branch()
        assignee = self.payload.get('assignee')
        if assignee:
            task.assignee = assignee
        if task_type == TaskChoices.SUB_TASK:
            task.parent = self.payload.get('parent')  # it must be instance

        task.deadline = self.payload.get('deadline')
        task.descriptions = self.payload.get('descriptions')
        created_by = self.payload.get('created_by')
        task.created_by = created_by
        task.save()
        if assignee != created_by:
            # send email & notifications to user if he not assignee task to himself

            title = f'{created_by.username} assigned an task to you.'
            payload = {
                'title': title,
                'recipient': assignee.id,
                'subject': ASSIGNEE_TASK,
                'related_data': task.id
            }
            NotificationTask.task_push_notification.delay(payload)
        return task
