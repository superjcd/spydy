from spydy.urls import FileUrls, DummyUrls
from spydy.exceptions import UrlCompleted
import pytest


class TestFileUrls():
    fileurls = FileUrls(file_name="./tests/files/urls")

    def test_urls_total_equal_to_num(self, num=7):
        assert self.fileurls.total == num

    def test_urls_add_to_end(self, url="url_at_end.com"):
        self.fileurls.add_to_end(url)
        self.test_urls_total_equal_to_num(8)

    def test_urls_add_to_front(self, url="url_at_front.com"):
        self.fileurls.add_to_front(url)
        self.test_urls_total_equal_to_num(9)

    def test_urls_callmethod_call_pop(self):
        assert self.fileurls() == "url_at_front.com"

    def test_urls_handle_exception_add_url_back_to_front(self):
        wrong_url = "wrong.com"
        self.fileurls.handle_exception(recovery_type="url_back_front", url=wrong_url)
        assert self.fileurls() == wrong_url

    def test_urls_handle_exception_add_url_back_to_end(self):
        wrong_url = "wrong.com"
        self.fileurls.handle_exception(recovery_type="url_back_end", url=wrong_url)
        assert self.fileurls._urls[-1] == wrong_url

    def test_urls_finished_and_raise_urlcompleted_excpetion(self):
        with pytest.raises(UrlCompleted) as e:
            while True:
                self.fileurls()


class TestDummyUrls():
    dummyurls = DummyUrls(url="dummy.com", repeat=5)

    def test_urls_total_equal_to_num(self, num=5):
        assert self.dummyurls.total == num

    def test_urls_add_to_end(self, url="url_at_end.com"):
        self.dummyurls.add_to_end(url)
        self.test_urls_total_equal_to_num(num=6)

    def test_urls_add_to_front(self, url="url_at_front.com"):
        self.dummyurls.add_to_front(url)
        self.test_urls_total_equal_to_num(num=7)

    def test_urls_callmethod_call_pop(self):
        assert self.dummyurls() == "url_at_front.com"

    def test_urls_handle_exception_add_url_back_to_front(self):
        wrong_url = "wrong.com"
        self.dummyurls.handle_exception(recovery_type="url_back_front", url=wrong_url)
        assert self.dummyurls() == wrong_url

    def test_urls_handle_exception_add_url_back_to_end(self):
        wrong_url = "wrong.com"
        self.dummyurls.handle_exception(recovery_type="url_back_end", url=wrong_url)
        assert self.dummyurls._urls[-1] == wrong_url

    def test_urls_finished_and_raise_urlcompleted_excpetion(self):
        with pytest.raises(UrlCompleted) as e:
            while True:
                self.dummyurls()



  



