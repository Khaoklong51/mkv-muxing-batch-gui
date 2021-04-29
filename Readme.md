# MKV Muxing Batch GUI

App for muxing(merging) videos with [subtitles,chapters,attachments] with many options.<br>
### App Preview
https://user-images.githubusercontent.com/52576632/116090926-0944f800-a6ad-11eb-8fc4-4732588ca00e.mp4

### Subtitles Options
>1. Add new subtitle to each video file
>1. Subtitles names **don't have to match** videos names
>1. You can reorder the subtitles so that each subtitle is matched with the right video
>1. You can set subtitles to be default/forced
>1. You can set subtitle delay, track name, language
### Chapters Options
>1. add new chapter to each video file
>1. Chapters names **don't have to match** videos names
>1. You can reorder the chapters so that each chapter is matched with the right video
## Attachments Options
>1. Add new attachments to all video files 
>1. You can discard old attachments files from all videos 
## Source Files Options [Only Works for MKV files]
>1. You can discard old subtitles  
>1. You can keep subtitles with specific language(s) and/or track id(s) and discard any other subtitle
>1. You can discard old audios  
>1. You can keep audios with specific language(s) or track id(s) and discard any other audio
>1. You can set an old subtitle track to be default/forced
>1. You can set an old audio track to be default/forced
>1. If your muxing is limited to add/delete [attachments,chapters], or make old track default/forced, you can make it fast [by modifying the source file], a prompt will appear when this happen

## Muxing Options
>1. You can change subtitle settings(delay, track name, language) for each subtitle file to override global settings
>1. You can save a log file to see everything happened
## Notes
>1. the video destination folder shouldn't be the same as source folder
>1. When the option [keep this subtitle/audio only] is activated with language/track that does not exist in the source video, then the option will lead to output video with only chosen language/track (even if it means to discard all subtitle/audio from the source)
>1. When the option [make this subtitle/audio default] is activated with language/track that does not exists in the source, then the option will be ignored
## Supported Extensions
**Video**:
[AVI, MKV, MP4, M4V, MOV, MPEG, OGG, OGM, H264, H265, WEBM, WMV]

**Subtitle**:
[ASS, SRT, SSA, SUP, PGS]

**Chapter**:
[XML]

## 💾 Downloads
[![Github All Releases](https://img.shields.io/github/downloads/yaser01/mkv-muxing-batch-gui/total.svg?color=4DC71F)]()

MKV Muxing Batch GUI works on Windows 7/8/8.1/10 32-bit/64-bit

See the project's [releases&nbsp;page](https://github.com/yaser01/mkv-muxing-batch-gui/releases) for download links

<br><br>

## 🙏 Attribution
- The whole app depends on mkvmerge and mkvpropedit so Big thanks to [MKVToolNix](https://gitlab.com/mbunkus/mkvtoolnix)
- Big thanks to my friends who helped me in testing the app and provided a lot of ideas
  <br><br>
## 🦟 Software bugs
Bugs reported on the project's [issues page](https://github.com/yaser01/mkv-muxing-batch-gui/issues) will be checked weakly and I'm looking forward any suggestions for future updates

<br><br>

## 🏷️ License
GPLv2 © [yaser01](https://github.com/yaser01/mkv-muxing-batch-gui/blob/main/LICENSE)
