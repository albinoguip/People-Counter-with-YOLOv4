# YOLOv4 People Detection and Tracking Service

Este projeto implementa um serviço de inferência utilizando FastAPI para detecção e contagem de pessoas em vídeos usando o modelo YOLOv4. O serviço principal (S1) recebe frames dos vídeos enviados por dois clientes (S2 e S3), realiza a detecção de pessoas e rastreia cada pessoa individualmente para garantir que cada pessoa seja contada apenas uma vez.

## Estrutura do Projeto

- `server/`: Contém o código do serviço FastAPI que realiza a inferência.
- `client/`: Contém o código dos clientes que enviam frames dos vídeos para o servidor.

## Pré-requisitos

- Docker
- Docker Compose

## Configuração

### Passos para Configurar e Executar o Projeto

1. Clone este repositório:
    ```sh
    git clone https://github.com/albinoguip/People-Counter-with-YOLOv4.git
    cd seu_repositorio
    ```

2. Coloque os vídeos `01.mp4` e `02.mp4` na pasta `client1` e `client2`:
    ```sh
    cp caminho/para/01.mp4 client1/01.mp4
    cp caminho/para/02.mp4 client2/02.mp4
    ```

3. Coloque os arquivos `yolov4.cfg` e `yolov4.weights` na pasta `server`:
    ```sh
    cp caminho/para/yolov4.cfg server/yolov4.cfg
    cp caminho/para/yolov4.weights server/yolov4.weights
    ```

4. Construa e inicie os contêineres Docker:
    ```sh
    docker-compose up --build
    ```

### Estrutura de Arquivos e Pastas

```plaintext
.
├── client
│   ├── Dockerfile
│   ├── client.py
│   ├── video1.mp4
│   └── video2.mp4
├── server
│   ├── Dockerfile
│   ├── main.py
│   ├── yolov4.cfg
│   └── yolov4.weights
├── docker-compose.yml
└── README.md
