TEST_SIZE = 0.2
RANDOM_STATE = 42
GENE_SPACE = {
    "neurons": [8, 16, 32, 64],
    "dropout": [0.1, 0.2, 0.3, 0.4],
    "learning_rate": [0.001, 0.0005, 0.0001],
    "batch_size": [16, 32, 64],
    "epochs": [30, 50, 100]
}
GA_CONFIG = {
    "population": [20, 30, 40],
    "crossover": [0.70, 0.80, 0.60],
    "mutation": [0.20, 0.30, 0.10],
}
GENERATIONS=10
DEFAULT_MODEL_PARAMETER = {
    "neurons": 16,
    "dropout": 0.2,
    "learning_rate": 0.001,
    "epochs": 50,
    "batch_size": 32,
    "validation_split": 0.2
}
GA_MODEL_PARAMETER = {
    "neurons": 16,
    "dropout": 0.1,
    "learning_rate": 0.0005,
    "epochs": 100,
    "batch_size": 16,
    "validation_split": 0.2
}
FEATURES = [
    "Gravidez",
    "Glicose",
    "Pressão Arterial",
    "Espessura da Pele",
    "Insulina",
    "IMC",
    "Função Diabética",
    "Idade"
]
FEATURES_DF = [
    "Pregnancies",
    "Glucose",
    "BloodPressure",
    "SkinThickness",
    "Insulin",
    "BMI",
    "DiabetesPedigreeFunction",
    "Age",
]