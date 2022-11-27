# The Invidious documentation

# Running the documentation locally for development purposes

## Local `mkdocs-material` installation

```bash
# You might want to create a virtualenv first
pip install mkdocs-material
mkdocs-material serve
```

## With docker

```bash
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material:latest
```
