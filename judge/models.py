from django.db import models

# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=100)
    statement = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Solution(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    verdict = models.CharField(max_length=100)
    submitted_at = models.DateTimeField()
    submitted_code = models.TextField()

    def __str__(self):
        return self.verdict


class TestCase(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)

    def __str__(self):
        return self.input
