import pytest
from unittest.mock import patch, mock_open
from gameplay import load_json_data 

def test_load_json_data_success():
    mock_data = '{"score": 10, "highscore": 100}'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        data = load_json_data("game_data.json", {"score": 0, "highscore": 0})
        assert data == {"score": 10, "highscore": 100}

def test_load_json_data_file_not_found():
    with patch("os.path.exists", return_value=False):
        data = load_json_data("non_existent_file.json", {"score": 0, "highscore": 0})
        assert data == {"score": 0, "highscore": 0}

def test_load_json_data_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        data = load_json_data("game_data.json", {"score": 0, "highscore": 0})
        assert data == {"score": 0, "highscore": 0}
