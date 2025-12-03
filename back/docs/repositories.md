# Camada de Repositórios

A camada de **repositórios** é responsável por centralizar e organizar
as operações de acesso e manipulação dos dados persistidos no banco.
Cada repositório encapsula consultas, comandos e regras específicas de
persistência para uma entidade, mantendo a lógica de acesso a dados
isolada das demais camadas da aplicação — como serviços, DTOs e rotas.

Essa separação melhora a manutenção, facilita testes, reduz acoplamento
e garante uma estrutura mais limpa e escalável.

---

## Repositório de Usuários

Gerencia operações como criação, consulta, autenticação e atualização
de usuários cadastrados no sistema.

::: src.repositories.user_repository

---

## Repositório de Bancas

Responsável por consultar, criar, atualizar e remover bancas vinculadas
a fornecedores. Também controla acesso a dados relacionados à operação
comercial da feira.

::: src.repositories.banca_repository

---

## Repositório de Endereços

Centraliza a manipulação de endereços registrados no sistema, incluindo
cadastro, consultas, atualizações e associações com outras entidades.

::: src.repositories.address_repository

---

## Repositório de Produtos

Gerencia todos os produtos vinculados a bancas, controlando cadastro,
atualizações de preço, remoção e consultas estruturadas.

::: src.repositories.produto_repository

---

## Repositório de Pesquisas

Registra as pesquisas realizadas pelos usuários e permite consultas para
estatísticas, monitoramento e análises de comportamento.

::: src.repositories.pesquisa_repository
