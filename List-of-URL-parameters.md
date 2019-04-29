A list of URL parameters for Invidious, which can automatically toggle various UI and video settings.

Supported player parameters are listed [here](https://github.com/omarroth/invidious/blob/8c2958b86d0952c176c1df83f2cbaa9adce5e59f/src/invidious/videos.cr#L1200-L1211).

_This list is incomplete. You can help by expanding it._

| Parameter      | Setting                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| _UI Language_  | Reflects locales listed [here](https://github.com/omarroth/invidious/blob/8c2958b86d0952c176c1df83f2cbaa9adce5e59f/src/invidious.cr#L62-L74) |
| `hl=ar`        | Arabic                                                                                                                                           |
| `hl=de`        | German                                                                                                                                           |
| `hl=en-US`     | English                                                                                                                                          |
| `hl=eo`        | Esperanto                                                                                                                                        |
| `hl=es`        | Spanish                                                                                                                                          |
| `hl=eu`        | Basque                                                                                                                                           |
| `hl=fr`        | French                                                                                                                                           |
| `hl=it`        | Italian                                                                                                                                          |
| `hl=nb_NO`     | Norwegian Bokmål                                                                                                                                 |
| `hl=nl`        | Dutch                                                                                                                                            |
| `hl=pl`        | Polish                                                                                                                                           |
| `hl=ru`        | Russian                                                                                                                                          |
| `hl=uk`        | Ukranian                                                                                                                                         |
| _Autoplay_     |
|
| `autoplay=1`   | Video loads and starts playback automatically
|
| `autoplay=0`   | Disabled
|
| _Continue_     |
|
| `continue=1`   | When video is done, automatically go to the next related video (similar to YouTube’s _Autoplay_ feature)
|
| `continue=0`   | Disabled
|
| _Quality_      |                                                                                                                                                  |
| `quality=dash` | [DASH](https://en.wikipedia.org/wiki/Dynamic_Adaptive_Streaming_over_HTTP)                                                                       |
| _Subtitles_    | List of ISO 639-1 language codes (comma-separated)                                                                                               |
| `subtitles=en` | English (will use `auto-generated` if native translation is unavailable)                                                                         |
