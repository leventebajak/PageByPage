# PageByPage

This repository contains a set of Python scripts for processing documents page by page.
You can easily install the required dependencies and start processing by running the provided script.

## Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

Download Ollama from https://ollama.com/download and run this command to download the model:

```bash
ollama run llama3.1
```

## Running the Script

To start processing, run the `pagebypage.py` script. The script will ask you for parameters and then begin processing the documents based on your input.

## Scripts Overview

- `pagebypage.py`: Main script to process documents page by page. It will prompt you for the necessary parameters and start processing.
- `processing.py`: Contains functions and logic for processing documents.
- `evaluation.py`: Script to evaluate the faithfulness of the processing results.