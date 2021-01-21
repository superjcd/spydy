from spydy.store import DbStore

def test_dbstore():
    ds = DbStore(connection_url='sqlite:///./tests/files/dmoz.db', table_name="stats")
    data = {'categories':"1,031,722", 'editors':"91,929", 'sites':"3,861,202", 'languages':"90"}
    result = ds.store(data)