# Camada de Serviços

A camada de **serviços** é responsável por centralizar e aplicar as regras de negócio
da aplicação.  
Enquanto os repositórios lidam diretamente com a persistência dos dados, os serviços
orquestram:

- Validações adicionais  
- Regras de negócio por entidade  
- Integrações entre múltiplos repositórios  
- Transformação de dados usando DTOs  
- Garantia de consistência e integridade  

Essa camada funciona como intermediária entre *controllers/endpoints* e o acesso ao
banco, mantendo o código mais organizado, testável e isolado.

---

## Serviço de Usuários

Gerencia criação, consulta, atualização e remoção de usuários, garantindo regras
como verificação de e-mail duplicado e padronização via DTOs.

::: src.services.user_service

---

## Serviço de Autenticação

Responsável pela autenticação simples utilizando e-mail e senha.  
Retorna DTOs prontos para consumo pela API, sem expor o modelo ORM.

::: src.services.auth_service

---

## Serviço de Bancas

Gerencia criação, listagem, atualização e remoção de bancas.  
Cria automaticamente o endereço vinculado e valida dados essenciais.

::: src.services.banca_service

---

## Serviço de Produtos

Aplica regras de negócios relacionadas a produtos, como validação de banca existente,
atualizações controladas e listagem por banca.

::: src.services.produto_service

---

## Serviço de Pesquisas

Executa operações avançadas de busca, incluindo filtros por preço, distância,
ordenadores customizados e registro automático das pesquisas realizadas.

::: src.services.pesquisa_service
