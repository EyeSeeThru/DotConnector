# DotConnector

DotConnector is a Flask web application that allows users to analyze the potential connections between two items using a language model API. The application prompts a Language Model (LLM) to generate insights based on user input.

## Features

- Configure LLM API (base URL and model).
- Input two items to analyze their connections.
- Display results from the LLM in a structured format.

## Requirements

- Python >= 3.10
- Flask
- Requests
- Python-dotenv for environment variable management

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/EyeSeeThru/DotConnector.git
   cd DotConnector
   ```

2. Install dependencies using Poetry:
```
poetry install
```

3. Create/edit the .env file in the root directory to add your LLM API key:
4. 
```
LLM_API_KEY=your_api_key_here
```

## Usage
1. Run the Flask application:
```
python main.py
```

The application will be accessible at: http://0.0.0.0:80.

2. Open your browser and navigate to the application.

3. Fill out the LLM configuration form with your Base URL and Model name.

4. Input two items in the provided fields and click "Find Connections".

5. View the analysis results below the input fields.


## License

This project is licensed under the MIT License

## Acknowledgments

- Flask - A lightweight WSGI web application framework.
- Requests - Simple HTTP library for Python.
