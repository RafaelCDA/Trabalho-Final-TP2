"""
# Configuração do Banco de Dados

Este módulo estabelece os componentes fundamentais para acesso ao banco
de dados da aplicação. A configuração inclui:

- criação do engine de conexão
- fábrica de sessões para operações transacionais
- base declarativa utilizada pelos modelos ORM

Todos os módulos que interagem com o banco devem utilizar esta camada
como ponto central de inicialização e gerenciamento.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# -------------------------------------------------------------------
# Engine Factory
# -------------------------------------------------------------------
def create_db_engine(url: str = "sqlite:///./data/database.db"):
    """
    Cria e retorna o engine de banco de dados.

    ## Parâmetros
    - **url** (*str*): Caminho de conexão do banco.
      Por padrão, utiliza SQLite armazenado em arquivo local.

    ## Retorno
    - **Engine**: Instância configurada para comunicação com o banco.

    ## Observações
    - `check_same_thread=False` é necessário em ambientes que executam
      múltiplas threads, garantindo acesso seguro ao SQLite.
    """
    return create_engine(url, connect_args={"check_same_thread": False})


engine = create_db_engine()


# -------------------------------------------------------------------
# Session Factory
# -------------------------------------------------------------------
def create_session_factory(engine):
    """
    Cria e retorna a fábrica de sessões.

    ## Parâmetros
    - **engine** (*Engine*): Engine já configurado para o banco.

    ## Retorno
    - **sessionmaker**: Fábrica responsável por gerar sessões de uso.

    ## Detalhes
    - `autocommit=False`: o commit deve ser realizado manualmente.
    - `autoflush=False`: evita gravações automáticas prematuras.
    """
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


SessionLocal = create_session_factory(engine)


# -------------------------------------------------------------------
# Declarative Base
# -------------------------------------------------------------------
def create_declarative_base():
    """
    Cria a base declarativa utilizada pelos modelos ORM.

    ## Retorno
    - **DeclarativeBase**: Classe base para definição de modelos.

    ## Observações
    - Todos os modelos da aplicação devem herdar desta base para serem
      registrados corretamente no metadata utilizado pelo SQLAlchemy.
    """
    return declarative_base()


Base = create_declarative_base()
