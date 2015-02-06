from prime.models import Issue, Article, PDF, Recipe, DIYarticle
from main.models import RecipeTag, DIYTag
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

# utility functions

def get_recent_issues(issue_slug=None):
    if issue_slug is None:
        issue = Issue.objects.latest('release_date')
        recent_issues = Issue.objects.order_by('-release_date')[1:4]
    else:
        issue = get_object_or_404(Issue, slug=issue_slug)
        if issue == Issue.objects.latest('release_date'):
            recent_issues = Issue.objects.order_by('-release_date')[1:4]
        else:
            recent_issues = Issue.objects.order_by('-release_date')[0:3]
    return issue, recent_issues


# pages

class IssueView(View):

    def get(self, context, slug):
        issue, recent_issues = get_recent_issues(slug)
        #articles = Article.objects.filter(issue=issue).order_by('position')
        articles = Article.objects.filter(issue=issue).order_by('position').all()[:5]
        pdf = PDF.objects.get(issue=issue)
        context = {'issue': issue, 'recent_issues': recent_issues,
                   'articles': articles, 'pdf': pdf, 
                   'MEDIA_URL': settings.MEDIA_URL,
                   'STATIC_URL': settings.STATIC_URL}
        return render_to_response('prime/front.html', context)


class ArticleView(View):

    def get(self, context, issue_slug, article_slug):
        issue, recent_issues = get_recent_issues(issue_slug)
        try:
            article = Article.objects.filter(issue=issue).get(slug=article_slug)
        except Article.DoesNotExist:
            raise Http404
        if article.redirect:
            return redirect(article.redirect)
        articles = Article.objects.filter(issue=issue).order_by('position')
        pdf = PDF.objects.get(issue=issue)
        context = {'issue': issue, 'recent_issues': recent_issues,
                   'article': article, 'articles': articles, 'pdf': pdf,
                   'MEDIA_URL': settings.MEDIA_URL, 
                   'STATIC_URL': settings.STATIC_URL}
        return render_to_response('prime/article.html', context)


class LandingView(View):
    def get(self, context):
        articles = Article.objects.all()[:4]
        context = {
                    'articles': articles,
                    'MEDIA_URL': settings.MEDIA_URL,
                    'STATIC_URL': settings.STATIC_URL
                    } 
        return render_to_response('prime/landingbase.html', context)


class RecipeFrontView(View):
    def get(self, context):
        recipe_list = Recipe.objects.all()
        paginator = Paginator(recipe_list, 1)
        page = self.request.GET.get('page')
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)
        tags = RecipeTag.objects.all()
        context = { 'recipes': recipes,
                    'tags': tags,
                    'STATIC_URL': settings.STATIC_URL,
                    'MEDIA_URL': settings.MEDIA_URL
                    }
        return render_to_response('prime/recipefront.html', context)


class DIYFrontView(View):
    def get(self, context):
        articles = DIYarticle.objects.all()[:5]
        tags = DIYTag.objects.all()
        context = { 'articles': articles,
                    'tags': tags,
                    'STATIC_URL': settings.STATIC_URL,
                    'MEDIA_URL': settings.MEDIA_URL
                    }
        return render_to_response('prime/diyfront.html', context)



class RecipeView(View):

    def get(self, context, recipe_slug):
        try:
            recipe = Recipe.objects.get(slug=recipe_slug)
        except Recipe.DoesNotExist:
            raise Http404
        if recipe.redirect:
            return redirect(recipe.redirect)
        recipes = Recipes.objects.filter
        context = {
                    'recipe': recipe,
                    'pdf': pdf,
                    'MEDIA_URL': settings.MEDIA_URL, 
                    'STATIC_URL': settings.STATIC_URL
                    }
        return render_to_response('prime/recipe.html')

# special handlers

def error404(request): # not currently implemented
    issue, recent_issues = get_recent_issues()
    print "hello"
    context = {'issue': issue, 'recent_issues': recent_issues,
               'MEDIA_URL': settings.MEDIA_URL, 
               'STATIC_URL': settings.STATIC_URL}
    return render_to_response('404.html', context)
