# RegressionMaker

## Introduction

This ReadMe document is a user guide for our newly released software, **The RegressionMaker**. It is an application for dataset analysis, preprocessing, and regression modeling. You can download the application from our GitHub repository. The file weighs around 28KB and is compatible with Windows, macOS, and Linux operating systems.

**‘RegressionMaker’** has been developed as part of the **COIL Project**, a collaborative effort between **Seneca Polytechnic** (Toronto, Canada) and **Universidad da Coruña** (A Coruña, Spain).

---

## Overview

RegressionMaker is a Python-based GUI application, an intuitive tool designed to simplify the regression modeling process for users ranging from novice analysts to seasoned data scientists. By offering an easy-to-use interface, RegressionMaker boosts productivity by reducing the complexity of preprocessing datasets and building regression models. This guide will help you get started with RegressionMaker and make the most of its functionalities.

![Welcome Screen](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/Imagen1.png)

---

## Features

RegressionMaker provides a range of functionalities to simplify the regression modeling process. These features are designed to make the tool accessible to users of all experience levels:

| **Feature**               | **Description**                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| Dataset Import            | Supports CSV, Excel, and SQLite files for seamless data integration.          |
| Missing Value Detection   | Identifies missing values in datasets and displays a summary of affected columns. |
| Preprocessing Options     | Provides options to drop rows, and fill missing values with mean, median, or a constant value. |
| Regression Type Selection | Allows users to choose between simple regression (one input, one output) and multiple regression. |
| Feature & Target Selection | Enables intuitive selection of input features and output target columns.       |
| Model Building            | Automatically generates regression models with performance metrics like R² and Mean Squared Error. |

---

## Getting Started

To begin using RegressionMaker, ensure your system meets the requirements and is properly configured.

### System Requirements

| **Component**       | **Requirements**                                           |
|---------------------|-----------------------------------------------------------|
| Operating System    | Windows 10 or later, macOS 10.15 or later, or Linux 2.2    |
| Python Version      | 3.x or later                                               |
| Hard Disk Space     | At least 50MB is needed                                    |
| Graphics            | Not required                                              |
| Processor           | Intel i5 or higher                                        |

### Dependencies

- **PyQt5** for building the graphical user interface.
- **Pandas** for data manipulation.
- **Scikit-learn** for regression modeling.
- **Matplotlib** for data visualization.
- **Joblib** for saving the regression model.

**Note:** All these functionalities can be downloaded and installed using Visual Studio Code. The installation instructions are available in the GitHub documentation on the repository.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AntonioDevesaSoengas/COIL-10.git
   ```
2. **Navigate to the project directory:**
   ```bash
   cd COIL-10
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the application:**
   ```bash
   python main.py
   ```

---

## Navigating the Interface

Before using the application, it is important to familiarize yourself with the interface elements and their functions (see Table 3). Each section of the interface is designed to guide users through the workflow of dataset preprocessing and regression modeling.

### Understanding the Interface

![How to load datasets and saved models](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/LoadDatasets2.png)

![Choosing another file](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/ChoosingAnother3.png)

![Preprocessing NaN values options](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/Preproccesing4.png)

| **Icon** | **Button**                     | **Function**                                                                 |
|----------|--------------------------------|-----------------------------------------------------------------------------|
| 1        | Load Dataset                  | For uploading your dataset. Supported formats include CSV, Excel, and SQLite. |
| 2        | Load Model                    | Allows uploading a previously saved regression model. Supported formats include joblib files. |
| 3        | Choose Another File           | Allows users to select a different file after the initial dataset upload.  |
| 4        | Options for preprocessing NaN Values | Provides options to drop rows, and fill missing values with mean, median, or a constant value. |
| 5        | Simple Regression and Multiple Regression | Buttons to choose the type of regression: Simple or Multiple.         |
| 6        | Features                      | A list to select independent variables for the regression.                  |
| 7        | Target                        | A list to select the dependent variable for the regression.                 |
| 8        | Confirm Selection             | A button to finalize your requirements and target selection.               |

![Regression user interface](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/RegressionUserInterface5.png)

---

## Creating a Linear Regression Model

This section guides you through loading datasets, handling missing values, selecting regression options, and generating graphical output.

### Steps to Generate the Linear Regression Model

1. **Load Dataset:**
   - Click the "Load Dataset" button to import your dataset.
   - Supported file types include:
     - CSV files
     - Excel files
     - SQLite databases

   **Important:** If you want to load a saved model from your computer, select "Load Model." If you need to upload a different dataset, click the "Choose Another File" button.

2. **Identify Missing Values:**
   - Click "Next" to identify missing values in your dataset.
   - Columns with missing values and their counts will be displayed in red text.

   ![Missing value detection message](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/MissingValuesDetected6.png)

3. **Preprocess NaN Values:**
   - Use the dropdown menu labeled "Options for preprocessing NaN values" to choose one of the following options:

     | **Option**                 | **Function**                                               |
     |---------------------------|-----------------------------------------------------------|
     | Remove rows with NaN values | Removes rows with missing values in your dataset.         |
     | Fill with Median          | Fills missing values with the median of the column.        |
     | Fill with Mean            | Fills missing values with the mean of the column.          |
     | Fill with constant value  | Prompts you to input a constant value to fill the missing cells. |

   - Click "Apply Preprocessing" to confirm the selected action.

   ![Applying preprocessing button](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/ApplyingPreprocessing7.png)

4. **Choose Regression Type:**
   - Click "Next" and select either:
     - Simple Regression: For a single feature and target.
     - Multiple Regression: For multiple features and a target.

   **Note:** The type of regression determines the input format for features and targets.

5. **Select Features and Target:**
   - Choose your input variables from the "Input Column (Features)."
   - Use the "Output Column (Target)" to choose the output variable.

   **Important:** Ensure you understand that "Features" correspond to the independent variables and "Target" is the dependent variable in the model.

6. **Create the Regression Model:**
   - Click "Create Regression Model."
   - A success message will inform you that the regression model is ready.

   ![Creating the regression model](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/CreatingModel8.png)

---

## Viewing the Results Page

After successfully generating a regression model, users are navigated to the Results Page, which includes a range of components:

![Regression result window](https://github.com/AntonioDevesaSoengas/COIL-10/blob/main/images/ResultWindow9.png)

| **Icon** | **Panel**               | **Function**                                                                 |
|----------|-------------------------|-----------------------------------------------------------------------------|
| 1        | Description Box         | Allows users to document observations, notes, or analyses specific to the generated regression model. |
| 2        | Regression Graph        | Graphical regression model prediction built based on the user selection.   |
| 3        | Model Formula and Metrics | Displays the regression equation created by the model.                     |
| 4        | Prediction Box          | Users can test the model by entering numeric values to receive predicted results. |
| 5        | Save Model Button       | Allows users to save the generated regression model for future use.         |

---

## About the Documentation

RegressionMaker's documentation is regularly updated to reflect the latest changes and enhancements to the application. After each update, the revised documentation will be uploaded to the GitHub repository. Users are encouraged to always refer to the repository for the most current version of this guide.

---

## Contributing

We welcome contributions from developers and users to enhance the features and functionality of RegressionMaker. Please follow these steps:

1. Fork the repository.
2. Create a branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Make your changes and commit them with clear messages:
   ```bash
   git commit -m "feat: Add new feature"
   ```
4. Push the branch to your fork:
   ```bash
   git push origin feature-name
   ```
5. Open a Pull Request.

---

## Contributors

- **Antonio Devesa Soengas** - Scrum Master, Development Lead
- **Iván Docampo** - Documentation, Feature Development
- **Alejandro Nogueiras** - GUI Enhancements, Regression Model Creation
- **Miguel Baños** - Preprocessing, Testing
- **Iván Rodríguez** - Error Management, Persistence Implementation
- **Harshit Kohli** - Documentation and Technical Writing

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Additional Support and Inquiries

If you have suggestions for improving this guide or need information not addressed in the documentation, please get in touch with the technical writer at **hkohli5@myseneca.ca**.

---

## Conclusion

RegressionMaker simplifies the process of creating regression models with its user-friendly interface and robust preprocessing tools. By following this guide, you’ll be able to harness its features effectively and make data-driven decisions with ease. For further assistance, refer to the GitHub repository.
