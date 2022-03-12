FROM squidfunk/mkdocs-material:latest as build
COPY . .
RUN build

FROM docker.io/library/nginx:alpine
COPY --from=build /site/ /usr/share/nginx/html/
