from spydy.store import CsvStore, DbStore


def test_csv_store_output():
    csvstore = CsvStore(file_name="temp.csv")
    data = {
        "categories": "1,031,722",
        "editors": "91,929",
        "sites": "3,861,202",
        "languages": "90",
    }
    result = csvstore(data)
    assert result == data


# def test_dbstore():
#     ds = DbStore(connection_url='sqlite:///./tests/files/dmoz.db', table_name="stats")
#     data = {'categories':"1,031,722", 'editors':"91,929", 'sites':"3,861,202", 'languages':"90"}
#     result = ds.store(data)
