
from core.services.base_service import BaseService
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
            # TODO: send email to user if he not assignee to himself
            task.assignee = assignee
        if task_type == TaskChoices.SUB_TASK:
            task.parent = self.payload.get('parent')  # it must be instance

        task.deadline = self.payload.get('deadline')
        task.descriptions = self.payload.get('descriptions')
        task.created_by = self.payload.get('created_by')
        task.save()
        return task
