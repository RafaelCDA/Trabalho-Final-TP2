# Configuração
SRC=src
TESTS=tests
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

# Detectar sistema operacional
ifeq ($(OS),Windows_NT)
	RM=powershell -Command "Remove-Item -Recurse -Force"
else
	RM=rm -rf
endif

# Target padrão
default: run

# Ambiente
$(VENV):
	@echo "Criando ambiente virtual."
	python3 -m venv $(VENV)
	@echo "Atualizando pip."
	$(PIP) install --upgrade pip
	@echo "Instalando dependências do requirements.txt."
	$(PIP) install -r requirements.txt

install: $(VENV)
	@echo "Ambiente pronto."

# Execução
run: install
	@echo "Inicializando servidor ..."
	$(PYTHON) -m uvicorn src.main:app --reload

# Qualidade de código
format: install
	@echo "Formatando código com Black."
	$(VENV)/bin/black $(SRC) $(TESTS)

lint: install
	@echo "Executando Ruff (lint)."
	$(VENV)/bin/ruff check $(SRC) $(TESTS)
	@echo "Executando Pyright (type-check)."
	$(VENV)/bin/pyright

# Testes
test: install
	@echo "Executando testes."
	$(VENV)/bin/pytest -q

coverage: install
	@echo "Executando cobertura de testes."
	$(VENV)/bin/coverage run -m pytest
	@echo "Gerando relatório de cobertura."
	$(VENV)/bin/coverage report -m
	@echo "Gerando relatório HTML em htmlcov/."
	$(VENV)/bin/coverage html

# Documentação
docs: install
	@echo "Gerando documentação MkDocs."
	$(VENV)/bin/mkdocs build
	@echo "Documentação gerada em site/"

docs-serve: install
	@echo "Iniciando servidor de documentação MkDocs."
	$(VENV)/bin/mkdocs serve

# Help
help:
	@echo ""
	@echo "============= COMANDOS DISPONÍVEIS ============="
	@echo " make                - Inicia o servidor"
	@echo " make install        - Cria a venv e instala dependências"
	@echo " make run            - Inicia o servidor FastAPI"
	@echo " make format         - Formata código com Black"
	@echo " make lint           - Executa Ruff e Pyright"
	@echo " make test           - Executa testes"
	@echo " make coverage       - Gera relatório de cobertura"
	@echo " make docs           - Gera documentação MkDocs"
	@echo " make docs-serve     - Sobe servidor local da documentação"
	@echo " make clean          - Remove caches, ambiente virtual e build da documentação"
	@echo "================================================="
	@echo ""

# Limpeza
clean:
	@echo "Removendo ambiente virtual e caches."
	$(RM) $(VENV)
	$(RM) .pytest_cache
	$(RM) .ruff_cache
	$(RM) .mypy_cache
	$(RM) htmlcov
	$(RM) site
	$(RM) .coverage

ifeq ($(OS),Windows_NT)
	@echo "Removendo __pycache__ recursivamente."
	powershell -Command "Get-ChildItem -Recurse -Directory -Filter '__pycache__' | Remove-Item -Recurse -Force"
else
	@echo "Removendo __pycache__ recursivamente."
	find . -type d -name "__pycache__" -exec rm -rf {} +
endif

	@echo "Limpeza concluída."

.PHONY: default help install run format lint test coverage docs clean
