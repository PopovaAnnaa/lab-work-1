import json
from car_customization import load_customization_data


def test_load_customization_data(mocker):
    mock_data = {"selected_skin": "Striker.png", "selected_road": "Snowpath.png"}
    mock_open = mocker.mock_open(read_data=json.dumps(mock_data))
    mocker.patch("builtins.open", mock_open)

    data = load_customization_data()
    assert data == mock_data
