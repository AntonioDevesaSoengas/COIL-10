import statsmodels.formula.api as smf
import pandas as pd
from import_files import *

# Importo mi archivo
data = import_data(r"C:\Users\Alejandro\Downloads\housing.csv")

# Visualiza las primeras filas del DataFrame para verificar que los datos se hayan cargado correctamente
print(data.head())
