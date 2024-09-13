# Pyusite

## #To be discontinued in favor of wibekwa# ##

A Django app CMS.  As of 2024, this is a limited and clunky CMS which might be useful as a starting point or an example for someone who wants to build their own.  On the other hand, it might fit your needs as is.

Pyusite (which I pronounce like "Pius Site") is named from a mashup of "Python User's Site"  The previous name was "sdc_site", from the initials of a customer I was working for when I started on this project

## Description

* It's not a blog.  Instead of automatically placing your article in a timeline, you place it where you want

## Getting Started

### Dependencies

* Touglates: [https://github.com/tougshire/touglates](https://github.com/tougshire/touglates).
* Django Filters Stoex: [https://github.com/tougshire/django_filters_stoex](https://github.com/tougshire/django_filters_stoex)
* Django Filters: [https://pypi.org/project/django-filter/](https://pypi.org/project/django-filter/)
<!-- * Django C_KEditor 5: [https://pypi.org/project/django-c_keditor-5/](https://pypi.org/project/django-c_keditor-5/) -->
* Django Markdown: [https://pypi.org/project/django-markdown/](https://pypi.org/project/django-markdown/)
* This repository, pyusite: [https://github.com/tougshire/pyusite](https://github.com/tougshire/pyusite)

### Installing

* Start a Django Project
* From your projecdt root folder (the one with manage.py in it), clone Pyusite, Django Filters Stoex, and Touglates using git
* * ex: `git clone https://github.com/tougshire/pyusite`
* Install Django Filters with pip
<!-- * Install Django Filters and Django C_KEditor 5 with pip -->

### Configuring

<!-- Follow the examples in the documentation for Django Filters and Django C_KEDitor 5. You don't have to configure Django Markdown  -->
Follow the examples in the documentation for Django Filters.

Your installed apps should look something like:

```
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tougshire_auth.apps.TougshireAuthConfig",
    "touglates.apps.TouglatesConfig",
    "django_filters",
    "django_filters_stoex.apps.DjangoFiltersStoexConfig",
    <!-- "django_c_keditor_5", -->
    "pyusite.apps.PyusSiteConfig",
]
```
* Add configuration settings for pyusite.  Include the following code in your settings, and customize for your project:

```
PYUSITE_AVAILABLE = {
    "default": {
        "SITE_NAME": "Toughire Pyusite",
        "TEMPLATE_DIR": os.path.join("pyusite", "default", ""),
        "STATIC_DIR": os.path.join("pyusite", "default", ""),
        "BANNER_IMAGE": os.path.join("tougshire", "tougshire.banner.jpg"),
        "FOOTER_CONTENT": '<div class="footer" style="border:1px solid white; width:60%; margin:.5ex auto auto auto;"><br>Tougshire</div><br/> Suffolk, VA 23434',
        "COLORSCHEME": "green",
        "RECIPIENTS": ["tougshire@tougshire.com"],
        "head_lines": [
            '<!-- <a rel="me" href="https://assortedflotsam.com/@bnmng">Mastodon</a> -->'
        ],
        "keyed_head_lines": {
            "og_image": '<meta property="og:image" content="https://media.tougshire.com/tougshire/gallery/tougshireavatar.png" />',
            "og_image_alt": '<meta property="og:image:alt" content="The Tougshire Logo" />',
        },
    },
}

PYUSITE = PYUSITE_AVAILABLE["default"]

```
* add a path which includes "pyusite.urls", and another which includes "touglates.urls" to your project's urls.py
<!-- * add urls for c_keditor 5 -->

Example urls paths below.

```
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("site/", include("pyusite.urls")),
        path("touglates/", include("touglates.urls")),
        <!-- path(
            "c_keditor5/",
            include("django_c_keditor_5.urls"),
            name="c_k_editor_5_upload_file",
        ), -->
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
```

* Add `"pyusite.context_processors.pyusite"` to `TEMPLATES["OPTONS"]["context_processors"]`

example TEMPLATES:

```
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "pyusite.context_processors.pyusite",
            ],
        },
    },
]
```
## Help

This is still in early phases and much more has to be done.

## Author

benjamin at tougshire.com

