import os
import time
import joblib
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from utils.transform import transform_data_images, load_image_transformer

os.makedirs('data', exist_ok=True)
os.makedirs('models', exist_ok=True)

print('1) Preparación: cargar CIFAR-10 y transformar (si no existen artefactos)')
if not os.path.exists('data/processed_cifar10.npz'):
    try:
        from tensorflow.keras.datasets import cifar10
    except Exception as e:
        raise RuntimeError('TensorFlow no está disponible en el entorno') from e
    (X_train, y_train), (X_test, y_test) = cifar10.load_data()
    X = np.concatenate([X_train, X_test], axis=0)
    y = np.concatenate([y_train, y_test], axis=0).reshape(-1)
    # shuffle
    rng = np.random.default_rng(42)
    idx = rng.permutation(X.shape[0])
    X = X[idx]
    y = y[idx]
    # transform and save
    X_proc, y_proc, tinfo = transform_data_images(X, y, normalize=True, flatten=True, fit=True)
    np.savez_compressed('data/processed_cifar10.npz', X=X_proc, y=y_proc)
    X_hist, X_new, y_hist, y_new = train_test_split(X_proc, y_proc, test_size=0.2, random_state=42, stratify=y_proc)
    np.savez_compressed('data/historical.npz', X=X_hist, y=y_hist)
    np.savez_compressed('data/new_samples.npz', X=X_new, y=y_new)
    print('Prepared and saved processed datasets.')
else:
    print('Processed dataset already exists; skipping preparation.')

print('\n2) Entrenamiento incremental: cargar datos y reentrenar modelo (máx 2 epochs)')
arr_h = np.load('data/historical.npz')
arr_n = np.load('data/new_samples.npz')
X_hist, y_hist = arr_h['X'], arr_h['y']
X_new, y_new = arr_n['X'], arr_n['y']
X_all = np.concatenate([X_hist, X_new], axis=0)
y_all = np.concatenate([y_hist, y_new], axis=0)
X_train, X_val, y_train, y_val = train_test_split(X_all, y_all, test_size=0.2, random_state=42, stratify=y_all)

# Load existing model if any
model_files = [p for p in os.listdir('models') if p.startswith('model_') and p.endswith('.joblib') and '_meta' not in p]
model = None
if model_files:
    model_files = sorted(model_files, key=lambda p: os.path.getmtime(os.path.join('models', p)))
    model = joblib.load(os.path.join('models', model_files[-1]))
    print('Loaded existing model:', model_files[-1])
else:
    # scikit-learn recent versions use 'log_loss' as the loss name
    model = SGDClassifier(loss='log_loss', max_iter=1, tol=None, warm_start=True, random_state=42)
    print('Initialized new SGDClassifier for partial_fit')

epochs = 2
classes = np.unique(y_all)
for ep in range(epochs):
    if hasattr(model, 'partial_fit'):
        if ep == 0 and not hasattr(model, 'classes_'):
            model.partial_fit(X_train, y_train, classes=classes)
        else:
            model.partial_fit(X_train, y_train)
    else:
        model.fit(X_train, y_train)
    y_tr_pred = model.predict(X_train)
    y_val_pred = model.predict(X_val)
    print(f'Epoch {ep+1}/{epochs} - Train acc: {accuracy_score(y_train, y_tr_pred):.4f} - Val acc: {accuracy_score(y_val, y_val_pred):.4f}')

# Save model
ts = int(time.time())
model_path = f'models/model_{ts}.joblib'
joblib.dump(model, model_path)
meta = {'version': ts, 'trainer': 'SGDClassifier', 'epochs_trained': epochs, 'timestamp': ts}
joblib.dump(meta, f'models/model_{ts}_meta.joblib')
print('Saved model to', model_path)

print('\n3) Predicciones sobre new_samples usando el modelo guardado')
# Load newest model explicitly
model = joblib.load(model_path)
X_test = X_new
y_test = y_new
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print('Accuracy on new_samples:', acc)
print('\nClassification report (first 10 classes):')
print(classification_report(y_test, y_pred, digits=4, zero_division=0))

# Save predictions
np.savez_compressed('data/predictions.npz', y_true=y_test, y_pred=y_pred)
print('Saved predictions to data/predictions.npz')

print('\nPipeline completed successfully.')
