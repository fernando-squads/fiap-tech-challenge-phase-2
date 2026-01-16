from src.monitoring import logging
from src.data import load_data
from src.config import TEST_SIZE, RANDOM_STATE, DEFAULT_MODEL_PARAMETER, GA_MODEL_PARAMETER
from src.model import build_model
from src.model import predict

logger = logging.getLogger(__name__)

def test_compare_result_default_vs_ga():

    logger.info("Testando comparação de resultados entre processar o modelo com super parametros padrões e processar modelo com super parametros otimizados pelo algoritimo genetico")

    file_path = './src/data/diabetes.csv'

    logger.info("Iniciando o aplicativo")

    logger.info(f"Lendo o dataset no caminho: {file_path} ...")

    X_train, X_test, y_train, y_test, scaler = load_data(file_path, TEST_SIZE, RANDOM_STATE)

    logger.info(f"Lendo o dataset no caminho: {file_path} ...(OK)")


    default_neurons = DEFAULT_MODEL_PARAMETER["neurons"]
    default_dropout = DEFAULT_MODEL_PARAMETER["dropout"]
    default_learning_rate = DEFAULT_MODEL_PARAMETER["learning_rate"]
    default_epochs = DEFAULT_MODEL_PARAMETER["epochs"]
    default_batch_size = DEFAULT_MODEL_PARAMETER["batch_size"]
    default_validation_split = DEFAULT_MODEL_PARAMETER["validation_split"]

    logger.info(f"Construindo o modelo com informações padrões: {DEFAULT_MODEL_PARAMETER}")

    default_model = build_model(X_train.shape[1], default_neurons, default_dropout, default_learning_rate)

    logger.info("Construindo o modelo ...(OK)")

    logger.info("Iniciando predição com dados padrões")

    default_score = predict(
        default_model,
        X_train,
        y_train,
        default_epochs,
        default_batch_size,
        default_validation_split,
        X_test,
        y_test
    )

    logger.info(f"Predição com dados padrões realizada e com o seguinte score: {default_score}")

    ga_neurons = GA_MODEL_PARAMETER["neurons"]
    ga_dropout = GA_MODEL_PARAMETER["dropout"]
    ga_learning_rate = GA_MODEL_PARAMETER["learning_rate"]
    ga_epochs = GA_MODEL_PARAMETER["epochs"]
    ga_batch_size = GA_MODEL_PARAMETER["batch_size"]
    ga_validation_split = GA_MODEL_PARAMETER["validation_split"]

    logger.info(f"Construindo o modelo com informações geradas pelo algorito genético: {GA_MODEL_PARAMETER}")

    ga_model = build_model(X_train.shape[1], ga_neurons, ga_dropout, ga_learning_rate)

    logger.info("Construindo o modelo ...(OK)")

    logger.info("Iniciando predição com dados gerados pelo algoritimo genético")

    ga_score = predict(
        ga_model,
        X_train,
        y_train,
        ga_epochs,
        ga_batch_size,
        ga_validation_split,
        X_test,
        y_test
    )

    logger.info(f"Predição com dados padrões realizada e com o seguinte score: {ga_score}")

    logger.info("Finalizando o aplicativo")