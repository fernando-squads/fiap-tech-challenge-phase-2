# TECH CHALLENGE FASE 2

O Tech Challenge é o projeto que engloba o conhecimento adquirido em todas as disciplinas da fase.
Este projeto foi criado utilizando [Python](https://www.python.org/).

## Scripts disponíveis

No diretório do projeto, você pode executar:

### `python3 -m venv env`

O Ambiente Virtual Python (VENV) é usado para executar e testar scripts com diferentes versões ou dependências em um ambiente específico. Os scripts contidos nesse ambiente são todos scripts Python, que podem ser visualizados em "Scripts" na barra de navegação à esquerda do Automation Gateway.

### `source env/bin/activate`

Usar o comando `source venv/bin/activate` enquanto estiver nesse diretório ativará o ambiente virtual.

### `pip install <package_name>`

O comando `pip install` é usado para instalar pacotes de software para Python a partir do Índice de Pacotes Python (PyPI) ou de outros repositórios de pacotes. O pip é o gerenciador de pacotes padrão para Python e está incluído na maioria das distribuições modernas do Python.

### `pip freeze > requirements.txt`

Este comando é usado para criar um arquivo chamado requirements.txt que lista todos os pacotes Python instalados no ambiente atual, juntamente com suas versões específicas.

### `python my_script.py`

O comando `python my_script.py` é usado para executar um programa Python a partir da linha de comando. A extensão de arquivo `.py` é a convenção padrão para salvar arquivos que contêm código-fonte Python.

## Execute o projeto em sua máquina

### `Execute o comando`
```shell script
uvicorn src.api.predict_api:app --reload
```

### `Teste com Swagger`
Abra seu navegador e cole o URL: http://127.0.0.1:8000/docs

### `Teste com Curl`
No terminal, execute o código abaixo
```shell script
curl -X 'POST' \
  'http://127.0.0.1:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "Pregnancies": 6,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 168,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 50
}'
```
## Executar testes automatizados
### `Execute o comando`
```shell script
pytest
```