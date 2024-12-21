# RegressionMaker

## Introduction

**RegressionMaker** is a Python-based application designed to facilitate the creation and visualization of linear regression models (both simple and multiple). This user-friendly software supports datasets in CSV, Excel, and SQLite formats and provides a range of tools for data preprocessing and regression analysis. The project, developed collaboratively by **Seneca Polytechnic** (Toronto, Canada) and **Universidad da Coruña** (A Coruña, Spain), is a product of the **COIL Project**.

---

## Overview

RegressionMaker streamlines the regression modeling workflow, making it accessible to users from diverse technical backgrounds. With an intuitive graphical interface, the application simplifies tasks such as data preprocessing, regression modeling, and model evaluation.

![Welcome Screen](https://github.com/AntonioDevesaSoengas/COIL-10/blob/d5b0044a5ecd8bc2c0a7fb25b4e28399ba5d2bfc/docs/images/Imagen1.png)

---

## Features

| **Feature**               | **Description**                                                                 |
|---------------------------|-------------------------------------------------------------------------------|
| Dataset Import            | Supports CSV, Excel, and SQLite files for seamless data integration.          |
| Missing Value Detection   | Identifies missing values in datasets and displays a summary of affected columns. |
| Preprocessing Options     | Options to drop rows, fill missing values with mean, median, or a constant value. |
| Regression Type Selection | Allows users to choose between simple regression and multiple regression.      |
| Feature & Target Selection| Intuitive selection of input features and output target columns.               |
| Model Building            | Automatically generates regression models with performance metrics like R² and Mean Squared Error. |

---

## Getting Started

To begin using RegressionMaker, ensure your system meets the requirements and follow the installation steps below.

### System Requirements

| **Component**       | **Requirements**                                           |
|---------------------|-----------------------------------------------------------|
| Operating System    | Windows 10 or later, macOS 10.15 or later, or Linux 2.2    |
| Python Version      | 3.x or later                                               |
| Hard Disk Space     | At least 50MB                                              |
| Processor           | Intel i5 or higher                                         |

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

RegressionMaker’s interface guides users step-by-step through the workflow of dataset preprocessing and regression modeling.

### Interface Overview

![Load Dataset](https://github.com/AntonioDevesaSoengas/COIL-10/blob/d5b0044a5ecd8bc2c0a7fb25b4e28399ba5d2bfc/docs/images/LoadDatasets2.png)

![Choosing Another File](https://github.com/AntonioDevesaSoengas/COIL-10/blob/d5b0044a5ecd8bc2c0a7fb25b4e28399ba5d2bfc/docs/images/ChoosingAnother3.png)

| **Icon** | **Button**                     | **Function**                                                                 |
|----------|--------------------------------|-----------------------------------------------------------------------------|
| 1        | Load Dataset                  | Upload datasets in CSV, Excel, or SQLite formats.                          |
| 2        | Load Model                    | Upload previously saved regression models.                                 |
| 3        | Choose Another File           | Select a different dataset after initial upload.                          |
| 4        | Preprocess NaN Values         | Options to drop rows or fill missing values.                              |
| 5        | Simple/Multiple Regression    | Buttons to select regression type.                                        |
| 6        | Features                      | Select independent variables.                                             |
| 7        | Target                        | Select dependent variable.                                                |
| 8        | Confirm Selection             | Finalize feature and target selection.                                    |

---

## Workflow

### Steps to Build a Regression Model

1. **Load Dataset:**
   - Click the "Load Dataset" button to upload your dataset.
   - Supported formats: CSV, Excel, SQLite.

2. **Handle Missing Values:**
   - Click "Next" to identify missing values.
   - Select an option from the dropdown menu to address missing data.

![Preprocessing NaN Values](https://github.com/AntonioDevesaSoengas/COIL-10/blob/d5b0044a5ecd8bc2c0a7fb25b4e28399ba5d2bfc/docs/images/Preproccesing4.png)

3. **Choose Regression Type:**
   - Simple Regression for one input and one output.
   - Multiple Regression for multiple inputs and one output.

4. **Select Features and Target:**
   - Choose features and target columns.

5. **Create Model:**
   - Click "Create Regression Model" to generate the model and view metrics.

![Regression Interface](https://github.com/AntonioDevesaSoengas/COIL-10/blob/d5b0044a5ecd8bc2c0a7fb25b4e28399ba5d2bfc/docs/images/RegressionUserInterface5.png)

---

## Results and Predictions

After creating a regression model, users can:

- View the regression graph.
- Test the model by inputting values for predictions.
- Save the model for future use.

![Results Window](https://github.com/AntonioDevesaSoengas/COIL-10/blob/d5b0044a5ecd8bc2c0a7fb25b4e28399ba5d2bfc/docs/images/ResultWindow9.png)

---

## Contributing

We welcome contributions! Please refer to the [Contributing Guidelines](CONTRIBUTING.md) for details on how to get involved.

---

## Contributors

- **Antonio Devesa Soengas**
- **Iván Docampo**
- **Alejandro Nogueiras**
- **Miguel Baños**
- **Iván Rodríguez**
- **Harshit Kohli**

---

## Support

For assistance or feedback, please reach out via the GitHub repository.
