from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    body_preview = models.CharField(max_length=300)
    url = models.TextField()
    source = models.CharField(max_length=75)
    score = models.DecimalField(max_digits=15, decimal_places=3)
    percentage = models.DecimalField(max_digits=15, decimal_places=2)

    def get_preview(self):
        return self.body[:300]

    def __str__(self):
        return self.title + ": " + self.body_preview


class Search(models.Model):
    query = models.CharField(max_length=100)
    neg = models.IntegerField(choices=((1, "Neg. Filtering"), (0, "Reg. BM25")), default=1)
    ndcg = models.DecimalField(max_digits=15, decimal_places=3)
