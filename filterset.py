import django_filters
from .models import Article, Rack
from django.db import models
from django import forms
from django_filters_stoex.filters import CrossFieldSearchFilter


class ArticleFilter(django_filters.FilterSet):

    orderbyfields = django_filters.OrderingFilter(
        fields=(
            "title",
            "author",
            "slug",
            "iframe_document",
            "iframe_src",
            "created_datetime",
            "updated_datetime",
            "publish_date",
            "display",
        ),
    )

    class Meta:
        model = Article
        fields = (
            "title",
            "show_title",
            "author",
            "slug",
            "iframe_document",
            "iframe_src",
            "content",
            "summary",
            "if_summary_blank",
            "created_datetime",
            "updated_datetime",
            "publish_date",
            "display",
        )


class RackFilter(django_filters.FilterSet):
    orderbyfields = django_filters.OrderingFilter(
        fields=[
            "section",
            "title",
            "order",
            "display",
        ]
    )

    class Meta:
        model = Rack
        fields = [
            "section",
            "title",
            "slug",
            "display",
        ]
