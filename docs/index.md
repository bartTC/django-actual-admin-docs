# django-actual-admin-docs

Render Markdown documentation directly in the Django admin `/admin/`.

- Support for nested subfolders
- Comprehensive Markdown format (link to which spec)
- Provides default styles for Markdown rendering

## Installation

1. `pip install django-actual-admin-docs`.
2. Add `actual_admin_docs` to your `INSTALLED_APPS` setting.
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

**See [Markdown Sample](markdown-sample.md) as an example**

You can use folders, subfolders, files in folders, etc.
You can use regular Markdown files and markup to write your documentation. 

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

Use regular Markdown links to link to other documents or objects.

```markdown
A link to another document [is a regular link](markdown-sample.md).
Documents in subdirectories [are supported too](./subdirectory/index.md).

For images, downloads etc. use regular markdown markup too:

![a red bird](./assets/image.jpg)

[Click to download](./subfolder/subfolder_in_a_subfolder/download.zip)
```

## Custom CSS

Overwrite the `actual-admin-docs.css` file to add your custom styles.