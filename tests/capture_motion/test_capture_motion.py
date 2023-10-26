# import pytest
# import os

# from use_case.capture_motion import capture_motion
# from video_source.stream import Stream
# from detectors.motion_detection import detect_motion, draw_contours
# from video_writer.video_writer import VideoWriter


# # def test_capture_motion(data_directory):
# #     test_video_file = os.path.join(data_directory, "single_motion_clip.avi")
# #     stream = Stream(test_video_file)
# #     width, height = stream.width, stream.height
# #     writer = VideoWriter(
# #         width, height, os.path.join(data_directory, "test_capture_motion.avi")
# #     )
# #     with stream:
# #         ret, frame = stream.stream()
# #     capture_motion(stream, frame, writer, tail_time=5, buffer=None)
# #     assert os.path.isfile(os.path.join(data_directory, "test_capture_motion.avi"))


# if __name__ == "__main__":
#     pytest.main()
