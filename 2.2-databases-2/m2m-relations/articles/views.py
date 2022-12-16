from django.views.generic import ListView

from .models import Article, ArticleSection


class ArticleListView(ListView):
    template_name = 'articles/news.html'
    model = Article
    ordering = '-published_at'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for article in context['object_list']:
            main_section = ArticleSection.objects.filter(article=article, main_section=True)
            other_sections = ArticleSection.objects.all().filter(article=article,
                                                           main_section=False).order_by('section__sections')
            article.sorted_sections = list(main_section) + list(other_sections)
        return context