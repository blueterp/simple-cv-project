from video_source.stream import Stream
from video_writer.local_video_writer import VideoWriter
from use_case.monitor_stream import capture_motion

stream = Stream("single_motion_clip.avi")
# stream = Stream(0)

writer = VideoWriter(stream.width, stream.height, "")
saved_file = capture_motion(stream, writer)
print(saved_file)
