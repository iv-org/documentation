# Search filters

Invidious supports the various search filters provided by YouTube.

Support for more user-friendly search is planned, see [#179](https://github.com/iv-org/invidious/issues/179).

Search filters are currently implemented as `key:value` operators, similar to [DuckDuckGo](https://help.duckduckgo.com/duckduckgo-help-pages/results/syntax/) and other search engines. Operators can be added to the search query to filter results, for example: [`type:playlist sort:views music`](https://invidio.us/search?q=type%3Aplaylist+sort%3Adate+music).

When using `subscriptions:true` or `channel:UCxxx` other filters are not applied.

Supported operators:

- `sort:`
  - `relevance` (default)
  - `rating`
  - `upload_date`, `date`
  - `view_count`, `views`
- `date:`
  - `hour`
  - `today`
  - `week`
  - `month`
  - `year`
- `type:`
  - `all` (default)
  - `video`
  - `channel`
  - `playlist`
  - `movie`
  - `show`
- `duration:`
  - `short`
  - `long`
- `features:` Multiple can be specified, for example `features:live,4k,subtitles`
  - `hd`
  - `subtitles`
  - `creative_commons`,`cc`
  - `live`, `livestream`
  - `purchased`
  - `4k`
  - `360`
  - `location`
  - `hdr`
- `channel:`, `user:`
  - `UCxxxxxxxxxxxxxxxxxxxxxx`
  - `author` Can be ambiguous, so using `UCID` is recommended
- `subscriptions:` If logged in, search only for videos from subscribed channels
  - `true`
  - `false`
