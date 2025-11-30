from typing import List, Optional
from src.models.produto_model import Produto

class ProdutoService:

    def __init__(self):
        # "Banco de dados" simples em memória
        self.produtos: List[Produto] = []
        self.next_id = 1

    def criar(self, data: dict) -> Produto:

        # === Validações básicas ===
        if not data.get("nome"):
            raise ValueError("Nome é obrigatório.")

        if data.get("preco") is None or data["preco"] < 0:
            raise ValueError("Preço inválido.")

        if not data.get("banca"):
            raise ValueError("A banca é obrigatória.")

        # Criar novo produto
        produto = Produto(
            id=self.next_id,
            **data
        )
        self.next_id += 1

        self.produtos.append(produto)
        return produto

    def listar(self) -> List[Produto]:
        return self.produtos

    def atualizar(self, produto_id: int, data: dict) -> Optional[Produto]:
        for produto in self.produtos:
            if produto.id == produto_id:

                for campo, valor in data.items():
                    if valor is not None:
                        setattr(produto, campo, valor)

                return produto

        return None

    def excluir(self, produto_id: int) -> bool:
        for produto in self.produtos:
            if produto.id == produto_id:
                self.produtos.remove(produto)
                return True

        return False

