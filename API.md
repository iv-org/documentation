GET `/api/v1/videos/:id`
> Given `:id`, return `video`  
> `Video schema`:  
```
{
  "title": String,
  "videoId": String,
  "videoThumbnails": [
    {    
      "quality": String,
      "url": String,
      "width": Int32,
      "height": Int32
    },
  ],

  "description": String,
  "descriptionHtml": String,
  "published": Int64
  
  "keywords": Array(String),
  "viewCount": Int64,
  "likeCount": Int32,
  "dislikeCount": Int32,
  
  "isFamilyFriendly": Bool,
  "allowedRegions": Array(String),
  "genre": String,
 
  "author": String,
  "authorId": String,
  "authorUrl": String,

  "lengthSeconds": Int32,
  "allowRatings": Bool,
  "rating": Float32,
  "isListed": Bool,

  "adaptiveFormats": [
    {
      "index": String,
      "bitrate": String,
      "init": String,
      "url": String,
      "itag": String,
      "type": String,
      "clen": String,
      "lmt": String,
      "projectionType": Int32,
      "container": String,
      "encoding": String,
      "qualityLabel": String?,
      "resolution": String?
    },
  ],
  "formatStreams": [
    {
      "url": String,
      "itag": String,
      "type": String,
      "quality": String,
      "container": String,
      "encoding": String,
      "qualityLabel": String,
      "resolution": String,
      "size": String
    }, 
  ],
  "captions": [
    {
      "label": String,
      "languageCode": String
    },
  ],
  "recommendedVideos": [
    {
      "videoId": String,
      "title": String,
      "videoThumbnails": [
        {
          "quality": String,
          "url": String,
          "width": Int32,
          "height": Int32
        },
      ],
      "author": String,
      "lengthSeconds": Int32,
      "viewCountText" String
    }
  ]
}
```

GET `/api/v1/trending`

GET `/api/v1/top`

GET `/api/v1/channels/:ucid`

GET `/api/v1/channels/:ucid/videos`

GET `/api/v1/search`
