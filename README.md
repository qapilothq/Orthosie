# Orthosie: Smart way to automate the generation of BDD testcase scenarios and teststeps

## Overview

Orthosie is a powerful FastAPI-based application to automate the generataion of BDD testcase scenarios using android app screenshot. It intelligently extracts platform-specific test steps (sequential user actions relevant to the specific scenario) from the Android page source XML. Powered by OpenAI's GPT-4, it provides intelligent recommendations, covering all positive and negitive scenarios.

**Current Status**: Beta version supporting Android XML only. iOS support coming soon.

## Key Features

- Automated BDD testcase scenario generation using screenshot as well as userinput
- Automated teststep generation for the specific test scenario using page source XML
- Intelligent openAI powered recommendations 
- RESTful API for seamless integration
- Detailed element metadata extraction from XML
- Comprehensive API documentation

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- FastAPI
- uvicorn
- langchain(for invoking the LLM)
- requests (for URL handling)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/qapilotio/Orthosie.git
   cd Orthosie
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

## Quick Start

1. Start the server:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. Access the interactive API documentation:
   - OpenAPI UI: `http://localhost:8000/docs`
   - ReDoc UI: `http://localhost:8000/redoc`

## API Reference

There are mainly two APIs, One can provide testcase suggestions in BDD format using image and natural language input and another one can generate the teststeps from the generated BDD formatted scenario and XML.

### POST /invoke/suggestions

Analyzes mobile screen for the smart BDD testcase generation. It also consider userinput if the user spefies the scenario from the entire screen

#### Request Body

```json
{
  "image": "string",  // Mandatory: File path or URL
  "userinput": "string"     // Optional: Natural language input(If user required any specific scenario from the give screen)
}
```

**Note**:  `image` must be provided. When user provides `userinput` it can generate the specific scenarios otherwise it will generate all the possible scenarios.

#### Response Format

```json
{
  "status": "success",
  "agent_response": {
      "feature": "Feature title as string",
      "scenarios": [
          {
              "type": "scenarioOutline", //Specifically for the scenarios having form fields
              "scenario": "Scenario title as string",
              "steps": [
                  "Array of steps in BDD format"
              ],
              "examples": "Json Object of example input values for form fields"
          },
          {
              "type": "scenario", //Generic scenarios in BDD format
              "scenario": "scenario title as string",
              "steps": [
                   "Array of steps in BDD format"
              ]
          },
      ]
  }
}
```

### POST /invoke/teststeps

Analyzes specific scenario JSON in the BDD format as generated from the suggestions API and android app source XML to generate teststeps with the metadata.

#### Request Body

```json
{
  "xml": "string",  // Mandatory: File path or URL
  "scenario": "string"     // Mandatory: JSON of specific scenario in the BDD format as generated in the suggestions api
}
```

**Note**:  `XML` and `scenario` must be provided. So it can analyze the both XML and scenario to generate the teststeps.

#### Response Format

```json
{
  "status": "success",
  "steps": [
    {
        "pageelementid": "String",
        "bounds": "String",
        "class": "String",
        "actionperformed": "String",
        "input_text": "String",
        "xml_statement": "entire element XML in String"
    }
  ]
}
```

### GET /health

Health check endpoint returning application status.

## Project Structure

```
valetudo/
├── main.py          # FastAPI application and endpoints
├── utils.py         # Helper functions and utilities
├── prompts.py       # GPT-4 prompt templates
├── init_llm.py           # OpenAI integration
├── requirements.txt # Project dependencies
└── .env            # Environment variables
```

## Error Handling

The API implements comprehensive error handling for:
- Invalid input formats
- Missing required fields
- Failed API calls
- Image processing errors
- XML parsing failures

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Contact  

For questions or support, please contact **[contactus@qapilot.com](mailto:contactus@qapilot.com)**.  

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
