import pytest
import os


FILE_NAME = "result.csv"

@pytest.fixture(name="configs")
def get_conifgs():
    from spydy import urls, request, parsers, logs, store
    myconfig = {
        "Globals":{
            "run_mode": "async_forever",
            "nworkers": "4"
        },
        "PipeLine":[urls.DummyUrls(url="https://dmoz-odp.org", repeat=10),
                    request.AsyncHttpRequest(), parsers.DmozParser(), logs.MessageLog(), store.CsvStore(file_name=FILE_NAME)]
        }

    return myconfig

@pytest.mark.skip
def test_configurate_and_run_spydy_by_dict(configs):
    from spydy.engine import Engine
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)
    engine = Engine.from_dict(configs=configs)
    engine.run()
    assert os.path.exists(FILE_NAME) == True
    os.remove(FILE_NAME)