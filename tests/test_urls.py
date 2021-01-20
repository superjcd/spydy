from spydy.urls import FileUrls

def test_fileurls():
    fileurls = FileUrls(file_name="./tests/files/urls")
    assert fileurls.pop() == "https://dmoz-odp.org/"