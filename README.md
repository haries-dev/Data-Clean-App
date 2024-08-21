# Data Cleaner Application

## Overview
The Data Cleaner Application is a Python-based tool for loading, cleaning, splitting, and saving CSV files. Built with `tkinter` for the GUI and `pandas` for data manipulation, this tool provides an intuitive interface for managing large datasets. It offers both automatic and manual cleaning options, along with additional features like data splitting and find-and-replace functionality.

## Features
- **Load CSV**: Easily load CSV files for data processing.
- **Automatic Cleaning**: Perform automatic data cleaning operations such as removing duplicates, trimming whitespace, removing symbols, and filling missing values.
- **Manual Cleaning**: Manually specify characters to remove from the dataset.
- **Split Data**: Split the dataset based on numeric ranges.
- **Find and Replace**: Find specific text and replace it within the dataset.
- **Save CSV**: Save the cleaned and processed data to a new CSV file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/data-cleaner-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd data-cleaner-app
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   **Dependencies:**
   - `tkinter`
   - `pandas`
   - `pandastable`

4. Run the application:
   ```bash
   python main.py
   ```

## Usage

1. **Loading a CSV File**:
   - Click on "Load CSV" and select the CSV file you want to work with.

2. **Automatic Cleaning**:
   - Click on "Automatic Clean" to open the configuration window.
   - Select the cleaning options you want to apply (e.g., Remove Duplicates, Trim Whitespace).
   - Click "Apply" to clean the data automatically.

3. **Manual Cleaning**:
   - Click on "Manual Clean" to open the manual configuration window.
   - Enter characters you want to remove and choose whether to clean the entire dataset.
   - Click "Apply" to clean the data manually.

4. **Splitting Data**:
   - Click on "Split Data" to open the split configuration window.
   - Enter the range for splitting the data.
   - The data will be split into multiple CSV files based on the specified range.

5. **Find and Replace**:
   - Click on "Find and Replace" to open the find and replace window.
   - Enter the text to find and the text to replace it with.
   - Click "Apply" to replace the text in the dataset.

6. **Saving the CSV File**:
   - Click on "Save CSV" to save the cleaned and processed data to a new CSV file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

- **Haries Palaniappan**

Feel free to open an issue if you find any bugs or want to request a feature!
