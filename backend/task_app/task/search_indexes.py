from haystack import indexes

from .models import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
        document=True,
        use_template=True,
        template_name='search/indexes/task/task_text.txt'
    )
    title = indexes.CharField(model_attr='title', boost=2)
    label = indexes.CharField(model_attr='label', null=True)
    assignee = indexes.CharField(model_attr='assignee__username', null=True)
    avatar = indexes.CharField(null=True)
    table = indexes.CharField()
    branch_name = indexes.CharField()
    descriptions = indexes.CharField(model_attr='descriptions', null=True)

    def get_model(self):
        return Task
    
    def prepare_avatar(self, obj):
        if obj.assignee:
            if hasattr(obj.assignee, 'userprofile'):
                return obj.assignee.userprofile.avatar
        return None

    def prepare_table(self, obj):
        return "task"

    def prepare_branch_name(self, obj):
        return obj.project.board_name + '-' + obj.branch
