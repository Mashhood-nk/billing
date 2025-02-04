# Invoice Generator Flask Application

This is a simple Flask-based web application for generating invoices in PDF format. It allows users to input invoice details such as company information, customer details, items, and tax rates, and then generates an invoice that can be downloaded in PDF format.

## Features
- Create invoices with customizable company and customer details.
- Add multiple items with quantity, rate, and tax information.
- Apply discounts and calculate the grand total.
- Automatically calculate the tax for each item based on the provided tax rate.
- Convert the total amount into words.
- Download the generated invoice as a PDF file.

## Technologies Used
- **Flask**: A lightweight WSGI web application framework for Python.
- **FPDF**: A Python library for creating PDFs.
- **Num2Words**: A library to convert numbers into words (used to convert the total amount into words).
- **HTML**: For the basic web form interface.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/invoice-generator.git
    ```

2. Navigate into the project directory:

    ```bash
    cd invoice-generator
    ```

3. Create and activate a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the necessary dependencies:

    ```bash
    pip install -r requirements.txt
    ```

    **Note**: If `requirements.txt` is not present, install the required libraries manually:

    ```bash
    pip install Flask fpdf num2words
    ```

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Open your browser and go to `http://127.0.0.1:5000/` to access the invoice generator form.

3. Fill out the form with the necessary details:
   - Company name and address
   - Customer name and phone number
   - Invoice number, date, and GSTIN
   - Tax rate and discount (optional)
   - Add item details (name, quantity, rate)

4. After filling the form, submit it to generate the invoice. The PDF will be downloaded automatically.

## Example of Generated Invoice

Here is an example of the generated invoice format:

- Company name and address
- GSTIN and invoice details
- Customer name and contact information
- Itemized list of products or services with quantity, rate, tax, and total for each item
- Grand total, including any discounts
- Amount in words

## Folder Structure

