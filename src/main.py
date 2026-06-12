from src.core import Jogador
from src.jogos import JogoDaVelha, XadrezSimplificado


def menu_principal() -> None:
    print("\n" + "=" * 40)
    print("   🎲 JOGOS DE TABULEIRO 🎲")
    print("=" * 40)
    print("  1. Jogo da Velha")
    print("  2. Xadrez Simplificado")
    print("  0. Sair")
    print("=" * 40)


def configurar_jogadores(n: int = 2) -> list[Jogador]:
    jogadores = []
    simbolos = ["X", "O"] if n == 2 else ["B", "P"]
    for i in range(n):
        nome = input(f"  Nome do Jogador {i + 1}: ").strip() or f"Jogador {i + 1}"
        jogadores.append(Jogador(nome, simbolos[i]))
    return jogadores


def main() -> None:
    while True:
        menu_principal()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("\nAté logo! 👋\n")
            break

        elif opcao == "1":
            print("\n--- Jogo da Velha ---")
            jogadores = configurar_jogadores(2)
            jogo = JogoDaVelha(jogadores[0], jogadores[1])
            jogo.jogar_terminal()

        elif opcao == "2":
            print("\n--- Xadrez Simplificado ---")
            print("  Jogador 1 = Brancas (B) | Jogador 2 = Pretas (P)")
            jogadores = configurar_jogadores(2)
            # Redefine símbolos para xadrez
            from src.core import Jogador as J
            branco = J(jogadores[0].nome, "B")
            preto = J(jogadores[1].nome, "P")
            jogo = XadrezSimplificado(branco, preto)
            jogo.jogar_terminal()

        else:
            print("  Opção inválida.")

        input("\nPressione ENTER para voltar ao menu...")


if __name__ == "__main__":
    main()
