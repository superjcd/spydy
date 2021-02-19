from spydy.store import CsvStore, DbStore, AsyncCsvStore
import os
import asyncio


def test_csv_store_output(tmpdir):
    test_csv_file = "dmoz_test.csv"
    if os.path.exists(test_csv_file):
        os.remove(test_csv_file)
    csvstore = CsvStore(file_name=test_csv_file)
    data = {
        "categories": "1,031,722",
        "editors": "91,929",
        "sites": "3,861,202",
        "languages": "90",
    }
    result = csvstore(data)
    assert result == data
    assert os.path.exists(test_csv_file) == True
    os.remove(test_csv_file)


def test_async_csv_store_output(tmpdir):
    test_csv_file = "dmoz_test.csv"
    if os.path.exists(test_csv_file):
        os.remove(test_csv_file)
    csvstore = AsyncCsvStore(file_name=test_csv_file)
    data = {
        "categories": "1,031,722",
        "editors": "91,929",
        "sites": "3,861,202",
        "languages": "90",
    }
    asyncio.run(csvstore(data))
    assert os.path.exists(test_csv_file) == True
    os.remove(test_csv_file)
