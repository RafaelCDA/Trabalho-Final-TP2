# Modelos da Aplicação

A camada de **modelos** contém as entidades persistidas no banco de dados.
Cada modelo é definido utilizando **SQLAlchemy ORM**, que realiza o
mapeamento entre classes Python e tabelas relacionais.

Esses modelos servem como base para toda a lógica de dados do sistema,
sendo utilizados por:

- Repositórios  
- Serviços  
- Controladores e rotas  
- Processos de validação e operações CRUD  

A documentação abaixo é gerada automaticamente a partir dos módulos
presentes no diretório `src/models`.

---

## Modelo: User

Representa os usuários cadastrados no sistema, incluindo consumidores,
fornecedores e administradores.

::: src.models.user

---

## Modelo: Banca

Define as bancas criadas pelos fornecedores dentro da feira, incluindo
informações de identificação, localização e horário de funcionamento.

::: src.models.banca

---

## Modelo: Produto

Modela os produtos vinculados a uma banca, armazenando dados comerciais
como nome, preço e imagem.

::: src.models.produto_model

---

## Modelo: Address

Representa os endereços registrados no sistema, permitindo associar
bancas e usuários a localizações específicas.

::: src.models.address
