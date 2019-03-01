##### GET `/api/v1/videos/:id`

> Schema:

```javascript
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
  "published": Int64,
  "publishedText": String,

  "keywords": Array(String),
  "viewCount": Int64,
  "likeCount": Int32,
  "dislikeCount": Int32,

  "paid": Bool,
  "premium": Bool,
  "isFamilyFriendly": Bool,
  "allowedRegions": Array(String),
  "genre": String,
  "genreUrl": String,

  "author": String,
  "authorId": String,
  "authorUrl": String,
  "authorThumbnails": [
    {
      "url": String,
      "width": Int32,
      "height": Int32
    }
  ],

  "subCountText": String,
  "lengthSeconds": Int32,
  "allowRatings": Bool,
  "rating": Float32,
  "isListed": Bool?,

  "hlsUrl": String?,
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
      "languageCode": String,
      "url": String,
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

Parameters:

```
region: ISO 3166 country code (default: "US")
```

##### GET `/api/v1/comments/:id`

> Schema:

```javascript
{
  "commentCount": Int32?,
  "videoId": String,
  "comments": [
    {
      "author": String,
      "authorThumbnails": [
        "url": String,
        "width": Int32,
        "height": Int32
      ],
      "authorId": String,
      "authorUrl": String,
      "isEdited": Bool,
      "content": String,
      "contentHtml": String,
      "published": Int64,
      "publishedText": String,
      "likeCount": Int32,
      "commentId": String,
      "authorIsChannelOwner": Bool,
      "creatorHeart": {
        "creatorThumbnail": String,
        "creatorName": String
      }?,
      "replies": {
        "replyCount": Int32,
        "continuation": String
      }?
    }
  ],
  "continuation": String?
}
```

Parameters:

```
source: "youtube", "reddit"
continuation: String
```

##### GET `/api/v1/insights/:id`

**Will always return 503: `YouTube has removed publicly-available analytics`***

> Schema:

```javascript
{
    "viewCount": Int64,
    "timeWatchedText": String,
    "subscriptionsDriven": Int32,
    "shares": Int32,
    "avgViewDurationSeconds": Int32,

    "graphData": {
        ...
    }
}
```

##### GET `/api/v1/captions/:id`

> Schema:

```javascript
{
  "captions": [
    {
      "label": String,
      "languageCode": String,
      "url": String
    }
  ]
}
```

Parameters:

```
label: String
lang:  String
tlang: String
region: ISO 3166 country code (default: "US")
```

A request with `label` will return the selected captions in WebVTT format.
Captions can also be selected with an ISO `lang`, e.g. &lang=en, `tlang` will auto-translate from English into the requested language (if English captions are available).

##### GET `/api/v1/trending`

> Schema:

```
[
  {
    "title": String,
    "videoId": String,
    "videoThumbnails": [
      {
        "quality": String,
        "url": String,
        "width": Int32,
        "height" Int32
    ],

    "lengthSeconds": Int32,
    "viewCount": Int64,

    "author": String,
    "authorId": String,
    "authorUrl": String,

    "published": Int64,
    "publishedText": String,
    "description": String,
    "descriptionHtml": String,

    "liveNow": Bool,
    "paid": Bool,
    "premium": Bool
  }
]
```

Parameters:

```
type: "music", "gaming", "news", "movies"
region: ISO 3166 country code (default: "US")
```

##### GET `/api/v1/top`

> Schema:

```
[
  {
    "title": String,
    "videoId": String,
    "videoThumbnails": [
      {
        "quality": String,
        "url": String,
        "width": Int32,
        "height" Int32
    ],

    "lengthSeconds": Int32,
    "viewCount": Int64,

    "author": String,
    "authorId": String,
    "authorUrl": String,

    "published": Int64,
    "publishedText": String,
    "description": String,
    "descriptionHtml": String
  }
]
```

##### GET `/api/v1/channels/:ucid`

> Schema:

```
{
  "author": String,
  "authorId": String,
  "authorUrl": String,
  "authorBanners": [
    {
      "url": String,
      "width": Int32,
      "height": Int32
    }
  ],
  "authorThumbnails": [
    {
      "url": String,
      "width": Int32,
      "height": Int32
    }
  ],

  "subCount": Int32,
  "totalViews": Int64,
  "joined": Int64,

  "paid": Bool,
  "autoGenerated": Bool,
  "isFamilyFriendly": Bool,
  "description": String,
  "descriptionHtml": String,
  "allowedRegions": Array(String),

  "latestVideos": [
    {
      "title": String,
      "videoId": String,
      "author": String,
      "authorId": String,
      "authorUrl": String,

      "videoThumbnails": [
        {
          "quality": String,
          "url": String,
          "width": Int32,
          "height": Int32
        }
      ],
      "description": String,
      "descriptionHtml": String,
      "viewCount": Int64,
      "published": Int64,
      "publishedText": String,
      "lengthSeconds": Int32,
      "paid": Bool,
      "premium": Bool
    }
  ],
  "relatedChannels": [
    {
      "author": String,
      "authorId": String,
      "authorUrl": String,
      "authorThumbnails": [
        {
          "url": String,
          "width": Int32,
          "height": Int32
        }
      ]
    }
  ]
}
```

Parameters:

```
sort_by: "newest", "oldest", "popular" (default: newest)
```

Note that a channel's username (if it doesn't include spaces) is also valid in place of `ucid`, e.g. `/api/v1/channels/BlenderFoundation`.

##### GET `/api/v1/channels/:ucid/videos`, `/api/v1/channels/videos/:ucid`

> Schema:

```javascript
[
  {
    title: String,
    videoId: String,
    author: String,
    authorId: String,
    authorUrl: String,

    videoThumbnails: [
      {
        quality: String,
        url: String,
        width: Int32,
        height: Int32
      }
    ],
    description: String,
    descriptionHtml: String,

    viewCount: Int64,
    published: Int64,
    publishedText: String,
    lengthSeconds: Int32
    paid: Bool,
    premium: Bool
  }
]
```

Parameters:

```
page: Int32
sort_by: "newest", "oldest", "popular" (default: newest)
```

##### GET `/api/v1/channels/:ucid/latest`, `/api/v1/channels/latest/:ucid`

```javascript
[
  {
    title: String,
    videoId: String,
    authorId: String,
    authorUrl: String,

    videoThumbnails: [
      {
        quality: String,
        url: String,
        width: Int32,
        height: Int32
      }
    ],
    description: String,
    descriptionHtml: String,

    viewCount: Int64,
    published: Int64,
    publishedText: String,
    lengthSeconds: Int32
    paid: Bool,
    premium: Bool
  }
]
```

##### GET `/api/v1/channels/playlists/:ucid`, `/api/v1/channels/:ucid/playlists`

```javascript
{
  "playlists": [
    {
      "title": String,
      "playlistId": String,
      "author": String,
      "authorId": String,
      "authorUrl": String,
      "videoCount": Int32,
      "videos": [
        {
          "title": String,
          "videoId": String,
          "lengthSeconds": Int32,
          "videoThumbnails": [
            {
              "quality": String,
              "url": String,
              "width": Int32,
              "height": Int32
            }
          ]
        }
      ]
  ],
  "continuation": String?
}
```

##### GET `/api/v1/channels/search/:ucid`

> Schema:

```javascript
[
  {
    type: "video",
    title: String,
    videoId: String,
    author: String,
    authorId: String,
    authorUrl: String,
    videoThumbnails: [
      {
        quality: String,
        url: String,
        width: Int32,
        height: Int32
      }
    ],
    description: String,
    descriptionHtml: String,
    viewCount: Int64,
    published: Int64,
    publishedText: String,
    lengthSeconds: Int32,
    liveNow: Bool,
    paid: Bool,
    premium: Bool
  },
  {
    type: "playlist",
    title: String,
    playlistId: String,
    author: String,
    authorId: String,
    authorUrl: String,

    videoCount: Int32,
    videos: [
      {
        "title": String,
        "videoId": String,
        "lengthSeconds": Int32,
        "videoThumbnails": [
          {
            quality: String,
            url: String,
            width: Int32,
            height: Int32
          }
        ]
      }
    ]
  },
  {
    type: "channel",
    author: String,
    authorId: String,
    authorUrl: String,

    authorThumbnails: [
      {
        url: String,
        width: Int32,
        height: Int32
      }
    ],
    subCount: Int32,
    videoCount: Int32,
    description: String,
    descriptionHtml: String
  }
];
```

Parameters:

```
q: String
page: Int32
```

##### GET `/api/v1/search`

> Schema:

```javascript
[
  {
    type: "video",
    title: String,
    videoId: String,
    author: String,
    authorId: String,
    authorUrl: String,
    videoThumbnails: [
      {
        quality: String,
        url: String,
        width: Int32,
        height: Int32
      }
    ],
    description: String,
    descriptionHtml: String,
    viewCount: Int64,
    published: Int64,
    publishedText: String,
    lengthSeconds: Int32,
    liveNow: Bool,
    paid: Bool,
    premium: Bool
  },
  {
    type: "playlist",
    title: String,
    playlistId: String,
    author: String,
    authorId: String,
    authorUrl: String,

    videoCount: Int32,
    videos: [
      {
        "title": String,
        "videoId": String,
        "lengthSeconds": Int32,
        "videoThumbnails": [
          {
            quality: String,
            url: String,
            width: Int32,
            height: Int32
          }
        ]
      }
    ]
  },
  {
    type: "channel",
    author: String,
    authorId: String,
    authorUrl: String,

    authorThumbnails: [
      {
        url: String,
        width: Int32,
        height: Int32
      }
    ],
    subCount: Int32,
    videoCount: Int32,
    description: String,
    descriptionHtml: String
  }
];
```

Parameters:

```
q: String
page: Int32
sort_by: "relevance", "rating", "upload_date", "view_count"
date: "hour", "today", "week", "month", "year"
duration: "short", "long"
type: "video", "playlist", "channel", "all", (default: video)
features: "hd", "subtitles", "creative_commons", "3d", "live", "purchased", "4k", "360", "location", "hdr" (comma separated: e.g. "&features=hd,subtitles,3d,live")
region: ISO 3166 country code (default: "US")
```

##### GET `/api/v1/playlists/:plid`

> Schema:

```javascript
{
    "title": String,
    "playlistId": String,

    "author": String,
    "authorId": String,
    "authorThumbnails": [
        {
            "url": String,
            "width": String,
            "height": String
        }
    ],
    "description": String,
    "descriptionHtml": String,

    "videoCount": Int32,
    "viewCount": Int64,
    "updated": Int64,

    "videos": [
        {
          "title": String,
          "videoId": String,
          "author": String,
          "authorId": String,
          "authorUrl": String,
  
          "videoThumbnails": [
              {
                  "quality": String,
                  "url": String,
                  "width": Int32,
                  "height": Int32
              }
          ],
          "index": Int32,
          "lengthSeconds": Int32
        }
    ]
}
```

Parameters:

```
page: Int32
```

##### GET `/api/v1/mixes/:rdid`

> Schema:

```javascript
{
  title: String,
  mixId: String,
  videos: [
    {
      title: String,
      videoId: String,
      author: String,
      authorId: String,
      authorUrl: String,
      videoThumbnails: [
        {
          quality: String,
          url: String,
          width: Int32,
          height: Int32
        }
      ],
      index: Int32,
      lengthSeconds: Int32
    }
  ]
}
```
