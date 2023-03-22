# Pijama2json

Pijama2json is a Python script that reads data about disciplines offered in computer science course from UFCG (what we call as pijama, it a PDF) and turns it into a JSON format.

## Requirements

To run this script, you need to have Python 3 installed on your system along with the following packages:

- PyPDF2
- json

You can install the packages by running:

```
$ pip install ...
```

## Usage

To use pijama2json, you can run the following command:

```
$ python3 app.py <input_file> <output_file>
```

Where:

```<input_file>``` is the path to the PDF file containing the data.
```<output_file>``` is the path to the JSON file to be created.

The script will extract the relevant data from the PDF file and store it in the specified JSON file.
