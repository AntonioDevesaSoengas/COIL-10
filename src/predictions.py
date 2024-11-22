class PredictionHandler:
    def __init__(self, model, input_columns):
        """
        Inicializa el manejador de predicciones.
        :param model: Modelo de regresión disponible (creado o cargado).
        :param input_columns: Lista de nombres de las variables de entrada.
        """
        self.model = model
        self.input_columns = input_columns

    def predict(self, input_values):
        """
        Realiza una predicción utilizando el modelo y los valores de entrada proporcionados.
        :param input_values: Lista de valores numéricos para las variables de entrada.
        :return: Valor predicho por el modelo.
        """
        if not self.model:
            raise ValueError("No hay un modelo disponible para realizar predicciones.")

        if len(input_values) != len(self.input_columns):
            raise ValueError("El número de valores de entrada no coincide con las variables esperadas.")

        return self.model.predict([input_values])[0]
