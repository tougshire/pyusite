from django import forms
from django.contrib import admin
from django.urls import reverse
from .models import (
    Article,
    Articlecomment,
    Document,
    Hanger,
    Rack,
    Menu,
    Menuitem,
    MenuPage,
    Page,
    Imij,
    Section,
    Tag,
)

# from django_c_keditor_5.widgets import C_KEditor5Widget
from django.conf import settings


class ArticleModelForm(forms.ModelForm):
    create_rack_to_section = forms.ModelChoiceField(
        Section.objects.all(),
        required=False,
        help_text="If selected, create a new rack for this article in the selected section",
    )
    # content = forms.CharField(
    #     required=False
    #     # required=False, widget=C_KEditor5Widget(config_name="extends")
    # )


class MenuitemModelForm(forms.ModelForm):
    page = forms.ModelChoiceField(
        Page.objects.all(),
        required=False,
        help_text="If selected, auto-fill href with a URL that points to the page (! will overwrite anything placed in the href field!)",
    )
    rack = forms.ModelChoiceField(
        Rack.objects.all(),
        required=False,
        help_text="If selected, auto-fill href with a URL that points to the rack (! will overwrite anything placed in the href field!)",
    )


class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0


class MenuitemInline(admin.TabularInline):
    model = Menuitem
    extra = 0


class MenuPageInline(admin.TabularInline):
    model = MenuPage
    extra = 0


class RackInline(admin.TabularInline):
    model = Rack
    extra = 0


class HangerInline(admin.TabularInline):
    model = Hanger
    fk_name = "article"
    extra = 0


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["pk", "title", "slug", "updated_datetime"]
    fields = [
        "title",
        "show_title",
        "slug",
        "author",
        "display",
        "content",
        "summary",
        "if_summary_blank",
        ("iframe_document", "iframe_src", "iframe_height"),
        "publish_date",
        "create_rack_to_section",
    ]
    form = ArticleModelForm
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        HangerInline,
    ]

    def save_model(self, request, obj, form, change):

        saved = super().save_model(request, obj, form, change)

        if form.cleaned_data["create_rack_to_section"]:
            rack = Rack.objects.create(
                title=obj.title,
                slug=obj.slug,
                section=form.cleaned_data["create_rack_to_section"],
            )
            Hanger.objects.create(
                rack=rack,
                article=obj,
            )

        return saved


@admin.register(Articlecomment)
class ArticlecommentAdmin(admin.ModelAdmin):
    list_display = ("name", "content", "article", "when", "active")
    list_filter = ("active", "when")
    search_fields = ("name", "email", "content")
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class DocumentAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


class MenuAdmin(admin.ModelAdmin):
    inlines = [
        MenuitemInline,
    ]


class MenuitemAdmin(admin.ModelAdmin):
    form = MenuitemModelForm

    def save_model(self, request, obj, form, change):

        saved = super().save_model(request, obj, form, change)

        if form.cleaned_data["rack"]:
            rack = Page.objects.get(pk=form.cleaned_data["rack"].pk)
            obj.href = reverse("rack" + rack.slug)
            obj.href = reverse("pyusite:rack", kwargs={'slug':rack.slug})

            if not form.cleaned_data["label"]:
                obj.label = rack.title
            obj.save()

        if form.cleaned_data["page"]:
            page = Page.objects.get(pk=form.cleaned_data["page"].pk)
            obj.href = reverse("pyusite:page", kwargs={'slug':page.slug})
            if not form.cleaned_data["label"]:
                obj.label = page.title
            obj.save()

        return saved


class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        SectionInline,
        MenuPageInline,
    ]


# class RackAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"slug": ("title",)}
#     inlines = [
#         HangerInline,
#     ]


class SectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        RackInline,
    ]


class ImijAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)

admin.site.register(Document, DocumentAdmin)

admin.site.register(Menu, MenuAdmin)

admin.site.register(Menuitem, MenuitemAdmin)

admin.site.register(MenuPage)

admin.site.register(Page, PageAdmin)

# admin.site.register(Rack, RackAdmin)

admin.site.register(Rack)

admin.site.register(Hanger)

admin.site.register(Imij, ImijAdmin)

admin.site.register(Section, SectionAdmin)
