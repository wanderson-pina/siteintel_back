# Minha API

Este Projeto se refere a um Modelo de Predição de Potabilidade de Amostras de Agua.

O objetivo aqui é ilustrar as orientações para a execução do código.

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
É necessário ir ao diretório raiz (Comando cd + diretório), pelo terminal, para poder executar os comandos descritos abaixo.

> É indicado o uso de ambientes virtuais:
    No Ambiente Windows foi utilizado o comando (python3 -m venv env), para a criação do ambiente virtual, e o comando ( env/scripts/activate), para ativar o ambiente virtual.

```
Instalar os Requirements para a execução do código:
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

flask run --reload



```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.
