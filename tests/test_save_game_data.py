from unittest.mock import patch, mock_open
import json
from gameplay import save_game_data

def test_save_game_data():
    with patch("builtins.open", mock_open()) as mock_file:
        save_game_data(10, 20)

        mock_file.assert_called_once_with("game_data.json", "w")

        # Отримуємо всі write() виклики та об'єднуємо їх у один рядок
        written_data = "".join(call_args[0][0] for call_args in mock_file().write.call_args_list)
        expected_json = json.dumps({"score": 10, "highscore": 20})  # Очікуваний JSON
        assert written_data == expected_json, f"Expected {expected_json}, but got {written_data}"
