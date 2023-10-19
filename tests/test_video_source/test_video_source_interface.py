import pytest
from video_source.fake_video_source import FakeVideoSource


def test_create_fake_video_source():
    camera = FakeVideoSource()
    assert camera.source_index == 0


def test_stream_fake_video_source():
    camera = FakeVideoSource()

    with camera.stream() as stream:
        assert stream.is_streaming
    assert not stream.is_streaming


# def test_save_stream_writer():
#     camera = FakeVideoSource()
#     snippet = camera.save_snippet(stream_id="snippet1", duration="10s")

#     assert snippet


if __name__ == "__main__":
    pytest.main()
