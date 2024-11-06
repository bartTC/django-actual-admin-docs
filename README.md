# django-actual-admin-docs

Render Markdown documentation directly in the Django admin`.

- Support for nested subfolders
- Comprehensive Markdown format (link to which spec)
- Provides default styles for Markdown rendering

## Installation

1. Install the `django-actual-admin-docs` package:

   - `pip install django-actual-admin-docs[highlight]` if you want to enable syntax highlighting in code blocks. This adds [Pygments](https://pygments.org) as a dependency.

   - `pip install django-actual-admin-docs` if you don't need that and want to keep your third party dependencies lean.

2. Add `actual_admin_docs` to your `INSTALLED_APPS` setting:

   ```python 
   INSTALLED_APPS = [
     "django.contrib.admin",
     "actual_admin_docs",
     ...
   ]
   ```
   
3. Add the documentation urlpattern, above your admin urls:

   ```python
   from django.contrib import admin
   from django.urls import include, path
   
   urlpatterns = [
       path("admin/docs/", include("actual_admin_docs.urls")),
       path("admin/", admin.site.urls),
   ]
   ```
4. Add a `DOCS_ROOT` setting which should be a `pathlib.Path` pointing to the docs directory:

   ```python 
   DOCS_ROOT = BASE_DIR / "docs"
   ```

## Documentation folder structure

You can use folders, subfolders, files in folders, etc.

```
🗂 docs/
│
├── 🗂 subfolder   
│   │   
│   ├── 🗂 subfolder with spaces
│   │   └── 📝 another-file.md
│   │ 
│   ├── 📝 another-file.md
│   └── 📝 index.md
│
├── 🗂 img    
│   └── 🌁 cat_studying_glasses.jpg
│
├── 📝 index.md
└── 📝 markdown-sample.md
```

Use regular Markdown links to link to other documents or objects:

```markdown
A link to [another document](./markdown-sample.md) is just a regular Markdown link. Documents in subdirectories [are supported too](./subfolder/another-file.md).

For images, downloads etc. use regular markdown markup too:

![A cat judging your code](./img/cat_studying_glasses.jpg)
[Click to download](./img/./img/cat_studying_glasses.jpg)
```

## Custom CSS

Overwrite the `actual-admin-docs.css` file to add your custom styles.


-----

# 🤺 Local Development

```bash
$ poetry install
$ poetry run pytest
$ DJANGO_SETTINGS_MODULE=actual_admin_docs.tests.testproject.settings poetry run django-admin runserver
```