import json
from car_customization import load_game_data


def test_load_game_data(mocker):
    mock_data = {"score": 100, "highscore": 200}
    mock_open = mocker.mock_open(read_data=json.dumps(mock_data))
    mocker.patch("builtins.open", mock_open)

    data = load_game_data()
    assert data == mock_data
