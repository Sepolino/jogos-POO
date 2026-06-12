from ..core import (
    ConjuntoDeRegras,
    Jogada,
    Jogador,
    JogoTabuleiro,
    Peca,
    RegraDestinoDentroDoTabuleiro,
    RegraDestinoDentroDoTabuleiroVazio,
    Tabuleiro,
)


class PecaVelha(Peca):
    """
    Peca simples do Jogo da Velha (X ou O).

    Sobrescreve simbolo e movimentos_validos de Peca.
    """

    @property
    def simbolo(self) -> str:
        """Retorna o simbolo do jogador dono da peca."""
        return self._jogador.simbolo

    def movimentos_validos(
        self,
        linha: int,
        coluna: int,
        tabuleiro: Tabuleiro,
    ) -> list[tuple[int, int]]:
        """Retorna movimentos validos; no jogo da velha pecas nao se movem."""
        return []


class JogoDaVelha(JogoTabuleiro):
    """
    Implementacao do Jogo da Velha (3x3).

    Herda de JogoTabuleiro e sobrescreve todos os metodos abstratos.
    Demonstra heranca, polimorfismo, composicao e uso de regras.
    """

    TAMANHO = 3

    def __init__(self, jogador1: Jogador, jogador2: Jogador):
        super().__init__([jogador1, jogador2])
        self._tabuleiro = Tabuleiro(self.TAMANHO, self.TAMANHO)
        self._regras = ConjuntoDeRegras(
            [
                RegraDestinoDentroDoTabuleiro(),
                RegraDestinoDentroDoTabuleiroVazio(),
            ]
        )

    def inicializar_tabuleiro(self) -> None:
        """Configura o tabuleiro vazio para uma nova partida."""
        self._tabuleiro.limpar()

    def validar_jogada(self, jogada: Jogada) -> bool:
        """Valida se a posicao escolhida esta dentro do tabuleiro e vazia."""
        valido, _motivo = self._regras.validar_todas(jogada, self._tabuleiro)
        return valido

    def aplicar_jogada(self, jogada: Jogada) -> None:
        """Coloca a peca do jogador atual na celula escolhida."""
        peca = PecaVelha(jogada.jogador)
        self._tabuleiro.definir_celula(
            jogada.linha_destino,
            jogada.coluna_destino,
            peca,
        )

    def realizar_jogada_posicao(self, linha: int, coluna: int) -> bool:
        """
        Executa uma jogada no turno atual usando coordenadas do tabuleiro.

        Este metodo publico foi criado para interfaces graficas e outros
        adaptadores nao precisarem conhecer a classe Jogada nem atributos
        internos do jogo.
        """
        jogada = Jogada(
            jogador=self.jogador_atual,
            linha_destino=linha,
            coluna_destino=coluna,
        )
        return self.fazer_jogada(jogada)

    def obter_estado_tabuleiro(self) -> list[list[str]]:
        """
        Retorna uma matriz com os simbolos visiveis do tabuleiro.

        Celulas vazias sao representadas por string vazia para facilitar
        renderizacao em interfaces graficas.
        """
        estado = []
        for linha in range(self.TAMANHO):
            valores = []
            for coluna in range(self.TAMANHO):
                celula = self._tabuleiro.obter_celula(linha, coluna)
                valores.append(celula.simbolo if celula else "")
            estado.append(valores)
        return estado

    def obter_placar(self) -> list[dict[str, int | str]]:
        """Retorna o placar dos jogadores em formato estruturado."""
        return [
            {
                "nome": jogador.nome,
                "simbolo": jogador.simbolo,
                "vitorias": jogador.vitorias,
                "derrotas": jogador.derrotas,
                "empates": jogador.empates,
            }
            for jogador in self._jogadores
        ]

    def verificar_fim_de_jogo(self) -> bool:
        """Verifica vitoria ou empate apos uma jogada."""
        for jogador in self._jogadores:
            if self._verificar_vitoria(jogador):
                self._vencedor = jogador
                jogador.registrar_vitoria()
                outro = [j for j in self._jogadores if j != jogador][0]
                outro.registrar_derrota()
                print(f"\n{jogador.nome} ({jogador.simbolo}) venceu!")
                return True

        if self._tabuleiro.esta_cheio():
            for jogador in self._jogadores:
                jogador.registrar_empate()
            print("\nEmpate!")
            return True

        return False

    def exibir_tabuleiro(self) -> None:
        """Exibe o estado atual do tabuleiro no terminal."""
        print("\n   0   1   2")
        for linha_indice in range(self.TAMANHO):
            linha = []
            for coluna_indice in range(self.TAMANHO):
                celula = self._tabuleiro.obter_celula(
                    linha_indice,
                    coluna_indice,
                )
                linha.append(f" {celula.simbolo if celula else '.'} ")
            print(f"{linha_indice} {'|'.join(linha)}")
            if linha_indice < self.TAMANHO - 1:
                print("  ---+---+---")
        print()

    def _verificar_vitoria(self, jogador: Jogador) -> bool:
        simbolo = jogador.simbolo

        def todos_iguais(celulas) -> bool:
            return all(c is not None and c.simbolo == simbolo for c in celulas)

        for indice in range(self.TAMANHO):
            if todos_iguais(self._tabuleiro.obter_linha(indice)):
                return True
            if todos_iguais(self._tabuleiro.obter_coluna(indice)):
                return True

        if todos_iguais(self._tabuleiro.obter_diagonal_principal()):
            return True
        if todos_iguais(self._tabuleiro.obter_diagonal_secundaria()):
            return True

        return False

    def jogar_terminal(self) -> None:
        """Loop principal para jogar no terminal."""
        print("=" * 30)
        print("   JOGO DA VELHA")
        print("=" * 30)
        self.iniciar()

        while not self._partida_encerrada:
            self.exibir_tabuleiro()
            jogador = self.jogador_atual
            print(f"Turno de {jogador.nome} ({jogador.simbolo})")

            try:
                linha = int(input("  Linha (0-2): "))
                coluna = int(input("  Coluna (0-2): "))
            except ValueError:
                print("  Entrada invalida. Use numeros de 0 a 2.")
                continue

            jogada = Jogada(
                jogador=jogador,
                linha_destino=linha,
                coluna_destino=coluna,
            )
            self.fazer_jogada(jogada)

        self.exibir_tabuleiro()
        print("\nPlacar final:")
        for jogador in self._jogadores:
            print(f"  {jogador.placar()}")
