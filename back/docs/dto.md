# Camada de DTOs

A camada de **DTOs (Data Transfer Objects)** é responsável por padronizar
a estrutura de entrada e saída de dados utilizada pelos endpoints e serviços.
Esses objetos garantem:

- Validação consistente dos dados recebidos.  
- Retornos uniformes para o cliente.  
- Isolamento entre modelos ORM e a API pública.  
- Segurança e clareza na troca de informações.  

Abaixo estão listados todos os DTOs organizados por domínio.

---

## DTOs de Usuário

Modelos utilizados para cadastro, autenticação, atualização e leitura de usuários.

::: src.dto.user_dto

---

## DTOs de Endereço

Estruturas aplicadas ao registro, modificação e retorno de endereços.

::: src.dto.address_dto

---

## DTOs de Banca

Modelos que representam a criação, atualização e leitura de bancas,
incluindo integração com DTOs de endereço.

::: src.dto.banca_dto

---

## DTOs de Produto

DTOs referentes aos produtos vinculados às bancas, incluindo operações
de criação, atualização e retorno.

::: src.dto.produto_dto

---

## DTOs de Pesquisa

Modelos utilizados para registrar pesquisas realizadas pelos usuários e
estruturação do retorno de buscas.

::: src.dto.pesquisa_dto
