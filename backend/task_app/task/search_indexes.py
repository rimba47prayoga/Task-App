from haystack import indexes

from .models import Task


class TaskIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
        document=True,
        use_template=True,
        template_name='search/indexes/task/task_text.txt'
    )
    title = indexes.CharField(model_attr='title', boost=2)
    label = indexes.CharField(model_attr='label')
    assignee = indexes.CharField(model_attr='assignee__username', null=True)
    branch_name = indexes.CharField()
    descriptions = indexes.CharField(model_attr='descriptions', null=True)

    def get_model(self):
        return Task

    def prepare_branch_name(self, obj):
        return obj.prefix_branch + '-' + obj.branch
