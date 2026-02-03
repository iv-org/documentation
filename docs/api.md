# API

### Language

All endpoints that return a JSON body support `&hl=LANGUAGE` for translating fields into the desired language. A list of languages are provided in [List of URL parameters](./url-parameters.md).

##### GET `/api/v1/stats`

> Schema:

```javascript
{
  "version": String,
  "software": {
    "name": "invidious",
    "version": String,
    "branch": String
  },
  "openRegistrations": Bool,
  "usage": {
    "users": {
      "total": Int32,
      "activeHalfyear": Int32,
      "activeMonth": Int32
    }
  },
  "metadata": {
    "updatedAt": Int64,
    "lastChannelRefreshedAt": Int64
  },
  "playback": {
    "totalRequests": Int32?
    "successfulRequests": Int32?
    "ratio": Float32?
  }
}
```

##### GET `/api/v1/videos/:id`

> Schema:

```javascript
{
  "type": String, // "video"|"published"
  "title": String,
  "videoId": String,
  "videoThumbnails": [
    {
      "quality": String,
      "url": String,
      "width": Int32,
      "height": Int32
    }
  ],
  "storyboards": [
    {
      "url": String,
      "templateUrl": String,
      "width": Int32,
      "height": Int32,
      "count": Int32,
      "interval	": Int32,
      "storyboardWidth": Int32,
      "storyboardHeight": Int32,
      "storyboardCount": Int32
    }
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
  "isListed": Bool,
  "liveNow": Bool,
  "isPostLiveDvr": Bool,
  "isUpcoming": Bool,
  "dashUrl:" String,
  "premiereTimestamp": Int64?,

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
      "projectionType": String,
      "container": String,
      "encoding": String,
      "qualityLabel": String?,
      "resolution": String?,
      "fps": Int32,
      "size": String?,
      "targetDurationsec": Int64?,
      "maxDvrDurationSec": Int64?,
      "audioQuality": String?,
      "audioSampleRate": String?,
      "audioChannels": String?,
      "colorInfo": String?,
      "captionTrack": String?
    }
  ],
  "formatStreams": [
    {
      "url": String,
      "itag": String,
      "type": String,
      "quality": String,
      "bitrate": String?,
      "container": String,
      "encoding": String,
      "qualityLabel": String,
      "resolution": String,
      "size": String
    }
  ],
  "captions": [
    {
      "label": String,
      "language_code": String,
      "url": String
    }
  ],
  "musicTracks": [
    {
      "song": String,
      "artist": String,
      "album": String,
      "license": String
    }
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
        }
      ],
      "author": String,
      "authorUrl": String,
      "authorId": String?,
      "authorVerified": Boolean,
      "authorThumbnails": [
        {
          "url": string,
          "width": Int32,
          "height": Int32
        }
      ],
      "lengthSeconds": Int32,
      "viewCount": 
      "viewCountText": String
    }
  ]
}
```

Parameters:

```
region: ISO 3166 country code (default: "US")
```

##### GET `/api/v1/annotations/:id`

Parameters:

```
source: "archive", "youtube" (default: "archive")
```

Returns annotation XML from YouTube's `/annotations_invideo` endpoint. Alternatively it provides access to legacy annotation data using [this collection](https://archive.org/details/youtubeannotations) on archive.org.

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
        {
          "url": String,
          "width": Int32,
          "height": Int32
        }
      ],
      "authorId": String,
      "authorUrl": String,

      "isEdited": Boolean,
      "isPinned": Boolean,
      "isSponsor": Boolean?,
      "sponsorIconUrl": String?,

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
sort_by: "top", "new" (default: top)
source: "youtube", "reddit" (default: youtube)
continuation: String
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

```javascript
[
  {
    "title": String,
    "videoId": String,
    "videoThumbnails": [
      {
        "quality": String,
        "url": String,
        "width": Int32,
        "height": Int32
      }
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
type: "music", "gaming", "movies", "default"
region: ISO 3166 country code (default: "US")
```

##### GET `/api/v1/popular`

> Schema:

```javascript
[
    {
        "type": "shortVideo",
        "title": String,
        "videoId": String,
        "videoThumbnails": [
            {
            "quality": String,
            "url": String,
            "width": Int32,
            "height": Int32
            }
        ],

        "lengthSeconds": Int32,
        "viewCount": Int64,

        "author": String,
        "authorId": String,
        "authorUrl": String,

        "published": Int64,
        "publishedText": String
    }
]
```

##### GET `/api/v1/search/suggestions`

> Schema:

```javascript
{
    "query": String,
    "suggestions": Array(String)
}
```

Parameters:

```
q: String
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
    playlistThumbnail: String,
    author: String,
    authorId: String,
    authorUrl: String,
    authorVerified: Boolean,

    videoCount: Int32,
    videos: [
      {
        title: String,
        videoId: String,
        lengthSeconds: Int32,
        videoThumbnails: [
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
    autoGenerated: Bool
    subCount: Int32,
    videoCount: Int32,
    description: String,
    descriptionHtml: String
  },
  {
    type: "hashtag"
    title: String,
    url: String,
    channelCount: Int32,
    videoCount: Int32
  }
];
```

Parameters:

```
q: String
page: Int32
sort: "relevance", "rating", "date", "views"
date: "hour", "today", "week", "month", "year"
duration: "short", "long", "medium"
type: "video", "playlist", "channel", "movie", "show", "all", (default: all)
features: "hd", "subtitles", "creative_commons", "3d", "live", "purchased", "4k", "360", "location", "hdr", "vr180" (comma separated: e.g. "&features=hd,subtitles,3d,live")
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
    "viewCountText": String,
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

##### GET `/api/v1/hashtag/:tag`
> Schema:
```javascript
{
  results: VideoObject[],
}
```
Parameters:
```
page: Int32
```

##### GET `/api/v1/resolveurl`
> Schema:
```javascript
{
  browseId?: String,
  ucid?: String,
  videoId?: String,
  playlistId?: String,
  startTimeSeconds?: String,
  postId?: String,
  params?: String,
  pageType: string
}
```
Parameters:
```
url: URL
```

##### GET `/api/v1/clips`
> Schema:
```javascript
{
  startTime: Float64, // in seconds
  endTime: Float64, // in seconds
  clipTitle: String,
  video: VideoObject
}
```
Parameters:
```
id: string
```