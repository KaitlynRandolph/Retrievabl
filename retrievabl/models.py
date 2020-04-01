from django.db import models


class Article(models.Model):
    article_title = models.CharField(max_length=100)
    article_body = models.TextField()
    body_preview = models.CharField(max_length=300)

    def get_preview(self):
        return self.article_body[:300]

    def __str__(self):
        return self.article_title + ": " + self.article_body


class NegWordsLM(models.Model):
    xyz = models.TextField()


class SearchResults(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    rank = models.DecimalField(max_digits=15, decimal_places=2)