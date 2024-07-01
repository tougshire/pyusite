from datetime import date, datetime
import re
from django.db.models.query import QuerySet
from django_filters_stoex.views import FilterView
from django.contrib.auth.mixins import PermissionRequiredMixin
import logging
import urllib
import markdown
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, response
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django_filters_stoex.forms import (
    FilterstoreRetrieveForm,
    FilterstoreSaveForm,
)
from pyusite.filterset import ArticleFilter, RackFilter
from pyusite.forms import (
    ArticleForm,
    ArticleHangerFormset,
    ArticlecommentForm,
    PageForm,
    PageSectionFormset,
    RackForm,
    RackHangerFormset,
    ImijForm,
    SectionForm,
    SectionRackFormset,
)
from touglates.templatetags import touglates_tags as touglates
from .models import Article, Articlecomment, Menu, Page, Rack, Imij, Section

logger = logging.getLogger(__name__)


def get_modelfields_labels(model):
    fields = model._meta.get_fields()
    labels = {}

    for field in fields:
        try:
            labels[field.name] = field.verbose_name
        except:
            try:
                labels[field.name] = field.name.replace("_", " ")
            except:
                pass

    return labels


def home_page(request):
    try:
        page = Page.objects.filter(is_home=True).first()
        if page.slug:
            return HttpResponseRedirect(reverse("pyusite:page", args=[page.slug]))
        else:
            return PageView(page.id)
    except Exception as e:
        logger.error(e)
        return HttpResponse("Error retrieving the page")


class PageCreate(CreateView):
    model = Page
    form_class = PageForm
    template_name = "pyusite/edit/page_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "sections": PageSectionFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "sections": PageSectionFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "pyusite",
                    "model_name": "Page",
                },
            )
        return reverse("pyusite:page-detail", kwargs={"pk": self.object.pk})


class PageUpdate(UpdateView):
    model = Page
    form_class = PageForm
    template_name = "pyusite/edit/page_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "sections": PageSectionFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):

        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "sections": PageSectionFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        return reverse("pyusite:page-detail", kwargs={"pk": self.object.pk})


class PageDetail(DetailView):
    model = Page
    template_name = "pyusite/edit/page_detail.html"

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        context_data["object_labels"] = get_modelfields_labels(Page)

        return context_data


class PageDelete(DeleteView):
    model = Page
    template_name = "pyusite/edit/page_confirm_delete.html"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["object_labels"] = get_modelfields_labels(Page)

    def get_success_url(self):
        return reverse("pyusite:page-list")


class PageList(PermissionRequiredMixin, ListView):
    model = Page
    permission_required = "pyusite.view_page"
    template_name = "pyusite/edit/page_list.html"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["object_labels"] = get_modelfields_labels(Page)

        context_data["count"] = self.object_list.count()

        return context_data


class PageView(DetailView):
    model = Page
    template_name = "{}/page.html".format(settings.PYUSITE["TEMPLATE_DIR"])

    def get_context_data(self, **kwargs):
        md = markdown.Markdown(extensions=["fenced_code", "extra"])

        context_data = super().get_context_data(**kwargs)

        sections = []
        special_sections = []

        for object_section in context_data["object"].section_set.all():

            racks = []
            for object_rack in object_section.rack_set.all():
                hangers = []
                for object_hanger in object_rack.hanger_set.all():
                    if (
                        object_hanger.article.display == "Y"
                        and object_hanger.article.publish_date <= date.today()
                        and (
                            object_hanger.expiration_date is None
                            or object_hanger.expiration_date > date.today()
                        )
                    ):
                        hangers.append(
                            {
                                "pk": object_hanger.pk,
                                "article": {
                                    "pk": object_hanger.article.pk,
                                    "slug": object_hanger.article.slug,
                                    "author": object_hanger.article.author,
                                    "created_datetime": object_hanger.article.created_datetime,
                                    "updated_datetime": object_hanger.article.updated_datetime,
                                    "publish_date": object_hanger.article.publish_date,
                                    "content_classes": object_hanger.article.content_classes,
                                    "read_more": object_hanger.article.read_more,
                                    "title": object_hanger.article.title,
                                    "show_title": object_hanger.article.show_title,
                                    "summary": md.convert(
                                        object_hanger.article.summary
                                    ),
                                    "content": md.convert(
                                        object_hanger.article.content
                                    ),
                                    "if_summary_blank": object_hanger.article.if_summary_blank,
                                    "iframe_document": object_hanger.article.iframe_document,
                                    "iframe_src": object_hanger.article.iframe_src,
                                    "iframe_height": object_hanger.article.iframe_height,
                                },
                            }
                        )
                if hangers:
                    racks.append(
                        {
                            "pk": object_rack.pk,
                            "width": object_rack.width,
                            "title": object_rack.title,
                            "show_title": object_rack.show_title,
                            "content_before_articles": object_rack.content_before_articles,
                            "content_after_articles": object_rack.content_after_articles,
                            "hangers": hangers,
                        }
                    )
            if racks or object_section.collapse==False:
                new_section = {
                        "pk": object_section.pk,
                        "title": object_section.title,
                        "show_title": object_section.show_title,
                        "content_before_racks": object_section.content_before_racks,
                        "content_after_racks": object_section.content_after_racks,
                        "collapse": object_section.collapse,
                        "is_special": object_section.is_special,
                        "slug": object_section.slug,
                        "racks": racks,
                    }

                if object_section.is_special:
                    special_sections.append(new_section)
                else:
                    sections.append(new_section)


        context_data["sections"] = sections
        context_data["special_sections"] = special_sections

        context_data["page_menus"] = Menu.objects.filter(
            menupage__page=self.get_object()
        )
        context_data["main_menus"] = Menu.objects.filter(level__gte=1000)

        context_data["base_url"] = self.request.build_absolute_uri("/")

        try:
            context_data["upper_banner_image"] = Imij.objects.get(
                name=settings.PYUSITE["UPPER_BANNER_IMAGE"]
            )
        except (KeyError, AttributeError, Imij.DoesNotExist) as e:
            pass

        return context_data


class RackView(DetailView):
    model = Rack
    template_name = "pyusite/edit/{}/rack.html".format(settings.PYUSITE["TEMPLATE_DIR"])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data["main_menus"] = Menu.objects.filter(level__gte=1000)

        context_data["base_url"] = self.request.build_absolute_uri("/")

        return context_data


class ArticleCreate(CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "pyusite/edit/article_create.html"

    def get_initial(self):
        initial_values = super().get_initial()
        initial_values["author"] = self.request.user
        return initial_values

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["images"] = Imij.objects.all()

        context_data['pages'] = Page.objects.all()
        context_data['sections'] = Section.objects.all()
        context_data['racks'] = Rack.objects.all()


        formsetclasses = {
            "hangers": ArticleHangerFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "hangers": ArticleHangerFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "pyusite",
                    "model_name": "Article",
                },
            )

        return reverse("pyusite:article-detail", kwargs={"pk": self.object.pk})


class ArticleUpdate(UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "pyusite/edit/article_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        context_data["images"] = Imij.objects.all()
        context_data['pages'] = Page.objects.all()
        context_data['sections'] = Section.objects.all()
        context_data['racks'] = Rack.objects.all()



        formsetclasses = {
            "hangers": ArticleHangerFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):

        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "hangers": ArticleHangerFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        return reverse("pyusite:article-detail", kwargs={"pk": self.object.pk})


class ArticleDetail(DetailView):
    model = Article
    template_name = "pyusite/edit/article_detail.html"

    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)

        context_data["object_labels"] = get_modelfields_labels(Page)

        return context_data


class ArticleDelete(DeleteView):
    model = Article
    template_name = "pyusite/edit/article_confirm_delete.html"

    def get_success_url(self):
        return reverse("pyusite:article-list")


class ArticleList(PermissionRequiredMixin, FilterView):
    model = Article
    permission_required = "pyusite.view_article"
    filterset_class = ArticleFilter
    filterstore_urlname = "pyusite:article-filterstore"
    template_name = "pyusite/edit/article_filter.html"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()

        context_data["object_labels"] = get_modelfields_labels(Page)

        context_data["count"] = self.object_list.count()

        return context_data


class ArticleView(DetailView):
    model = Article
    template_name = "{}/article.html".format(settings.PYUSITE["TEMPLATE_DIR"])

    def get_context_data(self, *args, **kwargs):
        md = markdown.Markdown(extensions=["fenced_code", "extra"])

        context_data = super().get_context_data(*args, **kwargs)

        article = {
            "pk": context_data["object"].pk,
            "slug": context_data["object"].slug,
            "author": context_data["object"].author,
            "created_datetime": context_data["object"].created_datetime,
            "updated_datetime": context_data["object"].updated_datetime,
            "publish_date": context_data["object"].publish_date,
            "content_classes": context_data["object"].content_classes,
            "read_more": context_data["object"].read_more,
            "title": context_data["object"].title,
            "show_title": context_data["object"].show_title,
            "summary": md.convert(context_data["object"].summary),
            "content": md.convert(context_data["object"].content),
            "if_summary_blank": context_data["object"].if_summary_blank,
            "iframe_document": context_data["object"].iframe_document,
            "iframe_src": context_data["object"].iframe_src,
            "iframe_height": context_data["object"].iframe_height,
            "featured_image": context_data["object"].featured_image,
        }
        context_data["article"] = article
        context_data["object"] = article

        return context_data


class RackCreate(CreateView):
    model = Rack
    form_class = RackForm
    template_name = "pyusite/edit/rack_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "hangers": RackHangerFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "hangers": RackHangerFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "pyusite",
                    "model_name": "Rack",
                },
            )

        return reverse("pyusite:rack-detail", kwargs={"pk": self.object.pk})


class RackUpdate(UpdateView):
    model = Rack
    form_class = RackForm
    template_name = "pyusite/edit/rack_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "hangers": RackHangerFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):

        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "hangers": RackHangerFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        return reverse("pyusite:rack-detail", kwargs={"pk": self.object.pk})


class RackDetail(DetailView):
    model = Rack
    template_name = "pyusite/edit/rack_detail.html"


class RackDelete(DeleteView):
    model = Rack
    template_name = "pyusite/edit/rack_confirm_delete.html"

    def get_success_url(self):
        return reverse("pyusite:rack-list")


class RackList(PermissionRequiredMixin, FilterView):
    model = Rack
    permission_required = "pyusite.view_rack"
    filterset_class = RackFilter
    filterstore_urlname = "pyusite:rack-filterstore"
    template_name = "pyusite/edit/rack_filter.html"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["filterstore_retrieve"] = FilterstoreRetrieveForm()
        context_data["filterstore_save"] = FilterstoreSaveForm()

        context_data["object_labels"] = get_modelfields_labels(Page)

        context_data["count"] = self.object_list.count()

        return context_data


class SectionCreate(CreateView):
    model = Section
    form_class = SectionForm
    template_name = "pyusite/edit/section_create.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "racks": SectionRackFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(self.request.POST)
            else:
                context_data[formsetkey] = formsetclass()

        return context_data

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "racks": SectionRackFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "pyusite",
                    "model_name": "Section",
                },
            )

        return reverse("pyusite:section-detail", kwargs={"pk": self.object.pk})


class SectionUpdate(UpdateView):
    model = Section
    form_class = SectionForm
    template_name = "pyusite/edit/section_update.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)

        formsetclasses = {
            "racks": SectionRackFormset,
        }

        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                context_data[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                context_data[formsetkey] = formsetclass(instance=self.object)

        return context_data

    def form_valid(self, form):

        response = super().form_valid(form)

        self.object = form.save(commit=False)

        formsetclasses = {
            "racks": SectionRackFormset,
        }
        formsetdata = {}
        formsets_valid = True
        for formsetkey, formsetclass in formsetclasses.items():
            if self.request.POST:
                formsetdata[formsetkey] = formsetclass(
                    self.request.POST, instance=self.object
                )
            else:
                formsetdata[formsetkey] = formsetclass(instance=self.object)

            if (formsetdata[formsetkey]).is_valid():
                formsetdata[formsetkey].save()
            else:
                logger.critical(formsetdata[formsetkey].errors)
                formsets_valid = False

        if not formsets_valid:
            return self.form_invalid(form)

        return response

    def get_success_url(self):
        return reverse("pyusite:section-detail", kwargs={"pk": self.object.pk})


class SectionDetail(DetailView):
    model = Section
    template_name = "pyusite/edit/section_detail.html"


class SectionDelete(DeleteView):
    model = Section
    template_name = "pyusite/edit/section_confirm_delete.html"

    def get_success_url(self):
        return reverse("pyusite:section-list")

    def get_success_url(self):
        return reverse("pyusite:section-list")


class SectionList(PermissionRequiredMixin, ListView):
    model = Section
    permission_required = "pyusite.view_section"
    template_name = "pyusite/edit/section_list.html"

    def get_context_data(self, *args, **kwargs):

        context_data = super().get_context_data(*args, **kwargs)

        context_data["object_labels"] = get_modelfields_labels(Page)

        context_data["count"] = self.object_list.count()

        return context_data


class ArticlecommentCreate(CreateView):
    model = Articlecomment
    form_class = ArticlecommentForm
    template_name = "pyusite/edit/articlecomment_create.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "pyusite",
                    "model_name": "Articlecomment",
                },
            )

        return reverse("pyusite:article-view", kwargs={"pk": self.object.article.pk})


class ImijDetail(DetailView):
    model = Imij


class ImijCreate(CreateView):
    model = Imij
    form_class = ImijForm
    template_name = "pyusite/edit/imij_create.html"

    def get_success_url(self):
        if "popup" in self.request.get_full_path():
            return reverse(
                "touglates:popup_closer",
                kwargs={
                    "pk": self.object.pk,
                    "app_name": "pyusite",
                    "model_name": "Imij",
                    "to_field_value": urllib.parse.quote_plus(self.object.markdown_code)
                },
            )

        return reverse("pyusite:Imij-detail", kwargs={"pk": self.object.pk})
