# COIL-10

 
Introduction

This ReadMe document is a user guide for our newly released software, The RegressionMaker. It is an application for dataset analysis, preprocessing, and regression modeling. You can download the application from our GitHub repository. The file weighs around 28KB and is compatible with Windows, macOS, and Linux operating systems.
‘RegressionMaker’ has been developed as part of the COIL Project, a collaborative effort between Seneca Polytechnic (Toronto, Canada), and Universidad da Coruña (A Coruña, Spain). 
Overview
RegressionMaker is a Python-based GUI application, an intuitive tool designed to simplify the regression modeling process for users ranging from novice analysts to seasoned data scientists. By offering an easy-to-use interface, RegressionMaker boosts productivity by reducing the complexity of preprocessing datasets and building regression models. This guide will help you get started with RegressionMaker and make the most of its functionalities.
 
Image 1: Welcome Screen
 
Features
RegressionMaker provides a range of functionalities to simplify the regression modeling process. These features are designed to make the tool accessible to users of all experience levels:
Feature	Description
Dataset Import	Supports CSV, Excel, and SQLite files for seamless data integration.
Missing Value Detection	Identifies missing values in datasets and displays a summary of affected columns.
Preprocessing Options	Provides options to drop rows, and fill missing values with mean, median, or a constant value.
Regression Type Selection	Allows users to choose between simple regression (one input, one output) and multiple regression.
Feature & Target Selection	Enables intuitive selection of input features and output target columns.
Model Building	
Automatically generates regression models with performance metrics like R-squared and Mean Squared Error.

User Interface

Interactive GUI built with PyQt5 for a smooth user experience.
Table 1: RegressionMaker features



 
Getting Started
To begin using RegressionMaker, ensure your system meets the requirements and is properly configured.
System Requirements
Before installing RegressionMaker, ensure your system meets the following requirements:
Component	Requirements
Operating System	Windows 10 or later, macOS 10.15 or later, or Linux 2.2

Python Version	3.x or later
Hard Disk Space	At least 50MB is needed
Graphics	Not required
Processor	Intel i5 or higher
Table 2: System Requirements

Remember, there are some dependencies in addition to the requirements shown in Table 2.
Dependencies:
•	PyQt5 to build the graphical user interface
•	Pandas for data manipulation.
•	Scikit-learn for regression modeling.
•	Matplotlib for data visualization
•	Joblib for saving the regression model

Important: All these functionalities can be downloaded and installed using Visual Media Code. 

Note: The installation instructions are available in the GitHub documentation on the repository.




 
Navigating the Interface
Before using the application, it is important to familiarize yourself with the interface elements and their functions (see Table 3). Each section of the interface is designed to guide users through the workflow of dataset preprocessing and regression modeling. 
Understanding the Interface
To get started with RegressionMaker, familiarize yourself with its interface components:
 
Image 2: How to load datasets and saved models
 
Image 3: Choosing another file
 
Image 4: Preprocessing NaN values options
Icon	Button	Function
1
Load Dataset	For uploading your dataset. Supported formats include CSV, Excel, and SQLite.
		2
Load Model	Allows to upload a previously saved regression model Supported formats include joblib files.

3
Choose Another File	Allows users to select a different file after the initial dataset upload.
4
Options for preprocessing NaN Values	Provides options to drop rows, and fill missing values with mean, median, or a constant value.
5
Simple Regression and Multiple Regression	Buttons to choose the type of regression either Simple or Multiple regression.
6
Features	
A list to select independent variables for the regression.

7
Target	A list to select the dependent variable for the regression.
8
Confirm Selection	A button to finalize your requirements and target selection.

Table 3: RegressionMaker button functionality 
 
Image 5: Regression user interface
 
Creating Linear Regression Model
This section guides you through loading datasets, handling missing values, selecting regression options, and generating graphical output.
To generate the linear regression model
1.	Click Load Dataset button to import your dataset. 
A window pops up if the loaded dataset has missing values.

Important: Supported file types include:
o	CSV files
o	Excel files
o	SQLite databases

Note: Select Load Model If you want to load a saved model from your computer.
Note: In case you need to upload a different dataset, click the Choose Another File button. 
2.	Click the Next button to identify missing values in your dataset.
A red color text will display the columns with missing values and their counts. (see image 6)
 
Image 6: Missing value detection message

Option	Function
Remove rows with NaN values	Removes rows with missing values in your dataset.
Fill with Median	Fills missing values with the mean of the column.
Fill with Mean	Fills missing values with the median of the column.

Fill with constant value	Prompts you to input a constant value to fill the missing cells.

3.	Use the dropdown menu labeled Options for preprocessing NaN values to choose one of the following options:









	Table 4: Preprocessing NaN values options
4.	Click Apply Preprocessing to confirm the selected action. (see image 7)
Success message confirms that preprocessing has been applied, displaying the changes in the dataset.

 
Image 7: Applying preprocessing button
5.	Click Next to choose your regression type (see image 7)
Select either:
•	Simple Regression: For a single feature and target.
•	Multiple Regression: For multiple features and a target.

Note: The type of regression determines the input format for features and a target.

6.	Choose your input variables from the Input Column (Features). (see image 5).

7.	Use the Output Column (Target) to choose the output variable. (see image 5).
Important: Ensure you understand that 'Features' corresponds to the independent variables and 'Target' is the dependent variable in the model.







8.	Click Confirm Selection after making your choices.
A message popups showing and confirming your selections.

9.	Click Create Regression Model (see image 8)
A success message popup informing that the regression model is ready.
Note: The application will build a regression model result in a separate window.
 
Image  8: Creating the regression model
 
Viewing the Results Page
After successfully generating a regression model, users are navigated to the Results Page (see image 9), which includes a range of components (see Table 5)
Note: The result window opens in a separate window.
 
Image 9: Regression result window
Icon	Panel	Function
1
Description Box	Allows users to document observations, notes, or analyses specific to the generated regression model.
2
Regression Graph	Graphical regression model prediction built based on the user selection.
3
Model Formula and Metrics	Displays the regression equation created by the model.
4
Prediction Box	User can test the model by entering numeric values to receive predicted results. The Prediction button executes this operation, displaying results.
5
Save Model Button	Allows user to save the generated regression model for future use. 
Note: Saved models can be reloaded for additional predictions or analysis.
Table 5:  Result page interface
About the Documentation 
RegressionMaker's documentation is regularly updated to reflect the latest changes and enhancements to the application. After each update, the revised documentation will be uploaded to the GitHub repository. Users are encouraged to always refer to the repository for the most current version of this guide.
Additional Support and Inquiries
If you have suggestions for improving this guide or need information not addressed in the documentation, please get in touch with the technical writer at hkohli5@myseneca.ca 
Conclusion
RegressionMaker simplifies the process of creating regression models with its user-friendly interface and robust preprocessing tools. By following this guide, you’ll be able to harness its features effectively and make data-driven decisions with ease. For further assistance, refer to the GitHub repository.

