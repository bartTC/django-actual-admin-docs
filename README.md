# django-actual-admin-docs

Render Markdown documentation directly in the Django admin `/admin/`.

- Support for nested subfolders
- Comprehensive Markdown format 
- Provides default styles for Markdown rendering

See [this screenshot](https://raw.githubusercontent.com/bartTC/django-actual-admin-docs/refs/heads/main/docs/example.png) of an example page.

## Installation

1. `pip install django-actual-admin-docs`.
2. Add `actual_admin_docs` to your `INSTALLED_APPS` setting.
3. Add the documentation urlpattern, above your admin urls:

   ```py
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

You can use regular folders, subfolders, images, files, etc. You can use regular Markdown files and markup to write your documentation and link between documents. 

```
🗂 docs/
│
├── 🗂 subfolder           
│   ├── 🗂 subfolder_in_a_subfolder
│   │   ├── 📦 download.zip
│   │   └── 📝 index.md
│   │ 
│   ├── 📝 another_file.md
│   └── 📝 index.md
│
├── 🗂 assets    
│   ├── 🌁 image.jpg
│   └── 🌁 other-image.jpg
│
└── 📝 index.md
```

### Markup

```markdown
A link to another document [is a regular link](markdown-sample.md).
Documents in subdirectories [are supported too](./subdirectory/index.md).

For images, downloads etc. use regular markdown markup too:

![a red bird](./assets/image.jpg)

[Click to download](./subfolder/subfolder_in_a_subfolder/download.zip)
```

## Custom CSS

Overwrite the `actual-admin-docs.css` file to set your custom styles.