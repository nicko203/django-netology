from django.contrib import admin
from .models import Article, Section, ArticleSection
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet


class SectionInlineFormset(BaseInlineFormSet):
    def clean(self):
        count = 0
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data['main_section']:
                count += 1
        if count > 1:
            raise ValidationError('Основным может быть только один раздел')
        elif count == 0:
            raise ValidationError('Укажите основной раздел')
        return super().clean()


class SectionInline(admin.TabularInline):
    model = ArticleSection
    formset = SectionInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    pass
