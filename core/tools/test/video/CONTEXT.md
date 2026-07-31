# video
> T1 unit tests for the video tool. Fixtures live here; network-marked cases are excluded from verify-fast.

<!-- routing:start -->
## Routing

| File | Interface | API | Description |
|------|-----------|-----|-------------|
| [`test_video_core.py`](test_video_core.py) | [`test_video_core.pyi`](test_video_core.pyi) | `FakeProc`, `FakeMedia`, `download_audio`, `transcribe`, `download_video` | test_video_core.py — T0/T1 unit tests for video_core (no network; fixtures + injected runners) |
| [`test_video_images.py`](test_video_images.py) | [`test_video_images.pyi`](test_video_images.pyi) | `FakeProc`, `FakeMedia`, `FakeImages`, `ocr_image`, `caption_image` | test_video_images.py — T1 unit tests for the image-post path (no network, injected runners) |
<!-- routing:end -->
