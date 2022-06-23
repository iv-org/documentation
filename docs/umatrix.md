# How to deal with uMatrix

If you're using [uMatrix](https://github.com/gorhill/uMatrix), you won't be able to automatically play a video served by Invidious on other websites without unblocking requests to Invidious instances.

So, to make it work, you'll need to allow `css`, `image`, `media`, `script`, `xhr`, `frame` for the instance from which you're trying to play the video.

Since there are many Invidious instances, you can use the tool called [Invimatrix](https://booteille.codeberg.page/invimatrix/) to automatically generate uMatrix & uBlock Origin rules for every known instance.
