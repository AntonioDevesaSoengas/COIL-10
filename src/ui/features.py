# Third-party libraries.
import pandas as pd
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QLabel, QTableView,
    QRadioButton, QListWidget, QAbstractItemView, QPushButton,
    QFileDialog, QHeaderView, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Local Libraries.
from data_preparation.import_files import import_data
from data_preparation.data_preprocessing import (
    detect_missing_values, fill_with_constant, fill_with_mean,
    fill_with_median, remove_missing_values, show_missing_values
)
from utils.table import Table
from utils.helpers import LabelHelper, ButtonHelper, LayoutHelper
from ui.welcome_window import WelcomeWindow


class DataViewer(QWidget):
    """
    QWidget subclass for loading, preprocessing, and analyzing datasets.

    Provides UI components for loading data, handling missing values, doing
    regression analysis, and managing model details using helper classes.

    Attributes:
        df (pd.DataFrame): Loaded dataset.
        last_file_path (str): Path of the last loaded file.
        input_columns (list): Columns used as input features.
        output_column (list): Columns used as output targets.
        empty_values (bool): Indicates presence of empty values.
        data_table (QTableView): Table view displaying the dataset.
        nan_solved (bool): Indicates if NaN values are handled.
        move (int): Used for navigation or state management.
    """

    def __init__(self):
        """
        Initialize the DataViewer widget.

        Sets up the initial state and initializes the user interface.
        """
        super().__init__()
        self.df = None
        self.last_file_path = None
        self.input_columns = []
        self.output_column = []
        self.empty_values = False
        self.data_table = None
        self.nan_solved = False
        self.move = 1
        self.initUI()

    def initUI(self):
        """
        Set up the user interface components.

        Initializes layouts, helper instances, and sets up various sections
        of the UI including the welcome window, steps guide, and navigation
        buttons.
        """
        self.main_layout = QVBoxLayout()
        self.spacer_layout = QHBoxLayout()
        self.spacer = QSpacerItem(0, 0)
        self.NBlayout = QHBoxLayout()
        self.button = ButtonHelper()
        self.layout = LayoutHelper()
        self.label = LabelHelper()
        self.setup_welcome_window()
        self.setup_steps_guide()
        self.setup_first_step()
        self.setup_nan_step()
        self.setup_regression_step()
        self.setup_model_details_step()
        self.setup_navigation_buttons()
        self.finalize_layout()

    def setup_welcome_window(self):
        """
        Initialize and display the welcome window.

        Creates an instance of WelcomeWindow and connects its start signal
        to the delete_welcome method to transition from the welcome screen.
        """
        self.welcome_window = WelcomeWindow()
        self.welcome_window.start_clicked.connect(self.delete_welcome)

    def setup_steps_guide(self):
        """
        Create and configure the steps guide section.

        Sets up labels and separators to guide the user through the program's
        various steps. This includes creating labels for each step and adding
        them to the layout with appropriate styling.
        """
        self.steps_layout = QVBoxLayout()
        self.steps_label = LabelHelper.create_label(
            parent=self,
            font=("Times New Roman", 12),
            text="STEPS:",
            alignment=Qt.AlignLeft,
            bold=True
        )

        self.steps_separator = self.layout.add_separator(
            "horizontal",
            None,
            False
        )

        self.first_step = LabelHelper.create_label(
            font=("Arial", 9),
            parent=self,
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.second_step = LabelHelper.create_label(
            font=("Arial", 9),
            parent=self,
            alignment=Qt.AlignLeft,
            italic=True
        )

        self.third_step = LabelHelper.create_label(
            font=("Arial", 9),
            parent=self,
            alignment=Qt.AlignLeft,
            italic=True
        )
        self.third_step.setMinimumWidth(250)

        self.layout_separator = self.layout.add_separator(
            "vertical",
            None,
            False
        )

        items_steps_layout = [
            self.steps_label,
            self.steps_separator,
            self.first_step,
            self.second_step,
            self.third_step
        ]
        self.layout.add_widget(self.steps_layout, items_steps_layout)
        self.steps_layout.setAlignment(Qt.AlignTop)

        # Hide the complete steps layout initially.
        self.layout.layout_visibility(True, False, self.steps_layout)

    # FIRST STEP: Open file and display data.
    def setup_first_step(self):
        """
        Set up the first step in the steps guide.

        Initializes UI components for loading datasets, models, choosing
        another file, displaying the file path, and showing the data table.
        """
        self.first_step_layout = QVBoxLayout()

        # Button to load dataset.
        self.load_button = self.button.add_QPushButton(
            '📂 Load Dataset',
            "Arial Black",
            12,
            243,
            None,
            False,
            background_color="green",
            color="white",
            padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(
            self.load_button, "darkgreen", "lightgrey"
        )
        self.load_button.clicked.connect(self.open_file_dialog)

        # Button to load model.
        self.load_model_button = self.button.add_QPushButton(
            '📦 Load Model',
            "Arial Black",
            12,
            243,
            None,
            False,
            background_color="blue",
            color="white",
            padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(
            self.load_model_button, "darkblue", "lightgrey"
        )
        self.load_model_button.clicked.connect(self.open_model_dialog)

        # Button to choose another file.
        self.back_button = self.button.add_QPushButton(
            "🔄️ Choose Another File",
            "Arial Black",
            12,
            262,
            None,
            False,
            background_color="orange",
            color="white",
            padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(
            self.back_button, "darkorange", "lightgrey"
        )
        self.back_button.clicked.connect(self.clear_table_and_choose_file)

        # Label to display the loaded file path.
        self.file_label = LabelHelper.create_label(
            parent=self,
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )
        self.file_label.setVisible(False)

        # Table to display the data.
        self.table_view = QTableView()
        self.table_view.setFont(QFont("Arial", 10))
        self.table_view.setVisible(False)

        # Add widgets to the first step layout.
        items_setup_first_step = [
            self.load_button,
            self.load_model_button,
            self.back_button,
            self.file_label,
            self.table_view
        ]
        self.layout.add_widget(self.first_step_layout, items_setup_first_step)

    # SECOND STEP: Nan values.
    def setup_nan_step(self):
        """
        Set up the NaN handling step in the steps guide.

        Initializes UI components for handling missing values (NaNs) in the 
        dataset,including labels, separators, a drop-down menu for 
        preprocessing options,and a confirmation button to apply preprocessing.
        """
        self.nan_layout = QVBoxLayout()

        self.sep = self.layout.add_separator(
            "horizontal",
            None,
            False
        )

        self.nan_label = self.label.create_label(
            parent=self,
            font=("Arial", 12),
            alignment=Qt.AlignLeft,
            bold=True,
        )

        self.nan_values = self.label.create_label(
            parent=self,
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        self.separator = self.layout.add_separator("horizontal", None, False)

        # Drop-down menu for pre-processing options.
        self.option_label = self.label.create_label(
            self,
            "Choose an option for preprocessing NaN values:",
            font=("Arial", 8),
            alignment=Qt.AlignLeft
        )
        items = [
            "Select an option...",
            "🗑️ Remove Rows with Missing Values",
            "📊 Fill with Mean",
            "📊 Fill with Median",
            "✏️ Fill with a Constant Value"
        ]
        self.preprocessing_options = self.button.add_QComboBox(
            items,
            None,
            None,
            False
        )
        self.preprocessing_options.currentIndexChanged.connect(
            self.preprocessing_button
        )

        # Confirmation button to apply pre-processing.
        self.apply_button = self.button.add_QPushButton(
            "🟢 Apply Preprocessing",
            "Arial Black",
            8,
            None,
            None,
            False,
            enabled=False
        )
        self.button.set_QPushButton_hoverStyle(
            self.apply_button,
            "darkgreen",
            "lightgrey"
        )
        self.apply_button.clicked.connect(
            self.confirm_preprocessing
        )

        # Add widgets to the NaN handling layout.
        widgets = [
            self.sep,
            self.nan_label,
            self.separator,
            self.option_label,
            self.preprocessing_options,
            self.apply_button
        ]
        self.layout.add_widget(self.nan_layout, widgets)

    # THIRD STEP: Options for the linear regresion-model.
    def setup_regression_step(self):
        """
        Set up the regression analysis step in the steps guide.

        Initializes UI components for selecting the type of regression,
        choosing input features and target columns, and creating the
        regression model.
        """
        self.regresion_layout = QVBoxLayout()

        # Radio buttons to select the type of regression.
        self.radio_simple = QRadioButton("Simple Regression")
        self.radio_multiple = QRadioButton("Multiple Regression")
        self.radio_simple.setChecked(True)  # Default to simple regression
        self.radio_simple.toggled.connect(self.update_feature_selector)
        self.radio_multiple.toggled.connect(self.update_feature_selector)

        self.radio_simple.setVisible(False)
        self.radio_multiple.setVisible(False)

        self.radio_layout = QHBoxLayout()
        radio_button = [self.radio_simple, self.radio_multiple]
        self.layout.add_widget(self.radio_layout, radio_button)

        # Column selector (features).
        self.feature_label = QLabel("Input Columns (Features)")
        self.feature_selector = QListWidget(self)
        self.feature_selector.setSelectionMode(
            QAbstractItemView.SingleSelection
        )  # Default to single selection (simple regression)
        self.feature_selector.setVisible(False)
        self.feature_label.setVisible(False)

        # Simple selector for the output column (target).
        self.target_label = QLabel("Output Column (Target)")
        self.target_selector = QListWidget(self)
        self.target_selector.setSelectionMode(
            QAbstractItemView.SingleSelection
        )  # Allow single selection for the target
        self.target_selector.setVisible(False)
        self.target_label.setVisible(False)

        # Confirmation button.
        self.confirm_button = self.button.add_QPushButton(
            "✅ Confirm Selection",
            "Arial Black",
            10,
            None,
            None,
            False,
            background_color="lightgreen",
            color="lightblack",
            padding="5px"
        )
        self.button.set_QPushButton_hoverStyle(
            self.confirm_button,
            "green",
            "white"
        )
        self.confirm_button.clicked.connect(self.confirm_selection)

        # Create Regression Model Button.
        self.create_model_button = self.button.add_QPushButton(
            "📈 Create Regression Model",
            "Arial Black",
            10,
            None,
            None,
            False,
            background_color="lightblue",
            color="lightblack",
            padding="10px"
        )
        self.button.set_QPushButton_hoverStyle(
            self.create_model_button,
            "blue",
            "white"
        )
        self.create_model_button.clicked.connect(self.show_results)

        # Add widgets to the regression layout.
        widgets = [
            self.radio_layout,
            self.feature_label,
            self.feature_selector,
            self.target_label,
            self.target_selector,
            self.confirm_button,
            self.create_model_button
        ]
        self.layout.add_widget(self.regresion_layout, widgets)

    def setup_model_details_step(self):
        """
        Sets up the UI components to display a loaded regression model.
        """
        self.model_details_layout = QVBoxLayout()

        # Label for displaying the formula.
        self.formula_label = LabelHelper.create_label(
            parent=self,
            text="Model Formula: ",
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        # Label for displaying MSE.
        self.mse_label = LabelHelper.create_label(
            parent=self,
            text="MSE: ",
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        # Label for displaying R².
        self.r_squared_label = LabelHelper.create_label(
            parent=self,
            text="R²: ",
            font=("Arial", 10),
            alignment=Qt.AlignLeft
        )

        # Text box for model description.
        self.description_text = QTextEdit()
        self.description_text.setPlaceholderText("Loaded model description...")
        self.description_text.setReadOnly(True)

        # Add widgets to the layout.
        widgets = [
            self.formula_label,
            self.mse_label,
            self.r_squared_label,
            self.description_text
        ]
        self.layout.add_widget(self.model_details_layout, widgets)

        # Make the layout initially invisible.
        self.layout.layout_visibility(True, False, self.model_details_layout)

    def setup_navigation_buttons(self):
        """
        Set up the navigation buttons: Back and Next.
        """
        self.back_layout = QVBoxLayout()
        self.return_button = QPushButton("<- Back")
        self.return_button.clicked.connect(self.back)
        self.return_button.setVisible(False)
        self.back_layout.addWidget(self.return_button)
        self.back_layout.setAlignment(Qt.AlignLeft)

        # Next Button.
        self.next_layout = QVBoxLayout()
        self.next_button = QPushButton("Next ->")
        self.next_button.clicked.connect(self.next)
        self.next_button.setVisible(False)
        self.next_button.setEnabled(False)
        self.next_layout.addWidget(self.next_button)
        self.next_layout.setAlignment(Qt.AlignRight)

        nav_buttons = [self.back_layout, self.next_layout]
        self.layout.add_widget(self.NBlayout, nav_buttons)

        # Configure alignment for the "Next" and "Back" buttons.
        self.NBlayout.setAlignment(Qt.AlignBottom)

    def finalize_layout(self):
        """
        Finalize and apply the main layout to the widget.
        """
        layouts = [
            self.welcome_window,
            self.first_step_layout,
            self.nan_layout,
            self.regresion_layout,
            self.NBlayout
        ]

        self.layout.add_widget(self.main_layout, layouts)

        # Add spacers and finalize the window structure.
        items_spacer_layout = [
            self.steps_layout,
            self.layout_separator,
            self.main_layout
        ]
        self.layout.add_widget(self.spacer_layout, items_spacer_layout)
        self.setLayout(self.spacer_layout)

        # Configure the basic properties of the window.
        self.setWindowTitle('Dataset Viewer')
        self.setMinimumSize(800, 600)

    def open_file_dialog(self):
        """
        Opens file dialog to select a dataset file and load the selected data.

        Allows the user to choose a CSV, Excel, or SQLite database file. 
        If the selected file is the same as the previously loaded file, 
        prompts the user to confirm reloading the data.
        """
        # Open File Explorer with PyQt5's QFileDialog
        filters = (
            "CSV Files (*.csv);;"
            "Excel Files (*.xlsx *.xls);;"
            "SQLite Databases (*.sqlite *.db)"
        )
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            "",
            filters
        )
        if file_path:
            if self.last_file_path == file_path:
                # Show message and confirmation options if it's the same file
                WARNING_MESSAGE = (
                    "You are selecting the same file. You have already loaded."
                    "Do you want to load it again?"
                )
                result = QMessageBox.question(
                    self,
                    "Warning",
                    WARNING_MESSAGE,
                    QMessageBox.Yes | QMessageBox.No
                )
                if result == QMessageBox.No:
                    return
                elif result == QMessageBox.Yes:
                    self.load_data(file_path)  # Reload the dataset directly
            else:
                self.last_file_path = file_path
                self.file_label.setText(f'📂 Loaded File: {file_path}')
                self.load_data(file_path)

    def open_model_dialog(self):
        """
        Opens file dialog to load a model and display details in a new window.
        """
        from model_management.model_loader import ModelLoader
        from ui.model_window import ModelWindow

        # Create an instance of ModelLoader.
        model_loader = ModelLoader(self)
        model_data = model_loader.load_model_dialog()

        if model_data:
            try:
                # Open a new window to display the model details.
                self.model_window = ModelWindow(model_data)
                self.model_window.show()
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    (
                        "An error occurred while displaying the model details:"
                        f"{str(e)}"
                    )
                )

    def load_data(self, file_path):
        """
        Loads data from the specified file path and displays it in the table.
        """
        try:
            self.df = import_data(file_path)
            if self.df is not None and not self.df.empty:
                self.display_data_in_table(self.df)
                # Enable buttons if data is loaded correctly.
                self.file_label.setText(f'📂 Loaded File: {file_path}')
                detect_missing_values(self)
                self.populate_selectors(self.df)
            else:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "The file is empty or could not be loaded correctly."
                )
        except pd.errors.EmptyDataError:
            QMessageBox.critical(
                self,
                "Error",
                "The CSV file is empty. Please select another file."
            )
        except pd.errors.ParserError:
            QMessageBox.critical(
                self,
                "Error",
                "The CSV file is corrupt or has an invalid format."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not load the file: {str(e)}"
            )

    def display_loaded_model(self, model_data: dict) -> None:
        """
        Updates the UI to display details of a loaded model, 
        including its formula,metrics, and description. 
        It also hides the irrelevant sections of the interface.
        """
        try:
            # Ensure the regression step layout is displayed
            self.layout.layout_visibility(True, False, self.main_layout)
            self.layout.layout_visibility(
                True, True, self.model_details_layout)

            # Update labels and metrics
            self.formula_label.setText(f"Formula: {model_data['formula']}")
            self.mse_label.setText(f"MSE: {model_data.get('mse', 'N/A')}")
            self.r_squared_label.setText(
                f"R²: {model_data.get('r_squared', 'N/A')}"
            )
            self.description_text.setText(
                model_data.get('description', 'No description available.')
            )

            # Hide irrelevant sections
            self.load_button.setVisible(False)
            self.load_model_button.setVisible(False)
            self.back_button.setVisible(False)
            self.preprocessing_options.setVisible(False)
            self.apply_button.setVisible(False)
            self.feature_selector.setVisible(False)
            self.target_selector.setVisible(False)
            self.confirm_button.setVisible(False)
            self.create_model_button.setVisible(False)

            # Adjust steps guide
            self.steps_guide()
            self.label.edit_label(
                self.third_step,
                text="Model loaded successfully.",
                background_color="lightgreen",
                bold=True,
                padding="5px",
            )
            QMessageBox.information(
                self,
                "Success",
                "The model has been loaded and its details are now displayed."
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                (
                    "An error occurred while displaying the model details: "
                    f"{str(e)}"
                )
            )

    def display_data_in_table(self, data):
        """
        Displays the provided data in a table and updates the UI accordingly.
        """
        self.data_table = Table(self.df)
        self.table_view.setModel(self.data_table)

        # Show only the table and relevant elements.
        self.table_view.setVisible(True)

        # Show file path
        self.file_label.setVisible(True)
        self.load_button.setVisible(False)
        self.next_button.setEnabled(True)

        if self.move == 1:  # Only show the button in step 1.
            self.back_button.setVisible(True)
        else:  # Hide in later steps
            self.back_button.setVisible(False)

        # Adjust Table Size.
        self.table_view.resizeColumnsToContents()
        self.table_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        if self.width() > 1000:
            self.table_view.horizontalHeader().setSectionResizeMode(
                QHeaderView.Stretch
            )

    def populate_selectors(self, data):
        """
        Populates the selectors with available columns from the dataset.
        """
        # Clean up your current selectors.
        self.feature_selector.clear()
        self.target_selector.clear()

        # Add the available columns.
        self.feature_selector.addItems(data.columns)
        self.target_selector.addItems(data.columns)

        # Update feature selection based on the selected regression type.
        self.update_feature_selector()

    def update_feature_selector(self):
        """
        Updates selector's selection based on the selected regression type.
        """
        if self.radio_simple.isChecked():
            # Simple Regression: Only One Selection Allowed.
            self.feature_selector.setSelectionMode(
                QAbstractItemView.SingleSelection
            )
        else:
            # Multiple Regression: Multiple Choices Allowed.
            self.feature_selector.setSelectionMode(
                QAbstractItemView.MultiSelection
            )

    def confirm_selection(self):
        """
        Confirms the selected columns and updates the UI accordingly.
        """
        # Get feature selections.
        selected_features = [
            item.text() for item in self.feature_selector.selectedItems()
        ]
        self.input_columns = selected_features

        # Get target selection.
        selected_target = [
            item.text() for item in self.target_selector.selectedItems()
        ]
        self.output_column = selected_target

        if not selected_features or not selected_target:
            QMessageBox.warning(
                self,
                "Incomplete Selection",
                "You must select at least one input and output column."
            )
            return

        QMessageBox.information(
            self,
            "Selection Confirmed",
            (
                "You have selected input columns: "
                f"{', '.join(selected_features)} and output column: "
                f"{', '.join(selected_target)}."
            )
        )

    def clear_table_and_choose_file(self):
        """
        Clears current data table and prompts the user to select a new file.
        """
        # Clean up the table and select a new file.
        file_path = self.open_file_dialog()
        if file_path and file_path != self.last_file_path:
            self.data_table.clear()
            self.load_data(file_path)

    def preprocessing_button(self):
        """
        Enables or disables the apply button based on the selected
        preprocessing option.
        """
        if self.preprocessing_options.currentIndex() == 0:
            self.apply_button.setEnabled(False)
        else:
            self.apply_button.setEnabled(True)

    def confirm_preprocessing(self):
        """
        Applies the selected pre-processing option and updates the UI.
        """
        # Get the selected pre-processing option from the ComboBox.
        option = self.preprocessing_options.currentText()
        if not option:
            QMessageBox.warning(
                self,
                "Warning",
                "You must select a pre-processing option before confirming."
            )
            return
        try:
            if option == "🗑️ Remove Rows with Missing Values":
                remove_missing_values(self)
            elif option == "📊 Fill with Mean":
                fill_with_mean(self)
            elif option == "📊 Fill with Median":
                fill_with_median(self)
            elif option == "✏️ Fill with a Constant Value":
                fill_with_constant(self)

            self.nan_data = False
            self.next_button.setEnabled(True)
            self.nan_solved = True
            self.label.edit_label(
                self.nan_label,
                text="There are no more empty values :)",
                color="green"
            )
            self.layout.edit_separator(self.sep, color="green")
            self.layout.edit_separator(self.separator, color="green")
            self.nan_values.setVisible(False)
            self.nan_layout.removeWidget(self.nan_values)
            self.preprocessing_options.setEnabled(False)
            self.apply_button.setEnabled(False)

            # Redisplay the table after preprocessing.
            self.display_data_in_table(self.df)  # Ensure the table is updated
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                (
                    "An error occurred while applying pre-processing: "
                    f"{str(e)}"
                )
            )

    def show_results(self):
        """
        Display regression results in new window. Notifies success or failure.
        """
        from ui.results_window import ResultWindow
        try:
            self.result_window = ResultWindow(
                self.df, self.input_columns, self.output_column
            )
            QMessageBox.information(
                self,
                "Success",
                "The regression model has been created successfully."
            )
            self.result_window.show()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An error occurred while creating the model: {str(e)}"
            )

    def delete_welcome(self):
        """
        Hides the welcome window and displays the next step.
        """
        self.welcome_window.setVisible(False)
        self.layout.layout_visibility(True, True, self.steps_layout)
        self.layout_separator.setVisible(True)
        self.drive_through()

    def next(self):
        """
        Moves to the next step in the workflow based on the current state.
        """
        if self.move < 3:
            if self.empty_values:
                self.move += 1
            else:
                self.move += 2
            self.drive_through()

    def back(self):
        """
        Moves back to the previous step based on the current state.
        """
        if self.move > 1:
            if self.empty_values:
                self.move -= 1
            else:
                self.move -= 2
            self.drive_through()

    def drive_through(self):
        """
        Manages the navigation through the steps based on the current state.
        """
        self.layout.layout_visibility(True, False, self.main_layout)
        self.layout.layout_visibility(True, True, self.NBlayout)

        if self.move == 1:
            self.steps_guide()
            self.layout.layout_visibility(True, True, self.first_step_layout)
            self.return_button.setEnabled(False)
            if self.data_table is None:
                self.back_button.setVisible(False)
                self.next_button.setEnabled(False)
            else:
                self.load_button.setVisible(False)
                self.next_button.setEnabled(True)

        elif self.move == 2:
            self.steps_guide()
            self.layout.layout_visibility(True, True, self.nan_layout)
            self.table_view.setVisible(True)
            self.return_button.setEnabled(True)

            # Ensure the load button remains hidden.
            self.back_button.setVisible(False)
            self.file_label.setVisible(False)
            if not self.nan_solved:
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)

        elif self.move == 3:  # Step 3: Create model
            self.steps_guide()
            self.layout.layout_visibility(True, True, self.regresion_layout)
            self.next_button.setEnabled(False)
            self.return_button.setEnabled(True)

    def steps_guide(self):
        """
        Guide the user through the steps based on the current state.
        """
        text1 = "1. Load dataset or Load model"
        text2 = "2. Delete empty values"
        text3 = "3. Create linear regression model"

        if self.move == 1:
            self.label.edit_label(
                self.first_step,
                text=text1,
                background_color="lightgreen",
                bold=True,
                padding="5px"
            )
            self.label.edit_label(self.second_step, text="")
            self.label.edit_label(self.third_step, text="")

        elif self.move == 2:
            if self.nan_data:
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)
            self.label.edit_label(
                self.second_step,
                text=text2,
                background_color="lightgreen",
                bold=True,
                padding="5px",
            )
            self.label.edit_label(self.first_step, text1)
            self.label.edit_label(self.third_step, text="")

        else:
            if self.empty_values:
                self.label.edit_label(
                    self.third_step,
                    text=text3,
                    background_color="lightgreen",
                    bold=True,
                    padding="5px"
                )
                self.label.edit_label(self.second_step, text2)
            else:
                self.label.edit_label(
                    self.third_step,
                    text="2. Create linear regression model",
                    background_color="lightgreen",
                    bold=True,
                    padding="5px"
                )
                self.second_step.setVisible(False)
            self.label.edit_label(self.first_step, text1)