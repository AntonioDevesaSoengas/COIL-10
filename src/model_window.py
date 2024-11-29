from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QTextEdit, QWidget, QGroupBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ModelWindow(QMainWindow):
    def __init__(self, model_data):
        super().__init__()
        self.setWindowTitle("Model Details")
        self.setGeometry(100, 100, 800, 600)  # Adjusted size for better visualization

        # Main layout
        layout = QVBoxLayout()

        # Description section
        description_group = QGroupBox("Model Description")
        description_layout = QVBoxLayout()
        description_text = QTextEdit()
        description_text.setText(model_data.get('description', 'No description available.'))
        description_text.setReadOnly(True)
        description_layout.addWidget(description_text)
        description_group.setLayout(description_layout)
        layout.addWidget(description_group)

        # Graph section
        graph_group = QGroupBox("Regression Graph")
        graph_layout = QVBoxLayout()

        # Check if graph data is available
        if 'graph' in model_data and model_data['graph']:
            canvas = FigureCanvas(model_data['graph'])
            graph_layout.addWidget(canvas)
        else:
            graph_label = QLabel("Graph not available.")
            graph_label.setAlignment(Qt.AlignCenter)
            graph_layout.addWidget(graph_label)

        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

        # Metrics section (Formula, MSE, R²)
        metrics_group = QGroupBox("Model Metrics")
        metrics_layout = QVBoxLayout()

        formula_label = QLabel(f"Formula: {model_data.get('formula', 'N/A')}")
        formula_label.setAlignment(Qt.AlignLeft)
        metrics_layout.addWidget(formula_label)

        mse_label = QLabel(f"MSE: {model_data.get('mse', 'N/A')}")
        mse_label.setAlignment(Qt.AlignLeft)
        metrics_layout.addWidget(mse_label)

        r_squared_label = QLabel(f"R²: {model_data.get('r_squared', 'N/A')}")
        r_squared_label.setAlignment(Qt.AlignLeft)
        metrics_layout.addWidget(r_squared_label)

        metrics_group.setLayout(metrics_layout)
        layout.addWidget(metrics_group)

        # Main container
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
