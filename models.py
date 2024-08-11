from datetime import date
from django.db import models
from django.conf import settings
from django.utils.text import slugify

class Page(models.Model):
    title = models.CharField(
        "title",
        blank=True,
        max_length=200,
        help_text="The title of the page. to be displayed (can be blank)",
    )
    show_title = models.BooleanField(
        "show title",
        default=True,
        help_text="If the title should be shown (if not blank)",
    )
    slug = models.SlugField(
        "name/slug",
        max_length=100,
        unique=True,
        help_text="The name or slug for use in URLs and within the application.  Note: Auto-generated value may not be unique. Uniquness and format are checked after submit",
    )

    is_home = models.BooleanField(
        "is home page", default=False, help_text="If this is the home page"
    )
    order = models.IntegerField(
        "order",
        default=0,
        help_text="The order that the page would appear in a list",
    )
    display = models.CharField(
        "display",
        max_length=2,
        choices=[("Y", "Normal"), ("H", "Hide from Menus"), ("N", "Do not display")],
        default="Y",
        help_text="How the page should be displayed",
    )

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ("order", "title")


class Section(models.Model):
    page = models.ForeignKey(
        Page,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The page to which this section belongs",
    )
    title = models.CharField(
        "title",
        blank=True,
        max_length=200,
        help_text="The title of the page. to be displayed (can be blank)",
    )
    show_title = models.BooleanField(
        "show title",
        default=True,
        help_text="If the title of this section should be shown (if not blank)",
    )
    slug = models.SlugField(
        "name/slug",
        max_length=100,
        unique=True,
        help_text="The name or slug for use in URLs and within the application.  Note: Auto-generated value may not be unique. Uniquness and format are checked after submit",
    )
    order = models.IntegerField(
        "order",
        default=0,
        help_text="The order that the section should appear on the page",
    )
    content_before_racks = models.TextField(
        blank=True,
        help_text="content to be displayed before the racks",
    )
    content_after_racks = models.TextField(
        blank=True,
        help_text="content to be displayed after the racks",
    )
    display = models.CharField(
        "display when",
        max_length=2,
        choices=[("Y", "Normal"), ("P", "Preview Only"), ("N", "Do not display")],
        default="Y",
        help_text="How the section should be displayed",
    )
    collapse = models.BooleanField(
        "collapse", default=True, help_text="Collapse if there are no racks"
    )
    is_special = models.BooleanField(
        default=False,
        help_text="If the section is special and thus won't be included in the regular loop"
    )
    def __str__(self):
        return '"{}" on page "{}"'.format(
            self.title if self.title > "" else self.slug, self.page
        )

    class Meta:
        ordering = ("page", "order")


class Rack(models.Model):
    section = models.ForeignKey(
        Section,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The section to which the rack belongs",
    )
    title = models.CharField(
        "title",
        blank=True,
        max_length=200,
        help_text="The title of the rack to be displayed (can be blank)",
    )
    show_title = models.BooleanField(
        "show title",
        default=False,
        help_text="If the title should be shown (if not blank)",
    )
    slug = models.SlugField(
        "name/slug",
        max_length=100,
        unique=True,
        help_text="The name or slug for use in URLs and within the application.  Note: Auto-generated value may not be unique. Uniquness and format are checked after submit",
    )
    width = models.IntegerField(
        "width",
        default=1,
        help_text="The width of the rack in multiples of how big it is compared to the narrowest rack",
    )
    show_article_meta = models.CharField(
        "show article meta",
        max_length=2,
        choices=[
            ("00", "None"),
            ("a0", "Author"),
            ("0d", "Publish Date"),
            ("ad", "Author and Date"),
        ],
        default="00",
        help_text="What article meta information should be shown for aticles in racks",
    )
    content_before_articles = models.CharField(
        "content before articles",
        max_length=255,
        blank=True,
        help_text="The content of the rack before any included articles",
    )

    content_after_articles = models.CharField(
        "content after articles",
        max_length=255,
        blank=True,
        help_text="The content of the rack after any included articles",
    )
    order = models.IntegerField(
        "order",
        default=0,
        help_text="A number used for ordering of the rack in a section",
    )
    display = models.CharField(
        "display",
        max_length=2,
        choices=[
            ("Y", "Normal"),
            ("P", "Preview Only"),
            ("N", "Do not display"),
        ],
        default="Y",
        help_text="How the rack should be displayed. Racks that are hidden from sections may still be displayed independently",
    )
    collapse = models.BooleanField(
        "collapse", default=True, help_text="Collapse if there are no hangers/articles"
    )

    def __str__(self):

        return '"{}" in section "{}"'.format(
            self.title if self.title > "" else self.slug, self.section
        )

    class Meta:
        ordering = (
            "section",
            "order",
        )


class Document(models.Model):
    title = models.CharField(
        "title",
        max_length=200,
        blank=True,
        help_text="The title to be displayed with document.  It may or may not correspond to anything in the document itself. (can be blank)",
    )
    show_title = models.BooleanField(
        "show title",
        default=True,
        help_text="If the title should be shown (if not blank)",
    )
    slug = models.SlugField(
        "name/slug",
        max_length=100,
        unique=True,
        help_text="The name or slug for use in URLs and within the application.  Note: Auto-generated value may not be unique. Uniquness and format are checked after submit",
    )

    doc_file = models.FileField(
        upload_to="documents", help_text="The file to be uploaded"
    )

    def __str__(self):
        return (
            self.title
            if self.title > ""
            else self.slug if self.slug > "" else str(self.pk)
        )


class Imij(models.Model):

    imagefile = models.ImageField("file", upload_to="pyusiteimages")
    name = models.CharField(
        "name",
        max_length=20,
        unique=True,
        help_text="The name to be used by authors to identify the image",
    )
    alt_text = models.TextField(
        "alt text",
        help_text="The default alt-text to be redered in the template.  This is the text displayed for the visually impaired",
    )
    title = models.CharField(
        "title",
        max_length=80,
        blank=True,
        help_text="The default title of the image to be used in rendering.  This is a tool-tip that appears when the user holds the mouse pointer over the image",
    )

    @property
    def markdown_code(self):
        return "![{}]({})".format(self.alt_text, self.imagefile.url)

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(
        "title", max_length=200, help_text="The title of the article."
    )
    show_title = models.BooleanField(
        "show title",
        default=True,
        help_text="If the title should be shown (if not blank)",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pyusite_article",
    )
    slug = models.SlugField(
        "name/slug",
        max_length=100,
        unique=True,
        help_text="The name or slug for use in URLs and within the application.  Note: Auto-generated value may not be unique. Uniquness and format are checked after submit",
    )
    iframe_document = models.ForeignKey(
        Document,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="If selected, the document to be displayed in the iframe.  This will take precedence over anything entered in the iframe source field",
    )
    iframe_src = models.CharField(
        "iframe source",
        max_length=255,
        blank=True,
        help_text="If an iframe is to be displayed, the URL of an approved iframe source (must be listed in settings), optionally followed by a css height value",
    )
    iframe_height = models.CharField(
        "iframe height",
        max_length=20,
        blank=True,
        help_text="The height of the iframe using css height syntax.  Blank to use values set in stylesheets",
    )
    content = models.TextField(
        "content",
        blank=True,
        help_text="The content of the article",
    )
    content_classes = models.CharField(
        "content classes",
        max_length=50,
        blank=True,
        help_text="Extra classes to be applied to the content when displayed",
    )
    summary = models.TextField(
        "summary",
        blank=True,
        help_text="A summary of the content of the article",
    )
    if_summary_blank = models.IntegerField(
        "If summary is blank",
        choices=[
            (0, "Show Blank"),
            (1, "Show Content"),
        ],
        default=1,
        help_text="What to display if the summary is blank",
    )
    read_more = models.CharField(
        max_length=50,
        default="Read More",
        blank=True,
        help_text="Text to display in a read more link",
    )
    created_datetime = models.DateTimeField(
        "date/time created",
        auto_now_add=True,
        help_text="The date/time that this article was created",
    )
    updated_datetime = models.DateTimeField(
        "date/time updated",
        auto_now=True,
        help_text="The date/time that this article was updated",
    )
    publish_date = models.DateField(
        "published",
        default=date.today,
        help_text="The published date, which can be filled in by the editors.  Used for sorting when more than one article is in a rack.",
    )
    display = models.CharField(
        "display",
        max_length=2,
        choices=[
            ("Y", "Normal"),
            ("P", "Preview Only"),
            ("N", "Do not display"),
        ],
        default="Y",
        help_text="How the section should be displayed.  If hidden from racks, the article may still be found by other means",
    )
    featured_image = models.ForeignKey(
        Imij,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The image to be displayed when linking to the article on social media",
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ("-publish_date", "title")


class Hanger(models.Model):
    rack = models.ForeignKey(
        Rack,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The rack that holds the article",
    )
    article = models.ForeignKey(
        Article,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        help_text="The article held by the containing article",
    )
    order = models.IntegerField(
        "order",
        default=0,
        help_text="A number used to order the articles, overriding the default",
    )
    expiration_date = models.DateField(
        "expiration date",
        blank=True,
        null=True,
        help_text="The date after which the article should no longer be displayed in the rack",
    )

    def __str__(self):
        return '"{}" in rack "{}"'.format(self.article, self.rack)

    class Meta:
        ordering = ("rack", "order", "article")


class Tag(models.Model):
    name = models.CharField("name", max_length=100, help_text="The name of the tag.")
    slug = models.SlugField(
        "slug", max_length=100, unique=True, help_text="The slug for use in URLs"
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Menu(models.Model):
    name = models.CharField(
        "name", max_length=30, blank=True, help_text="The label of this menu item"
    )
    level = models.IntegerField(
        "level",
        default=0,
        help_text="A number, like an id (but not unique enforced), which can be used for the page to indentify the menu. Use of 1000 for the main menu is recommended",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-level",)


class Menuitem(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The menu to which this item belongs",
    )

    href = models.CharField(
        "href",
        max_length=255,
        blank=True,
        help_text="The URL that this menu item points to",
    )
    label = models.CharField(
        "label", max_length=30, blank=True, help_text="The label of this menu item"
    )
    order = models.IntegerField(
        "order",
        help_text="The order that the item would appear in a menu",
    )

    def __str__(self):
        return self.label

    class Meta:
        ordering=("menu", "order")


class MenuPage(models.Model):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        help_text="The menu that is attached to this page",
    )
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        help_text="The page that this menu is attached to ",
    )

    def __str__(self):
        return '"{}" on page "{}"'.format(self.menu, self.page)


class Articlecomment(models.Model):
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField(max_length=80, help_text="Your name")
    email = models.EmailField(help_text="Your email")
    content = models.TextField()
    when = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["when"]

    def __str__(self):
        return "Comment {} by {}".format(self.content, self.name)
