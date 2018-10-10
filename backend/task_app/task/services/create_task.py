
from core.services.base_service import BaseService
from task.choices import TaskChoices
from task.models import Task


class CreateTaskService(BaseService):

    def execute(self):
        task = Task()
        task.title = self.payload.get('title')
        task_type = self.payload.get('task_type')
        task.task_type = task_type
        task.label = self.payload.get('label')
        task.priority = self.payload.get('priority')
        task.prefix_branch = self.payload.get('prefix_branch')
        task.branch = self.payload.get('branch')
        progress = self.payload.get('progress')
        if not progress:
            progress = TaskChoices.TODO
        task.progress = progress
        assignee = self.payload.get('assignee')
        if assignee:
            task.assignee = assignee
        task.progress = self.payload.get('progress')
        if task_type == TaskChoices.SUB_TASK:
            task.parent = self.payload.get('parent')  # it must be instance
        task.descriptions = self.payload.get('descriptions')
        task.created_by = self.payload.get('created_by')
        task.save()
        return task
