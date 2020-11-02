## oEmbed Endpoint for embedding Jovian Notebooks

oEmbed is an open standard to easily embed content from oEmbed providers into your site. You can use the oEmbed standard for embedding Jovian notebooks into your website, have a look at [oEmbed.com](https://oembed.com).

#### API Endpoint URL

You can use our API endpoint to request the embed code for public Notebooks, all responses are in json format. Replace {notebook-url} by your Jovian Notebook URL, or Jovian Viewer URL, or any raw `.ipynb` file URL:

- [GET][https://jovian.ai/api/oembed.json/?url={notebook-url}&maxwidth={max-width}](https://jovian.ai/api/oembed.json/?url=https://jvn.storage.googleapis.com/gists/aakashns/5bc23520933b4cc187cfe18e5dd7e2ed/raw/901a9d2508bd441dbf06954c5f46bf58/movielens-fastai.ipynb)

Parameters:

- **url** _(String, required)_: The URL of the notebook or Jovian Viewer URL.
- **cellId** _(Integer, optional)_: Index of the cell of the notebook for cell-level embeds. If no `cellId` id present, whole notebook gets embedded.
- **maxwidth** _(Integer, optional)_: The maximum width of the embedded resource (optional). Note that the maxheight parameter is not supported. This is because the embed code is responsive and its height varies depending on its width.

_Example URLs:_

- Jovian Notebook URLs
  - [Jovian Notebook](https://jovian.ai/aakashns/01-pytorch-basics)
  - [Jovian Notebook (Version specified)](https://jovian.ai/aakashns/movielens-fastai/v/14)
- Jovian Viewer URLs
  - [https://jovian.ai/viewer?url={notebook-url}](https://jovian.ai/viewer?url=https%3A%2F%2Fjvn.storage.googleapis.com%2Fgists%2Faakashns%2F5bc23520933b4cc187cfe18e5dd7e2ed%2Fraw%2F901a9d2508bd441dbf06954c5f46bf58%2Fmovielens-fastai.ipynb)
- [Raw `.ipynb` file URL](https://jvn.storage.googleapis.com/gists/aakashns/5bc23520933b4cc187cfe18e5dd7e2ed/raw/901a9d2508bd441dbf06954c5f46bf58/movielens-fastai.ipynb)

Response:

```json
{
  "title": "Jovian Viewer",
  "provider_name": "Jovian",
  "provider_url": "https://jovian.ai",
  "author_name": "Jovian ML",
  "version": "1.0",
  "type": "rich",
  "author_url": "https://github.com/JovianML",
  "height": 800,
  "width": 800,
  "html": "<iframe src='https://jovian.ai/embed?url=https%3A//jvn.storage.googleapis.com/gists/aakashns/5bc23520933b4cc187cfe18e5dd7e2ed/raw/901a9d2508bd441dbf06954c5f46bf58/movielens-fastai.ipynb' title='Jovian Viewer' height=800 width=800 frameborder=0 allowfullscreen></iframe>"
}
```

```eval_rst
.. meta::
   :description: Embed Jupyter notebooks to blogs and websites.
```
