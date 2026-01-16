from src.monitoring import logging
from src.data import load_data
from src.config import TEST_SIZE, RANDOM_STATE, GA_MODEL_PARAMETER
from src.model import build_model
from src.model import compale_and_save

logger = logging.getLogger(__name__)

file_path = './src/data/diabetes.csv'

logger.info("Iniciando o aplicativo")

logger.info(f"Lendo on dataset no caminho: {file_path} ...")

X_train, X_test, y_train, y_test, scaler = load_data(file_path, TEST_SIZE, RANDOM_STATE)

logger.info(f"Lendo on dataset no caminho: {file_path} ...(OK)")

neurons = GA_MODEL_PARAMETER["neurons"]
dropout = GA_MODEL_PARAMETER["dropout"]
learning_rate = GA_MODEL_PARAMETER["learning_rate"]
epochs = GA_MODEL_PARAMETER["epochs"]
batch_size = GA_MODEL_PARAMETER["batch_size"]
validation_split = GA_MODEL_PARAMETER["validation_split"]

model = build_model(X_train.shape[1], neurons, dropout, learning_rate)
compale_and_save(
    model,
    X_train,
    y_train,
    epochs,
    batch_size,
    validation_split,
    X_test,
    y_test,
    scaler
)