# The Invidious documentation

## Running the documentation locally for development purposes

Run those commands in the repository's folder.

### Local `mkdocs-material` installation

```bash
# You might want to create a virtualenv first
pip install mkdocs-material
# If you want to browse a static copy
mkdocs build
python -m http.server -d site/
xdg-open http://0.0.0.0:8000
# If you want to reload changes after editing
mkdocs serve
xdg-open http://127.0.0.1:8000/
```

### With docker

```bash
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material:latest
```
