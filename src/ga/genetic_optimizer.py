from src.monitoring import logging
import os
import random
import numpy as np
import tensorflow as tf
from deap import base, creator, tools
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

class GeneticOptimizer:

    def __init__(
        self,
        X_train,
        y_train,
        gene_space,
        population_size=20,
        generations=10,
        crossover_prob=0.7,
        mutation_prob=0.2,
        validation_size=0.2,
        random_state=42,
    ):
        self.logger = logging.getLogger(__name__)
        self._set_global_seed(random_state)

        self.gene_space = gene_space
        self.population_size = population_size
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob

        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            X_train,
            y_train,
            test_size=validation_size,
            stratify=y_train,
            random_state=random_state
        )

        self.toolbox = None
        self.population = None

        self.early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        )

    @staticmethod
    def _set_global_seed(seed):
        os.environ["PYTHONHASHSEED"] = str(seed)
        random.seed(seed)
        np.random.seed(seed)
        tf.random.set_seed(seed)

    def _build_model(self, neurons, dropout, learning_rate):
        tf.keras.backend.clear_session()

        model = Sequential([
            Dense(neurons, activation="relu", input_shape=(self.X_train.shape[1],)),
            Dropout(dropout),
            Dense(neurons // 2, activation="relu"),
            Dense(1, activation="sigmoid")
        ])

        model.compile(
            optimizer=tf.keras.optimizers.legacy.Adam(
                learning_rate=learning_rate
            ),
            loss="binary_crossentropy"
        )
        return model

    def _fitness(self, individual):
        neurons, dropout, lr, batch, epochs = individual
        scores = []

        for _ in range(3):  # anti-ruído
            model = self._build_model(
                neurons=int(neurons),
                dropout=float(dropout),
                learning_rate=float(lr)
            )

            model.fit(
                self.X_train,
                self.y_train,
                epochs=int(epochs),
                batch_size=int(batch),
                validation_data=(self.X_val, self.y_val),
                callbacks=[self.early_stopping],
                verbose=0
            )

            preds = (model.predict(self.X_val) > 0.5).astype(int)

            acc = accuracy_score(self.y_val, preds)
            recall = recall_score(self.y_val, preds)
            f1 = f1_score(self.y_val, preds)

            score = (0.4 * recall) + (0.4 * f1) + (0.2 * acc)
            scores.append(score)

        return (np.mean(scores),)

    def _mutate(self, individual):
        for i, key in enumerate(self.gene_space.keys()):
            if random.random() < self.mutation_prob:
                individual[i] = random.choice(self.gene_space[key])
        return individual,

    def _setup_deap(self):
        if not hasattr(creator, "FitnessMax"):
            creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        if not hasattr(creator, "Individual"):
            creator.create("Individual", list, fitness=creator.FitnessMax)

        self.toolbox = base.Toolbox()

        for key in self.gene_space:
            self.toolbox.register(key, random.choice, self.gene_space[key])

        self.toolbox.register(
            "individual",
            tools.initCycle,
            creator.Individual,
            tuple(getattr(self.toolbox, k) for k in self.gene_space),
            n=1
        )

        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("evaluate", self._fitness)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", self._mutate)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def run(self, verbose=True):
        self._setup_deap()
        self.population = self.toolbox.population(n=self.population_size)

        for ind in self.population:
            ind.fitness.values = self.toolbox.evaluate(ind)

        for gen in range(self.generations):
            offspring = self.toolbox.select(self.population, len(self.population))
            offspring = list(map(self.toolbox.clone, offspring))

            for c1, c2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.crossover_prob:
                    self.toolbox.mate(c1, c2)
                    del c1.fitness.values, c2.fitness.values

            for mutant in offspring:
                if random.random() < self.mutation_prob:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid = [ind for ind in offspring if not ind.fitness.valid]
            for ind in invalid:
                ind.fitness.values = self.toolbox.evaluate(ind)

            self.population[:] = offspring

            if verbose:
                best = tools.selBest(self.population, 1)[0]
                self.logger.info(f"Geração {gen+1}/{self.generations} | Fitness: {best.fitness.values[0]:.4f}")

    def get_best_params(self):
        best = tools.selBest(self.population, 1)[0]
        return dict(zip(self.gene_space.keys(), best)) | {
            "fitness": best.fitness.values[0]
        }