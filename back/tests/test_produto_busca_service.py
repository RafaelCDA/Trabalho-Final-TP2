"""
TESTES TDD - HU-01 e HU-02
Desenvolvimento Orientado a Testes - FASE VERMELHO
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.api.services.produto_busca_service import ProdutoBuscaService

def test_hu01_busca_produtos_por_nome():
    """HU-01: Como usuário, quero buscar produtos por nome"""
    from api.services.produto_busca_service import ProdutoBuscaService
    
    service = ProdutoBuscaService()
    resultados = service.buscar_produtos("tomate", -15.765, -47.876)
    
    # DEVE FALHAR primeiro - teste vermelho
    assert len(resultados) > 0, "Deveria encontrar produtos com 'tomate'"
    assert any("tomate" in p.nome.lower() for p in resultados)

def test_hu01_busca_produtos_por_banca():
    """HU-01: Como usuário, quero buscar produtos por nome da banca"""
    from api.services.produto_busca_service import ProdutoBuscaService
    
    service = ProdutoBuscaService()
    resultados = service.buscar_produtos("Banca do João", -15.765, -47.876)
    
    assert len(resultados) > 0, "Deveria encontrar produtos da 'Banca do João'"

def test_hu02_ordenacao_por_preco():
    """HU-02: Como usuário, quero ordenar por preço"""
    from api.services.produto_busca_service import ProdutoBuscaService
    
    service = ProdutoBuscaService()
    produtos = service.buscar_produtos("", -15.765, -47.876)  # Todos produtos
    ordenados = service.ordenar_produtos(produtos, "preco", -15.765, -47.876)
    
    precos = [p.preco for p in ordenados]
    assert precos == sorted(precos), "Deveria estar ordenado por preço crescente"

def test_hu02_ordenacao_por_localizacao():
    """HU-02: Como usuário, quero ordenar por localização"""
    from api.services.produto_busca_service import ProdutoBuscaService
    
    service = ProdutoBuscaService()
    produtos = service.buscar_produtos("", -15.765, -47.876)
    ordenados = service.ordenar_produtos(produtos, "localizacao", -15.765, -47.876)
    
    assert len(ordenados) > 0, "Deveria retornar produtos ordenados"
