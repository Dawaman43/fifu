
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path.cwd()))

try:
    from fifu.app import FifuApp
    from fifu.screens.video_select import VideoSelectScreen
    from fifu.services.youtube import VideoInfo
    from fifu.screens.options import OptionsScreen
    from fifu.services.youtube import ChannelInfo

    print("✅ Imports successful")

    # Test VideoSelectScreen instantiation
    videos = [
        VideoInfo(id="1", title="Video 1", url="http://v1"),
        VideoInfo(id="2", title="Video 2", url="http://v2"),
    ]
    screen = VideoSelectScreen(videos)
    print("✅ VideoSelectScreen instantiated")

    # Test App methods existence
    app = FifuApp()
    if hasattr(app, 'initiate_video_selection') and hasattr(app, 'on_video_selection_confirmed'):
        print("✅ App methods exist")
    else:
        print("❌ App methods missing")
        exit(1)

    # Test OptionsScreen methods (mocking app)
    channel = ChannelInfo(id="c1", name="Channel 1", url="http://c1")
    options_screen = OptionsScreen(channel)
    # options_screen.app = app  # Textual app property is read-only
    if hasattr(options_screen, '_initiate_video_selection'):
        print("✅ OptionsScreen has _initiate_video_selection")
    else:
        print("❌ OptionsScreen missing _initiate_video_selection")
        exit(1)

    print("✅ Verification passed!")

except Exception as e:
    print(f"❌ Verification failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
