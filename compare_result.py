from src.logger import logging
from src.data_loader import load_data
from src.config import TEST_SIZE, RANDOM_STATE, DEFAULT_MODEL_PARAMETER, GA_MODEL_PARAMETER
from src.model import build_model
from src.fitness import predict

logger = logging.getLogger(__name__)

file_path = './diabetes.csv'

logger.info("Iniciando o aplicativo")

logger.info(f"Lendo on dataset no caminho: {file_path} ...")

X_train, X_test, y_train, y_test = load_data(file_path, TEST_SIZE, RANDOM_STATE)

logger.info(f"Lendo on dataset no caminho: {file_path} ...(OK)")


default_neurons = DEFAULT_MODEL_PARAMETER["neurons"]
default_dropout = DEFAULT_MODEL_PARAMETER["dropout"]
default_learning_rate = DEFAULT_MODEL_PARAMETER["learning_rate"]
default_epochs = DEFAULT_MODEL_PARAMETER["epochs"]
default_batch_size = DEFAULT_MODEL_PARAMETER["batch_size"]
default_validation_split = DEFAULT_MODEL_PARAMETER["validation_split"]

default_model = build_model(X_train.shape[1], default_neurons, default_dropout, default_learning_rate)
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

logger.info(f"default_score: {default_score}")

ga_neurons = GA_MODEL_PARAMETER["neurons"]
ga_dropout = GA_MODEL_PARAMETER["dropout"]
ga_learning_rate = GA_MODEL_PARAMETER["learning_rate"]
ga_epochs = GA_MODEL_PARAMETER["epochs"]
ga_batch_size = GA_MODEL_PARAMETER["batch_size"]
ga_validation_split = GA_MODEL_PARAMETER["validation_split"]

ga_model = build_model(X_train.shape[1], ga_neurons, ga_dropout, ga_learning_rate)
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

logger.info(f"ga_score: {ga_score}")