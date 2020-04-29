import os

from django.shortcuts import render, reverse
from django.conf import settings
from .forms import ArticleSearchForm
from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from .models import Article, Search
from math import log2
from django.http import HttpResponseRedirect
import string
import re

neg_words = ['aggravated', 'agitated', 'alarmed', 'anger', 'angered', 'angry', 'anguish', 'antipathy', 'anxiety',
             'anxious', 'apprehension', "aren't", 'aversion', 'bad', 'befuddled', 'bewildered', 'bitterness', 'break',
             'broken', 'cannot', "can't", 'conceited', 'confound', 'confused', 'contempt', 'coward', 'crammed',
             'decrepit', 'deflated', 'dejected', 'deny', 'denied', 'depressed', 'desperate', 'despondent', "didn't",
             'disappointed', 'discombobulated', 'discomposed', 'disconcert', 'discontented', 'disgruntled', 'disgust',
             'disillusioned', 'dislike', 'dismayed', 'dispirited', 'displeasure', 'dissatisfied', 'distraught',
             'distressed', "doesn't", 'dread', 'embarrassed', 'enraged', 'envy', 'exasperated', 'excited', 'exploit',
             'fail', 'failure', 'fear', 'ferocious', 'flustered', 'fractious', 'frantic', 'frenzied', 'frenzy',
             'frightful', 'frightened', 'frustrated', 'fuddle', 'furious', 'gloomy', 'glumness', 'grievous', 'grouchy',
             'grumpy', 'guilty', "hadn't", "hasn't", "haven't", 'heartbroken', 'homesickness', 'hopeless', 'horrified',
             'horror', 'hostility', 'humiliated', 'hysterical', 'inconsolable', 'indignant', 'irritated', "isn't",
             'jealousy', 'jolted', 'lazy', 'livid', 'loathing', 'loneliness', 'mad', 'maddened', 'manic', 'melancholic',
             'miserable', 'misery', 'mortified', "mustn't", "needn't", 'nervous', 'no', 'nosy', 'outrage',
             'outraged', 'outrageous', 'overwrought', 'panicked', 'peculiar', 'perplexed', 'phrenetic', 'picky', 'rage',
             'regret', 'regretful', 'remorse', 'remorseful', 'resent', 'resentment', 'revulsion', 'sad', 'sadly',
             'sadness', 'scared', 'scary', 'scorn', 'shocked', "shouldn't", 'sorrowful', 'spite', 'stingy', 'stubborn',
             'stunned', 'tense', 'tenseness', 'terrified', 'terror', 'torment', 'uneasiness', 'upset', 'vengefulness',
             "wasn't", "weren't", 'wild', 'woeful', "won't", 'worried', "wouldn't", 'wrath', 'wretched'
             ]


def index(request):
    form = ArticleSearchForm()
    if 'query' and 'neg' in request.GET:
            return HttpResponseRedirect(reverse('retrievabl:search', kwargs={'query': request.GET['query'],
                                                                             'neg': request.GET['neg']}))
    return render(request, 'retrievabl/index.html', {'form': form})


def search(request):
    form = ArticleSearchForm()
    if 'query' in request.GET:
        query = request.GET['query']
        return HttpResponseRedirect('/search/' + query)
    return render(request, 'retrievabl/search.html', {'form': form})


def mission(request):
    form = ArticleSearchForm()
    if 'query' in request.GET:
        query = request.GET['query']
        return HttpResponseRedirect('/search/' + query)
    return render(request, 'retrievabl/our_mission.html', {'form': form})


def contact(request):
    form = ArticleSearchForm()
    if 'query' in request.GET:
        query = request.GET['query']
        return HttpResponseRedirect('/search/' + query)
    return render(request, 'retrievabl/contact_us.html', {'form': form})


def avg_doc_len(corpus):
    totlen = 0
    translator = str.maketrans('', '', string.punctuation)
    for doc in corpus:
        dbody = str(doc.body.lower().split()).translate(translator)
        length = len(re.findall(r'\w+', dbody))
        totlen += length
    avg = totlen / len(corpus)
    return avg


def neg_score(query, corpus):
    translator = str.maketrans('', '', string.punctuation)
    nw = neg_words
    query = query.lower()
    negbm25score = 0
    k = 1.25
    nk = 10 # weight for negative filtering
    avgdl = avg_doc_len(corpus)
    M = len(corpus)
    b = 0.75
    docfreq = {}
    freq = 0
    for doc in corpus:
        find_neg(doc)
        for word in query.lower().split():
            if word in str(doc.body.lower().split()).translate(translator):
                freq += 1
        docfreq[str(word).lower()] = freq
        freq = 0

    result = 0
    regbm25score = 0.0
    for doc in corpus:
        dbody = str(doc.body.lower().split()).translate(translator)
        length = len(re.findall(r'\w+', dbody))
        for word in query.split():
            if word in dbody:
                one = query.count(word.lower())
                two = (k + 1) * dbody.count(str(word).lower())
                three = dbody.count(str(word).lower()) + (k * (1 - b + (b * (length / avgdl))))
                four = log2((M + 1) / (doc.body.count(str(word)) + 1))
                result = one * (two / three) * four
                regbm25score += result

        result = (1 - ((doc.percentage / 100) * nk)) * regbm25score
        negbm25score = result
        doc.score = float(negbm25score)
        doc.save()
        negbm25score = 0.0
        regbm25score = 0.0


def reg_score(query, corpus):
    translator = str.maketrans('', '', string.punctuation)
    query = query.lower()
    regbm25score = 0
    k = 1.25
    avgdl = avg_doc_len(corpus)
    M = len(corpus)
    b = 0.75
    docfreq = {}
    freq = 0
    for doc in corpus:
        find_neg(doc)
        for word in query.lower().split():
            if word in str(doc.body.split()).translate(translator):
                freq += 1
        docfreq[str(word).lower()] = freq
        freq = 0
    for doc in corpus:
        dbody = str(doc.body.lower().split()).translate(translator)
        length = len(re.findall(r'\w+', dbody))
        for word in query.split():
            if word in dbody:
                    one = query.count(word.lower())
                    two = (k + 1) * dbody.count(str(word).lower())
                    three = dbody.count(str(word).lower()) + (k * (1 - b + (b * (length / avgdl))))
                    four = log2((M + 1) / (doc.body.count(str(word)) + 1))
                    result = one * (two / three) * four
                    regbm25score += result
        doc.score = float(regbm25score)
        doc.save()
        regbm25score = 0.0


def find_neg(doc):
    translator = str.maketrans('', '', string.punctuation)
    nw = neg_words
    neg_count = 0
    dbody = str(doc.body.lower().split()).translate(translator)
    for neg_word in nw:
        find = len(re.findall(str(neg_word), dbody))
        if find > 0:
            neg_count += find
    length = len(re.findall(r'\w+', dbody))
    doc.percentage = float(100 * (neg_count / length))
    doc.save()


class ArticleListView(ListView):
    template_name = 'retrievabl/search.html'
    context_object_name = 'articles'

    def get_ndcg(self, query):
        neg_score(query, Article.objects.all())
        articles = Article.objects.order_by('score').reverse().filter(score__gt=0)
        i = 1
        dcg = 0
        idcg = 0
        for article in articles:
            dcg += float(2 ** article.score - 1) / log2(i + 1)
            i += 1

        reg_score(query, Article.objects.all())
        articles = Article.objects.order_by('score').reverse().filter(score__gt=0)
        i = 1
        for article in articles:
            idcg += float(2 ** article.score - 1) / log2(i + 1)

        if idcg == 0:
            idcg = 1

        return float(dcg / idcg)

    def get_queryset(self):
        query = self.kwargs.pop('query', None)
        neg_rank = self.kwargs.pop('neg', None)

        if neg_rank == 1:
            neg_score(query, Article.objects.all())
        else:
            reg_score(query, Article.objects.all())

        result = Article.objects.order_by('score').reverse().filter(score__gt=0)
        return result
