import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout

def build_model(input_dim, neurons, dropout, learning_rate):
    tf.keras.backend.clear_session()

    model = Sequential([
        Dense(neurons, activation="relu", input_shape=(input_dim,)),
        Dropout(dropout),
        Dense(neurons // 2, activation="relu"),
        Dense(1, activation="sigmoid")
    ])

    model.compile(
        #optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        optimizer=tf.keras.optimizers.legacy.Adam(
            learning_rate=learning_rate
        ),
        loss="binary_crossentropy",
        #metrics=["accuracy"]
    )

    return model