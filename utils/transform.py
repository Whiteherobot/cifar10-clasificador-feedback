import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import joblib
import os

NUMERIC_COLS = None
SCALER_PATH = os.path.join('models', 'scaler.joblib')
IMG_TRANSFORM_PATH = os.path.join('models', 'transform_images.joblib')


def build_transform_pipeline(df: pd.DataFrame, numeric_cols=None):
    """Crea y ajusta un imputador y escalador para columnas numéricas.
    Devuelve el imputador, el escalador y la lista de columnas numéricas usadas.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    imputer.fit(df[numeric_cols])
    scaler.fit(imputer.transform(df[numeric_cols]))
    return imputer, scaler, numeric_cols


def transform_data(df: pd.DataFrame, imputer=None, scaler=None, fit=False):
    """Transforma el DataFrame para entrenamiento/predicción.

    Args:
        df: DataFrame original.
        imputer: SimpleImputer ajustado (opcional).
        scaler: StandardScaler ajustado (opcional).
        fit: Si True, ajusta imputer y scaler a `df` y los devuelve.

    Returns:
        X: matriz de características transformadas (numpy array).
        y: array objetivo o None si no existe la columna `maturity_level`.
        imputer, scaler: objetos usados (si fit=True o si se pasaron como None).
    """
    df_proc = df.copy()
    # Suponemos que la columna objetivo se llama 'maturity_level' si existe
    y = None
    if 'maturity_level' in df_proc.columns:
        y = df_proc['maturity_level'].values
        df_proc = df_proc.drop(columns=['maturity_level'])

    # Detectar columnas numéricas simples
    numeric_cols = df_proc.select_dtypes(include=[np.number]).columns.tolist()

    if imputer is None or scaler is None:
        imputer, scaler, numeric_cols = build_transform_pipeline(df_proc, numeric_cols=numeric_cols)

    X_num = imputer.transform(df_proc[numeric_cols])
    X_scaled = scaler.transform(X_num)

    if fit:
        # guardar scaler para reutilizar en producción
        os.makedirs('models', exist_ok=True)
        joblib.dump({'imputer': imputer, 'scaler': scaler, 'numeric_cols': numeric_cols}, SCALER_PATH)
        return X_scaled, y, imputer, scaler

    return X_scaled, y


def load_transformer(path=None):
    """Carga el imputer+scaler guardado por `transform_data(..., fit=True)`"""
    path = path or SCALER_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el transformador guardado en {path}")
    arte = joblib.load(path)
    return arte['imputer'], arte['scaler'], arte['numeric_cols']


def transform_data_images(X, y=None, normalize=True, flatten=True, fit=False):
    """Transformación simple para datasets de imágenes.

    Args:
        X: numpy array con imágenes (N,H,W,C) o (N,H,W) 
        y: etiquetas (opcional)
        normalize: si True divide por 255.0
        flatten: si True aplana imágenes a (N, H*W*C)
        fit: si True guarda el esquema de transformación en `models/transform_images.joblib`.

    Returns:
        X_proc: numpy array transformado
        y: etiquetas (si se pasaron)
    """
    X_proc = X.astype('float32')
    if normalize:
        X_proc = X_proc / 255.0

    transform_info = {'normalize': normalize, 'orig_shape': X_proc.shape}

    if flatten:
        X_proc = X_proc.reshape((X_proc.shape[0], -1))
        transform_info['flatten'] = True
        transform_info['flat_dims'] = X_proc.shape[1]
    else:
        transform_info['flatten'] = False

    if fit:
        os.makedirs('models', exist_ok=True)
        joblib.dump(transform_info, IMG_TRANSFORM_PATH)
        return X_proc, y, transform_info

    return X_proc, y


def load_image_transformer(path=None):
    path = path or IMG_TRANSFORM_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"No existe el transformador de imágenes en {path}")
    return joblib.load(path)
