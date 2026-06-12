"""Teste que simula o fluxo completo da UI para verificar exibição de empate."""

import sys
sys.path.insert(0, ".")

import pytest

pytest.importorskip("kivy")
pytest.importorskip("kivymd")

from app.models.game_model import GameModel
from app.controllers.game_controller import GameController
from kivy.uix.screenmanager import ScreenManager


def test_empate_ui_flow():
    """Simula o fluxo completo: configure -> play -> resultado (empate)."""
    print("\n" + "="*70)
    print("TESTE: Fluxo completo da UI com EMPATE")
    print("="*70)
    
    # Cria o controller e o model (sem GUI real)
    manager = ScreenManager()
    controller = GameController(manager)
    
    # Configura jogadores
    print("\n1. Configurando jogadores...")
    controller._model.configure_players(["Alice", "Bob"])
    print(f"   Players: {controller._model._player_names}")
    
    # Inicia a partida
    print("\n2. Iniciando partida...")
    controller.start_match(["Alice", "Bob"])
    print(f"   Tabuleiro inicial: {controller.get_board()}")
    
    # Executa jogadas que resultam em empate
    print("\n3. Executando jogadas para empate...")
    moves = [
        (0, 0), (0, 1),
        (0, 2), (1, 2),
        (1, 0), (2, 0),
        (1, 1), (2, 2),
        (2, 1),
    ]
    
    for i, (row, col) in enumerate(moves):
        result = controller.play_cell(row, col)
        print(f"   Move {i+1}: ({row},{col}) - Aceita: {result}")
    
    # Verifica se o jogo terminou
    print("\n4. Verificando estado final...")
    print(f"   Tabuleiro final: {controller.get_board()}")
    print(f"   Jogo terminado: {controller._model.is_finished()}")
    
    # Obtém o resultado
    result = controller.get_result()
    print("\n5. Resultado Final (como seria exibido na UI):")
    print(f"   ✓ Winner: {result['winner']}")
    print(f"   ✓ Status: {result['status']}")
    print(f"   ✓ Moves: {result['moves']}")
    print(f"   ✓ Scoreboard:")
    for player in result['scoreboard']:
        print(f"      - {player['nome']} ({player['simbolo']})")
        print(f"        V:{player['vitorias']} D:{player['derrotas']} E:{player['empates']}")
    
    # Validações
    print("\n6. Validações:")
    assert result['winner'] == "Empate", f"❌ ERRO: Winner deveria ser 'Empate', mas é '{result['winner']}'"
    print("   ✓ Winner é 'Empate'")
    
    assert result['status'] == "Empate", f"❌ ERRO: Status deveria ser 'Empate', mas é '{result['status']}'"
    print("   ✓ Status é 'Empate'")
    
    assert result['moves'] == 9, f"❌ ERRO: Deveria ter 9 jogadas, mas tem {result['moves']}"
    print("   ✓ Número de jogadas correto (9)")
    
    for player in result['scoreboard']:
        if player['nome'] == "Alice":
            assert player['empates'] == 1, f"❌ ERRO: Alice deveria ter 1 empate"
            print("   ✓ Alice com 1 empate")
        elif player['nome'] == "Bob":
            assert player['empates'] == 1, f"❌ ERRO: Bob deveria ter 1 empate"
            print("   ✓ Bob com 1 empate")
    
    print("\n" + "="*70)
    print("✓ TESTE PASSOU: Empate detectado e exibido corretamente!")
    print("="*70)


def test_vitoria_ui_flow():
    """Simula o fluxo completo: configure -> play -> resultado (vitória)."""
    print("\n" + "="*70)
    print("TESTE: Fluxo completo da UI com VITÓRIA")
    print("="*70)
    
    manager = ScreenManager()
    controller = GameController(manager)
    
    # Configura jogadores
    print("\n1. Configurando jogadores...")
    controller._model.configure_players(["Charlie", "Diana"])
    
    # Inicia a partida
    print("\n2. Iniciando partida...")
    controller.start_match(["Charlie", "Diana"])
    
    # Executa jogadas que resultam em vitória
    print("\n3. Executando jogadas para vitória...")
    moves = [
        (0, 0), (1, 0),
        (0, 1), (1, 1),
        (0, 2),  # Charlie vence
    ]
    
    for i, (row, col) in enumerate(moves):
        result = controller.play_cell(row, col)
        print(f"   Move {i+1}: ({row},{col}) - Aceita: {result}")
    
    # Obtém o resultado
    result = controller.get_result()
    print("\n4. Resultado Final (como seria exibido na UI):")
    print(f"   ✓ Winner: {result['winner']}")
    print(f"   ✓ Status: {result['status']}")
    
    # Validações
    print("\n5. Validações:")
    assert result['winner'] == "Charlie (X)", f"❌ ERRO: Winner deveria ser 'Charlie (X)'"
    print("   ✓ Winner é 'Charlie (X)'")
    
    assert result['status'] == "Vitoria", f"❌ ERRO: Status deveria ser 'Vitoria'"
    print("   ✓ Status é 'Vitoria'")
    
    print("\n" + "="*70)
    print("✓ TESTE PASSOU: Vitória detectada e exibida corretamente!")
    print("="*70)


if __name__ == "__main__":
    test_empate_ui_flow()
    test_vitoria_ui_flow()
    print("\n✓ TODOS OS TESTES PASSARAM!")
