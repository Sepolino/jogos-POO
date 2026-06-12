from app.models.game_model import GameModel


def test_model_inicia_partida_com_jogadores_configurados():
    model = GameModel()
    model.configure_players(["Ana", "Bruno"])
    model.start_new_match()

    assert model.get_current_player_text() == "Ana (X)"
    assert model.get_board() == [["", "", ""], ["", "", ""], ["", "", ""]]


def test_model_executa_partida_com_vitoria():
    model = GameModel()
    model.configure_players(["Ana", "Bruno"])
    model.start_new_match()

    assert model.play_turn(0, 0)
    assert model.play_turn(1, 0)
    assert model.play_turn(0, 1)
    assert model.play_turn(1, 1)
    assert model.play_turn(0, 2)

    result = model.get_result()
    assert model.is_finished()
    assert result["winner"] == "Ana (X)"
    assert result["moves"] == 5
