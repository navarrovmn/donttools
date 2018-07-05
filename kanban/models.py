from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=140)


class Issue(models.Model):
    KIND_TODO = 0
    KIND_DOING = 1
    KIND_DONE = 2
    KIND_CHOICES = [
        (KIND_TODO, ('To Do')),
        (KIND_DOING, ('Doing')),
        (KIND_DONE, ('Done')),
    ]
    KIND_MAP = dict(KIND_CHOICES)

    title = models.CharField(max_length=140)
    kind = models.PositiveIntegerField(choices=KIND_CHOICES)
    kind_name = property(lambda self: self.kind_display())
    description = models.TextField()
    is_active = models.BooleanField()
    status = models.CharField(max_length=140)
