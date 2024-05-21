from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = "pyusite"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("pyusite:homepage"))),
    path("homepage/", views.home_page, name="homepage"),
    path("page/", views.PageList.as_view(), name="page-list"),
    path("page/edit/create/", views.PageCreate.as_view(), name="page-create"),
    path("page/edit/update/<int:pk>/", views.PageUpdate.as_view(), name="page-update"),
    path("page/edit/delete/<int:pk>/", views.PageDelete.as_view(), name="page-delete"),
    path("page/edit/detail/<int:pk>/", views.PageDetail.as_view(), name="page-detail"),
    path("page/edit/popup/", views.PageCreate.as_view(), name="page-popup"),
    path(
        "page/<int:pk>/",
        views.PageView.as_view(),
        name="page",
    ),
    path(
        "page/<slug:slug>/",
        views.PageView.as_view(),
        name="page",
    ),
    path("section/", views.SectionList.as_view(), name="section-list"),
    path("section/edit/create/", views.SectionCreate.as_view(), name="section-create"),
    path(
        "section/edit/update/<int:pk>/",
        views.SectionUpdate.as_view(),
        name="section-update",
    ),
    path(
        "section/edit/delete/<int:pk>/",
        views.SectionDelete.as_view(),
        name="section-delete",
    ),
    path(
        "section/edit/detail/<int:pk>/",
        views.SectionDetail.as_view(),
        name="section-detail",
    ),
    path("section/edit/popup/", views.SectionCreate.as_view(), name="section-popup"),
    path("rack/", views.RackList.as_view(), name="rack-list"),
    path(
        "rack/<int:pk>/",
        views.RackView.as_view(),
        name="rack",
    ),
    path(
        "rack/<slug:slug>/",
        views.RackView.as_view(),
        name="rack",
    ),
    path("rack/edit/create/", views.RackCreate.as_view(), name="rack-create"),
    path("rack/edit/update/<int:pk>/", views.RackUpdate.as_view(), name="rack-update"),
    path("rack/edit/delete/<int:pk>/", views.RackDelete.as_view(), name="rack-delete"),
    path("rack/edit/detail/<int:pk>/", views.RackDetail.as_view(), name="rack-detail"),
    path("rack/edit/popup/", views.RackCreate.as_view(), name="rack-popup"),
    path("article/", views.ArticleList.as_view(), name="article-list"),
    path(
        "article/<int:pk>/",
        views.ArticleView.as_view(),
        name="article",
    ),
    path(
        "article/<slug:slug>/",
        views.ArticleView.as_view(),
        name="article",
    ),
    path("article/edit/create/", views.ArticleCreate.as_view(), name="article-create"),
    path(
        "article/edit/update/<int:pk>/",
        views.ArticleUpdate.as_view(),
        name="article-update",
    ),
    path(
        "article/edit/delete/<int:pk>/",
        views.ArticleDelete.as_view(),
        name="article-delete",
    ),
    path(
        "article/edit/detail/<int:pk>/",
        views.ArticleDetail.as_view(),
        name="article-detail",
    ),
    path("article/edit/popup/", views.ArticleCreate.as_view(), name="article-popup"),
    path("image/edit/popup/", views.ImijCreate.as_view(), name="imij-popup"),
    path("image/<int:pk>/", views.ImijDetail.as_view(), name="imij-detail"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
