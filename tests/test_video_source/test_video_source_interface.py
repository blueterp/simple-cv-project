"""TDD tests for footage source interface"""
import pytest
from video_source.fake_video_source import FakeVideoSource


def test_create_webcamera():
    """Tests simple constructor for fake video source object"""
    camera = FakeVideoSource()
    assert camera.source_index == 0


if __name__ == "__main__":
    pytest.main()
