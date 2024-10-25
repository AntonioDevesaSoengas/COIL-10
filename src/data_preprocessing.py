from PyQt5.QtWidgets import QMessageBox, QInputDialog
from sklearn.impute import SimpleImputer

def detect_missing_values(df):
    missing_data = df.isnull().sum()
    if missing_data.sum() == 0:
        message = "No hay valores inexistentes. El dataset está completo."
    else:
        message = "--- Detección de Valores Inexistentes ---\n"
        message += f"Valores inexistentes por columna:\n{missing_data[missing_data > 0]}"
    return message

def remove_missing_values(viewer):
    if viewer.df is not None:
        viewer.df = viewer.df.dropna()
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(viewer, "Éxito", "Filas con valores inexistentes eliminadas.")

def fill_with_mean(viewer):
    if viewer.df is not None:
        numeric_cols = viewer.df.select_dtypes(include=['number']).columns  # NUEVO: Solo aplicar a columnas numéricas
        imputer = SimpleImputer(strategy='mean')
        viewer.df[numeric_cols] = imputer.fit_transform(viewer.df[numeric_cols])
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(viewer, "Éxito", "Valores inexistentes rellenados con la media en columnas numéricas.")

def fill_with_median(viewer):
    if viewer.df is not None:
        numeric_cols = viewer.df.select_dtypes(include=['number']).columns  # NUEVO: Solo aplicar a columnas numéricas
        imputer = SimpleImputer(strategy='median')
        viewer.df[numeric_cols] = imputer.fit_transform(viewer.df[numeric_cols])
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(viewer, "Éxito", "Valores inexistentes rellenados con la mediana en columnas numéricas.")

def fill_with_constant(viewer):
    value, ok = QInputDialog.getDouble(viewer, "Rellenar con un Valor Constante", "Introduce el valor numérico para rellenar:")
    if ok and viewer.df is not None:
        numeric_cols = viewer.df.select_dtypes(include=['number']).columns  # NUEVO: Solo aplicar a columnas numéricas
        imputer = SimpleImputer(strategy='constant', fill_value=value)
        viewer.df[numeric_cols] = imputer.fit_transform(viewer.df[numeric_cols])
        viewer.display_data_in_table(viewer.df)
        QMessageBox.information(viewer, "Éxito", "Valores inexistentes rellenados con el valor constante.")