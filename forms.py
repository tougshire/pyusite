import datetime
from django.conf import settings
from django.forms import ModelForm, SelectDateWidget, inlineformset_factory, Select
from django.urls import reverse_lazy
from .models import Article, Articlecomment, Imij, Page, Rack, Hanger, Section
from django import forms
from touglates.widgets import TouglatesRelatedSelect, SlugInput


class ArticleForm(ModelForm):
    image_select = forms.ModelChoiceField(
        required=False,
        queryset=Imij.objects.all(),
        to_field_name="markdown_code",
        widget=TouglatesRelatedSelect(
            related_data={
                "model_name": "Imij",
                "app_name": "pyusite",
                "add_url": reverse_lazy("pyusite:imij-popup"),
            },
        ),
        help_text="Select or add an image then copy the resulting code",
        label="select image"
    )
    image_width = forms.ChoiceField(
        choices=(
            (".width10", "width: 10%"),
            (".width20", "width: 20%"),
            (".width30", "width: 30%"),
            (".width40", "width: 40%"),
            (".width50", "width: 50%"),
            (".width60", "width: 60%"),
            (".width70", "width: 70%"),
            (".width80", "width: 80%"),
            (".width90", "width: 90%"),
        ),
        initial=".width80"
    )
    image_float = forms.ChoiceField(
        choices=(
            ("", "center"),
            (".left", "left"),
            (".righht", "right"),
        ),
        initial=""
    )

    image_code = forms.CharField(
        required=False,
        label="Code",
        widget=forms.TextInput(attrs={"class":"widthlong"}),
        help_text="Select an image above, select appropriate parameters, then copy the resulting code into the content or summary"
    )

    class Meta:
        model = Article
        fields = [
            "title",
            "show_title",
            "author",
            "slug",
            "iframe_document",
            "iframe_src",
            "iframe_height",
            "summary",
            "content",
            "if_summary_blank",
            "publish_date",
            "display",
            "featured_image",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "widthlong"}),
            "slug": SlugInput(
                slug_name="slug", input_name="title", attrs={"class": "widthlong"}
            ),
            "iframe_src": forms.TextInput(attrs={"class": "widthlong"}),
            "summary": forms.TextInput(attrs={"class": "widthlong"}),
            # "summary": C_KEditor5Widget(
            #     config_name="extends", attrs={"style": "width:100%;"}
            # ),
            "content": forms.Textarea(attrs={"class": "widthlong"}),
            # "content": C_KEditor5Widget(
            #     config_name="extends", attrs={"style": "width:100%;"}
            # ),
        }

class RackSelect(TouglatesRelatedSelect):
    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value:
            option["attrs"]["data-section"] = value.instance.section.id
            option["attrs"]["data-page"] = value.instance.section.page.id

        return option


class HangerForm(ModelForm):
    class Meta:
        fields = [
            "rack",
            "article",
            "order",
            "expiration_date",
        ]
        widgets = {
            "rack": RackSelect(
                related_data={
                    "model_name": "Rack",
                    "app_name": "pyusite",
                    "add_url": reverse_lazy("pyusite:rack-popup"),
                }
            )
        }


class RackForm(ModelForm):
    class Meta:
        model = Rack
        fields = [
            "section",
            "title",
            "show_title",
            "slug",
            "width",
            "show_article_meta",
            "content_before_articles",
            "content_after_articles",
            "order",
            "display",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "widthlong"}),
            "slug": SlugInput(
                slug_name="slug", input_name="title", attrs={"class": "widthlong"}
            ),
        }


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = [
            "page",
            "title",
            "show_title",
            "slug",
            "order",
            "content_before_racks",
            "content_after_racks",
            "display",
            "collapse",
            "is_special",

        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "widthlong"}),
            "slug": SlugInput(
                slug_name="slug", input_name="title", attrs={"class": "widthlong"}
            ),
        }


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = [
            "title",
            "show_title",
            "slug",
            "is_home",
            "order",
            "display",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "widthlong"}),
            "slug": SlugInput(
                slug_name="slug", input_name="title", attrs={"class": "widthlong"}
            ),
        }


class ArticlecommentForm(forms.ModelForm):
    class Meta:
        model = Articlecomment
        fields = ("name", "email", "content")


class ImijForm(forms.ModelForm):
    class Meta:
        model = Imij
        fields = ("imagefile", "name", "alt_text", "title")


ArticleHangerFormset = inlineformset_factory(Article, Hanger, form=HangerForm, extra=10)
RackHangerFormset = inlineformset_factory(Rack, Hanger, form=HangerForm, extra=10)
PageSectionFormset = inlineformset_factory(Page, Section, form=SectionForm, extra=10)
SectionRackFormset = inlineformset_factory(Section, Rack, form=RackForm, extra=10)
