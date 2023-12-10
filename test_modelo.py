from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# To run: pytest -v test_modelo.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros    
url_dados = "database/water_golden.csv.csv"
colunas = ['aph', 'hard', 'soli', 'chlo', 'sulf', 'condu', 'organ', 'triha', 'turbi' , 'class']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]
    

 
# Método para testar modelo KNN a partir do arquivo correspondente
def test_modelo_knn():
    # Importando modelo de KNN
    knn_path = 'ml_model/modelwaterb.pkl'
    modelo_knn = Model.carrega_modelo(knn_path)


     # Obtendo as métricas do KNN
    acuracia_knn, recall_knn, precisao_knn, f1_knn = avaliador.avaliar(modelo_knn, X, Y)
    
    # Testando as métricas do KNN
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_knn >= 0.55
    assert recall_knn >= 0.5 
    assert precisao_knn >= 0.5 
    assert f1_knn >= 0.5 