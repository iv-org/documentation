# Attachment Types for community posts

Please refer to the [Common object types](./common_types.md) page for more details on the various JSON objects used below.


### Video
See [VideoObject](./common_types.md#videoobject) common type

### Image

```javascript
{
    type: "image".
    imageThumbnails: ImageObject[]
}
```

### MultiImage

```javascript
{
    type: "multiImage",
    images: [
        ImageObject[]
    ]
}
```

### Unknown

This usually means that parsing support for the attachment has not yet been implemented.

```javascript
{
    type: "unknown",
    error: String
}
```