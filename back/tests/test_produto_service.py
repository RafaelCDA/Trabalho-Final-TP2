from src.api.services.produto_service import ProdutoService

def test_criar_produto():
    service = ProdutoService()

    produto = service.criar({
        "nome": "Maçã",
        "preco": 10,
        "banca": "Banca 1",
        "lat": 0,
        "long": 0
    })

    assert produto.id == 1
    assert produto.nome == "Maçã"
    assert produto.preco == 10

def test_listar_produtos():
    service = ProdutoService()

    service.criar({
        "nome": "Banana",
        "preco": 5,
        "banca": "Banca 1",
        "lat": 0,
        "long": 0
    })

    resultado = service.listar()
    assert len(resultado) == 1
    assert resultado[0].nome == "Banana"

def test_busca_por_texto():
    service = ProdutoService()

    service.criar({
        "nome": "Apple iPhone",
        "preco": 5000,
        "banca": "Banca 1",
        "lat": 0,
        "long": 0
    })
    service.criar({
        "nome": "Green Apple",
        "preco": 10,
        "banca": "Banca 1",
        "lat": 0,
        "long": 0
    })
    service.criar({
        "nome": "Pineapple",
        "preco": 8,
        "banca": "Banca 1",
        "lat": 0,
        "long": 0
    })

    resultado = service.buscar_por_texto("appl")

    assert len(resultado) == 3
    nomes = [p.nome for p in resultado]
    assert "Apple iPhone" in nomes
    assert "Green Apple" in nomes
    assert "Pineapple" in nomes

