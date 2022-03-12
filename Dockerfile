FROM squidfunk/mkdocs-material:latest as build
WORKDIR /build
COPY . .
RUN mkdocs build

FROM docker.io/library/nginx:alpine
COPY --from=build /build/site/ /usr/share/nginx/html/
