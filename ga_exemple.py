from src.logger import logging
from src.data_loader import load_data
from src.config import TEST_SIZE, RANDOM_STATE, GENE_SPACE, GA_CONFIG, GENERATIONS
from src.genetic_optimizer import GeneticOptimizer

logger = logging.getLogger(__name__)

file_path = './diabetes.csv'

logger.info("Iniciando o aplicativo")

logger.info(f"Lendo on dataset no caminho: {file_path} ...")

X_train, X_test, y_train, y_test = load_data(file_path, TEST_SIZE, RANDOM_STATE)

logger.info(f"Lendo on dataset no caminho: {file_path} ...(OK)")

populations = GA_CONFIG["population"]
crossovers = GA_CONFIG["crossover"]
mutations = GA_CONFIG["mutation"]



for i in range(3):
    logger.info(f"=============== Iniciando o experimento {i + 1} ===============")
    logger.info(f"Configurações do experimento {i + 1}:")
    logger.info(f"   População: {populations[i]}")
    logger.info(f"   Cruzamento: {crossovers[i]}")
    logger.info(f"   Mutação: {mutations[i]}")
    
    optimizer = GeneticOptimizer(
        X_train,
        y_train,
        gene_space=GENE_SPACE,
        population_size=populations[i],
        generations=GENERATIONS,
        crossover_prob=crossovers[i],
        mutation_prob=mutations[i]
    )

    optimizer.run()
    best_params = optimizer.get_best_params()

    logger.info(f"Para o experimento {i + 1} os melhores parametros encontrados foram:")
    
    neurons = best_params["neurons"]
    dropout = best_params["dropout"]
    learning_rate = best_params["learning_rate"]
    batch_size = best_params["batch_size"]
    epochs = best_params["epochs"]
    fitness = best_params["fitness"]

    logger.info(f"   neurons: {neurons}")
    logger.info(f"   dropout: {dropout}")
    logger.info(f"   learning_rate: {learning_rate}")
    logger.info(f"   batch_size: {batch_size}")
    logger.info(f"   epochs: {epochs}")
    logger.info(f"   fitness: {fitness}")
    
    logger.info(f"=============== Finalizando o experimento {i + 1} ===============")

logger.info("Finalizando o aplicativo")