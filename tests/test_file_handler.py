from utils.file_handler import FileHandler

def test_write_and_read_json(tmp_path):
    test_file = tmp_path / "test.json"
    data = {"name": "Library", "status": "active"}

    FileHandler.write(str(test_file), data)
    result = FileHandler.read(str(test_file))

    assert result == data

