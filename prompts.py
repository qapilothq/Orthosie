suggestion_prompt = """
            You are an expert in software testing and behavior-driven development (BDD). Based on the provided base64-encoded image of the application's UI, generate clear, concise, and comprehensive BDD test cases in Gherkin syntax.

            **Key considerations:**

            **Image Analysis:**
            Analyze the provided base64-encoded image to identify visible UI elements such as input fields, buttons, dropdowns, and labels.
            Generate test cases specifically for the elements present in the image and avoid assumptions about elements that are not visible.
            
            **Scenario Coverage:**
            Cover positive and negative scenarios.
            Include edge cases and boundary conditions.
            Consider error handling, system notifications, and redirections.
            Address navigation flows based on user actions.
           
            **Input Fields Handling:**
            If the screen contains input fields (e.g., mobile number, email, date), generate test cases using field-specific valid and invalid values.
            Provide example values in the Examples section of the test case to ensure thorough validation.

            **Expected output:**
            Generate test cases focused on the provided elements without generic placeholders.
            Ensure user flows and validations match the given UI design.
            Readily executable in a BDD framework like Cucumber or Behave.

            Give the final output in the JSON format as follows:
            **"type"** should be either `"scenarioOutline"` for parameterized tests or `"scenario"` for single-flow cases.
            **"scenario"** should represent the title of the scenario.
            ```json
                {
                "feature": "[Feature Name]",
                "scenarios": [
                    {
                    "type": "scenarioOutline",
                    "scenario": "[Scenario Title]",
                    "steps": [
                        "Given [Condition]",
                        "When [User Action]",
                        "And [Additional Action]",
                        "Then [Expected Outcome]"
                    ],
                    "examples": {
                        "[Field Name]": [
                        "[Valid Example 1]",
                        "[Valid Example 2]"
                        ]
                    }
                    },
                    {
                    "type": "scenario",
                    "scenario": "[Scenario Title]",
                    "steps": [
                        "Given [Condition]",
                        "When [User Action]",
                        "Then [Expected Outcome]"
                    ]
                    }
                ]
                }
        """
suggestionWithText_prompt = """
            You are an expert in software testing and behavior-driven development (BDD). Based on the provided base64-encoded image of the application's UI and the user-inputted natural language scenario, generate clear, concise, and comprehensive BDD test cases in Gherkin syntax.
           
             **Key considerations:**

            **Image Analysis:**
            Analyze the provided base64-encoded image to identify visible UI elements such as input fields, buttons, dropdowns, and labels.
            Generate test cases specifically for the elements present in the image and avoid assumptions about elements that are not visible.
            
            **User-Inputted Scenario Focus:**
            If the user provides a specific natural language scenario (e.g., "login scenario"), focus only on generating test cases relevant to the user-inputted context.
            Ensure that test cases align with the user-specified scenario while considering elements present in the image.
            
            **Scenario Coverage:**
            Cover positive and negative scenarios.
            Include edge cases and boundary conditions.
            Consider error handling, system notifications, and redirections.
            Address navigation flows based on user actions.
           
            **Input Fields Handling:**
            If the screen contains input fields (e.g., mobile number, email, date), generate test cases using field-specific valid and invalid values.
            Provide example values in the Examples section of the test case to ensure thorough validation.

            **Expected output:**
            If a natural language input is provided (e.g., "login scenario"), filter the identified UI elements from the image to match the user-specified scenario.
            Generate test cases specific to this scenario and ignore other UI elements unrelated to the context.
            Ensure scenarios and steps are readily executable in a BDD framework like Cucumber or Behave.

            Give the final output in the JSON format as follows:
            **"type"** should be either `"scenarioOutline"` for parameterized tests or `"scenario"` for single-flow cases.
            **"scenario"** should represent the title of the scenario.
            ```json
                {
                "feature": "[Feature Name]",
                "scenarios": [
                    {
                    "type": "scenarioOutline",
                    "scenario": "[Scenario Title]",
                    "steps": [
                        "Given [Condition]",
                        "When [User Action]",
                        "And [Additional Action]",
                        "Then [Expected Outcome]"
                    ],
                    "examples": {
                        "[Field Name]": [
                        "[Valid Example 1]",
                        "[Valid Example 2]"
                        ]
                    }
                    },
                    {
                    "type": "scenario",
                    "scenario": "[Scenario Title]",
                    "steps": [
                        "Given [Condition]",
                        "When [User Action]",
                        "Then [Expected Outcome]"
                    ]
                    }
                ]
                }
        """
tetscase_prompt = """
    You are an expert in automation QA analysis. Analyze the provided Android page source XML and BDD test scenario JSON to generate sequential test steps based on the steps parameter only.

    **Instructions:**

        1. Consider only the actions listed under the When and And clauses in the scenario JSON.
        2. Identify relevant UI elements that support these actions from the Android page source XML.
        3. Ignore duplicate or similar elements based on resource-id and bounds.
        4. Generate test step details in the following JSON format:
            ```json
            [
                {
                    "pageelementid": "<resource-id>",
                    "bounds": "<bounds>",
                    "class": "<class>",
                    "actionperformed": "<user action based on scenario>",
                    "input_text": "<if applicable, the value to input>",
                    "xml_statement": "<corresponding XML element>"
                }
            ]
        5. Ensure that the final output contains only the specific actions described in the When and And clauses, maintaining the correct sequence of execution.

"""