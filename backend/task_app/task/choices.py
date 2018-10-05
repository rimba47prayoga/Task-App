
class TaskChoices(object):
    TODO, IN_PROGRESS, IN_REPO, TEST, DONE = range(5)
    PROGRESS_CHOICES = (
        (TODO, 'TODO'),
        (IN_PROGRESS, 'IN PROGRESS'),
        (IN_REPO, 'IN REPOSITORY'),
        (TEST, 'TEST'),
        (DONE, 'DONE')
    )

    LOWEST, LOW, MEDIUM, HIGH, HIGHEST = range(5)
    PRIORITY_CHOICES = (
        (LOWEST, 'LOWEST'),
        (LOW, 'LOW'),
        (MEDIUM, 'MEDIUM'),
        (HIGH, 'HIGH'),
        (HIGHEST, 'HIGHEST')
    )

    TASK, SUB_TASK, BUG = range(3)
    TASK_TYPE_CHOICES = (
        (TASK, 'TASK'),
        (SUB_TASK, 'SUB TASK'),
        (BUG, 'BUG')
    )
