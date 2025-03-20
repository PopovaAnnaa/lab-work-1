import json
from car_customization import save_customization_data


def test_save_customization_data(mocker):
    mock_data = {"selected_skin": "Wrecker.png", "selected_road": "Downtown.png"}
    mock_open = mocker.mock_open()
    mocker.patch("builtins.open", mock_open)

    save_customization_data(mock_data)

    mock_open.assert_called_once_with("customization_data.json", "w")

    handle = mock_open()

    written_content = "".join(call.args[0] for call in handle.write.call_args_list)

    assert written_content == json.dumps(mock_data)
