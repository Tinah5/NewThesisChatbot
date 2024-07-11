import openai
from langchain.prompts import PromptTemplate

def analyze_ambiguities(requirements_text, api_key):
    openai.api_key = api_key

    # Load your prompt template from file (example using a template file)
    with open('templates/prompt_template.txt', 'r') as file:
        prompt_template_content = file.read()

    # Create a PromptTemplate instance (example, adjust based on your PromptTemplate implementation)
    prompt = PromptTemplate(input_variables=["User_input"], template=prompt_template_content)

    # Fill the prompt template with the requirements text
    prompt_text = prompt.format(User_input=requirements_text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the chat-based model
            messages=[
                {"role": "system", "content": "You are an assistant that detects ambiguities in requirements."},
                {"role": "user", "content": prompt_text}
            ],
            max_tokens=1000  # Adjust as needed
        )

        # Extract the response text
        response_text = response['choices'][0]['message']['content']

        # Example parsing of response (adjust based on your actual response structure)
        ambiguity_detected = "ambiguity" in response_text.lower()
        ambiguity_type = "Semantic Ambiguity" if ambiguity_detected else "None"
        ambiguity_reason = "Multiple interpretations due to unclear scope" if ambiguity_detected else "No ambiguity detected"

        result = {
            "has_ambiguity": ambiguity_detected,
            "ambiguity_type": ambiguity_type,
            "ambiguity_reason": ambiguity_reason,
            "response_text": response_text  # Include the full response text for reference
        }

        return result

    except openai.error.APIError as e:
        if e.code == 429:
            # Handle rate limit reached: implement exponential backoff or retry after a delay
            pass
        else:
            raise e
