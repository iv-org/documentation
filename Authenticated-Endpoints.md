All endpoints under namespace `/api/v1/auth` require authentication.

Authentication can be in one of two forms:

- A `Cookie: <SID>` header (for logged in users)
- An `Authentication: Bearer <TOKEN>` (recommended)

A new token can be generated from `/authorize_token` with the given parameters:

```
scopes: Comma-separated list of scopes
callback_url: URL to redirect to with generated token
expire: Int64 how long a given token should be valid (in seconds)
```

Each `scope` has the following format:

```
METHOD1;METHOD2...:ENDPOINT(*)?
```

Where `METHOD` can be one of `GET`, `POST`, `PUT`, `DELETE`, `PATCH`.

An `ENDPOINT` can be any of the documented endpoints below.

Examples:

- `POST:playlists*`: authorizes `POST` methods to _any_ endpoint under `/api/v1/auth/playlists` (`/api/v1/auth/playlists`, `/api/v1/playlists/:id/videos`, etc.)

- `:playlists/*`: authorizes \_any method to endpoints under `/api/v1/auth/playlists/` (`/api/v1/auth/playlists/:id`, `/api/v1/playlists/:id/videos`, etc.)

- `GET:playlists/IVPAAAAAAA`: authorizes `GET` only to playlist `IVPAAAAAA`.

- `:preferences`: authorizes _any_ method to `/api/v1/auth/preferences`

- `GET;POST:preferences`: authorizes `GET` or `POST` to `/api/v1/auth/preferences`

When a `callback_url` is specified, after a user has authorized a token with the desired `scopes`, a GET request will be made to the `callback_url` with the token URL-escaped and appended as `token=TOKEN`.

##### GET `/api/v1/auth/feed`

Get subscription feed for the authenticated user.

Parameters:

```
max_results: Int32
page: Int32
```

> Schema:

```javascript
{
    "notifications": [
        {
            "type": "shortVideo",
            "title": String,
            "videoId": String,
            "videoThumbnails": [
                {
                    "quality": String,
                    "url": String,
                    "width": Int64,
                    "height": Int64
                }
            ],
            "lengthSeconds": Int64,
            "author": String,
            "authorId": String,
            "authorUrl": String,
            "published": Int64,
            "publishedText": String,
            "viewCount": Int64
        }
    ],
    "videos": [
        {
            "type": "shortVideo",
            "title": String,
            "videoId": String,
            "videoThumbnails": [
                {
                    "quality": String,
                    "url": String,
                    "width": Int64,
                    "height": Int64
                }
            ],
            "lengthSeconds": Int64,
            "author": String,
            "authorId": String,
            "authorUrl": String,
            "published": Int64,
            "publishedText": String,
            "viewCount": Int64
        }
    ]
}
```

##### GET `/api/v1/auth/notifications`

Parameters:

```
topics: Array(String) (comma separated: e.g. "UCID1,UCID2) limit of 1000 topics
since: Int64, timestamp
```

Provides an [EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) for receiving changes from each `topic` in `topics`. Currently the only supported topic-type is `ucid`, which will return an updated video object whenever the given channel uploads a video.

Important to note is that an event will also be sent when a channel _changes_ an already uploaded video, for example changing description or title.

Each event is a JSON object with the same schema as `/api/v1/videos`. The `fields` API can be used, which will be applied to each object.

A `debug` topic can also provided which will return a (psuedo-)randomly selected video every minute.

`since` will return all videos uploaded since `TIMESTAMP`, with a limit of the 15 most recent videos from each topic.

More details in [#469](https://github.com/omarroth/invidious/issues/469).

##### POST `/api/v1/auth/notifications`

Same as above `GET` endpoint, however `topics` is moved into post body as `Content-Type: application/x-www-form-urlencoded`.

##### GET `/api/v1/auth/playlists`

Get list of playlists for the given user.

> Schema:

```javascript
[
    {
        "type": "invidiousPlaylist",
        "title": String,
        "playlistId": String,
        "author": String,
        "authorId": null,
        "authorUrl": null,
        "authorThumbnails": [],
        "description": String,
        "descriptionHtml": String,
        "videoCount": Int32,
        "viewCount": 0,
        "updated": Int64,
        "isListed": Boolean,
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
                "indexId": String,
                "lengthSeconds": Int32
            }
        ]
    }
]
```

##### POST `/api/v1/auth/playlists`

`Content-Type: application/json`

Create new playlist.

Example request body:

```javascript
{
    "title": String,
    "privacy": "private"
}
```

`privacy` can be any of: `public`, `unlisted`, `private`

If successful, returns 201, a link to the created resource as a `Location` header, and the following response:

```javascript
{
    "title": String,
    "playlistId": String
}
```

##### GET `/api/v1/auth/playlists/:id`

Returns same result as unauthenticated `/api/v1/playlists/:id`.

Important to note is that if the requested playlist is marked as `private`, it will return an error if the request is not authenticated as the playlist's author.

##### PATCH `/api/v1/auth/playlists/:id`

`Content-Type: application/json`

Modify a playlist's `description`, `title`, `description`, or `privacy`.

Example request body:

```javascript
{
    "title": String,
    "description": String,
    "privacy": "private"
}
```

`privacy` can be any of: `public`, `unlisted`, `private`

Will return 204 on success.

##### DELETE `/api/v1/auth/playlists/:id`

Delete a given playlist `:id`.

Will return 204 on success.

##### POST `/api/v1/auth/playlists/:id/videos`

`Content-Type: application/json`

Add a video to the given playlist `:id`.

Example request body:

```javascript
{
    "videoId": String
}
```

Returns a 201 on success with the following schema:

```javascript
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
    ]
}
```

##### DELETE `/api/v1/auth/playlists/:id/videos/:index`

Delete a video from the given playlist `:id` with `indexId` `:index`.

Will return 204 on success.

##### GET `/api/v1/auth/preferences`

Get preferences for authenticated user.

> Schema:

```javascript
{
    "annotations": false,
    "annotations_subscribed": false,
    "autoplay": false,
    "captions": [
        "",
        "",
        ""
    ],
    "comments": [
        "youtube",
        ""
    ],
    "continue": false,
    "continue_autoplay": true,
    "dark_mode": "light",
    "latest_only": false,
    "listen": false,
    "local": false,
    "locale": "en-US",
    "max_results": 40,
    "notifications_only": false,
    "player_style": "invidious",
    "quality": "hd720",
    "default_home": "Popular",
    "feed_menu": [
        "Trending",
        "Playlists"
    ],
    "related_videos": true,
    "sort": "published",
    "speed": 1.0,
    "thin_mode": false,
    "unseen_only": false,
    "video_loop": false,
    "volume": 100
}
```

##### POST `/api/v1/auth/preferences`

`Content-Type: application/json`

Patch user preferences.

Example body:

```javascript
{
    "speed": 2.0,
    "volume": 10
}
```

##### GET `/api/v1/auth/subscriptions`

Get user's subscriptions.

> Schema:

```javascript
[
    {
        "author": String,
        "authorId": String
    }
]
```

##### POST `/api/v1/auth/subscriptions/:ucid`

`Content-Type: application/json`

Add a given `ucid` to a user's subscriptions.

Will return 204 on success.

##### DELETE `/api/v1/auth/subscriptions/:ucid`

Removes a given `ucid` from a user's subscriptions.

Will return 204 on success.

##### GET `/api/v1/auth/tokens`

Get a list of tokens for the authenticated user.

> Schema:

```javascript
[
    {
        "session": String,
        "issued": Int64
    }
]
```

##### POST `/api/v1/auth/tokens/register`

`Content-Type: application/json`

Create a new token for the authenticated user.

Example request body:

```javascript
{
    "scopes": Array(String), // Each scope has same format as each scope in `/authorize_token`
    "callbackUrl": String?,
    "expire": Int64
}
```

Returns a 200 on success with the newly created token as the response body.

Example response:

```javascript
{
    "session":"v1:YUwKEL1XwHQzp7-AAAAAAAAAAAAAAAAAA=",
    "scopes":["GET:notifications"],
    "signature":"jNYdAAAAAAAAAAAAAAAAAAAAAAAAAAAAVAXGb__2Gv-w="
}
```

##### POST `/api/v1/auth/tokens/unregister`

`Content-Type: application/json`

Revoke a token for the authenticated user.

Example request:

```javascript
{
    "session": "v1:YUwKEL1XwHQzp7-AAAAAAAAAAAAAAAAAA="
}
```

Returns 204 on success.
