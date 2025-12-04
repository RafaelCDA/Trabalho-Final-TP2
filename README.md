# Trabalho Final de Técnicas de Programação 2

## Integrantes:
- Ithalo Junio
- Thomas Jefferson
- Breno Back dos Santos
- Rafael Cutrim
- Sávio Henrique
- Gabriel
- Guilherme Gomes Santa Rosa
- Henrique

## Tecnologias:
- Python
- FastAPI
- Next.js
- Docker

## Instalação
1. Clone o repositório:
    ```bash
    git clone <link-do-repositório>
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd <nome-do-diretório>
    ```
3. Instale o Docker e Docker Compose, se ainda não estiverem instalados. [Guia de instalação](https://www.docs.docker.com/engine/install).
4. Execute o comando para iniciar os containers:
    ```bash
    docker-compose up --build -d
    ```
5. Acesse a aplicação no navegador:
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend: [http://localhost:80](http://localhost:80)
6. Para parar os containers, execute:
    ```bash
    docker-compose down
    ```
7. (Opcional) Para testar se o backend está funcionando corretamente, você pode acessar a rota de saúde via `curl` ou no navegador:
    ```bash
    curl http://localhost:80/health
    ```

## Desenvolvimento
Caso não queira utilizar o Docker, você pode executar o backend e o frontend separadamente.
### Backend
1. Navegue até o diretório do backend:
    ```bash
    cd back
    ```
2. Utilize o Makefile para criar um ambiente virtual e rodar a aplicação:
    ```bash
    make run
    ```
3. Acesse a aplicação no navegador em: [http://localhost:8000](http://localhost:8000)

### Frontend
1. Navegue até o diretório do frontend:
    ```bash
    cd front
    ```
2. Instale as dependências do Next.js:
    ```bash
    npm install
    ```
3. Inicie o servidor de desenvolvimento:
    ```bash
    npm run dev
    ```
4. Acesse a aplicação no navegador em: [http://localhost:3000](http://localhost:3000)
