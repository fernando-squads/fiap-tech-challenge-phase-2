import tensorflow as tf
from sklearn.metrics import accuracy_score, recall_score, f1_score
import numpy as np

def predict(model, X_train, y_train, epochs, batch, validation_split, X_val, y_val):
    early_stopping = tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True
        )
    model.fit(
        X_train,
        y_train,
        epochs=epochs,
        batch_size=batch,
        validation_split=validation_split,
        validation_data=(X_val, y_val),
        callbacks=[early_stopping],
        verbose=0
    )

    preds = (model.predict(X_val) > 0.5).astype(int)

    accuracy = accuracy_score(y_val, preds)
    recall = recall_score(y_val, preds)
    f1 = f1_score(y_val, preds)

    score = {
        "accuracy": accuracy,
        "recall": recall,
        "f1": f1,
        "fitness": np.mean([
            accuracy,
            recall,
            f1
        ])
    }

    return score