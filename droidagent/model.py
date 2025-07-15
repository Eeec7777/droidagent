from google import genai
from google.genai import types
import time
import os
import json
from dotenv import load_dotenv 

from .config import agent_config
from .utils.logger import Logger

load_dotenv()

# Configure Gemini API
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TIMEOUT = 60
MAX_TOKENS = 8000
MAX_RETRY = 1000
TEMPERATURE = 0.6

logger = Logger(__name__)

class APIUsageManager:
    usage = {}
    response_time = {}

    @classmethod
    def record_usage(cls, model, usage_metadata):
        if model not in cls.usage:
            cls.usage[model] = {
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0,
            }
        
        # For new Google GenAI API, we need to handle usage metadata differently
        if hasattr(usage_metadata, 'input_tokens'):
            cls.usage[model]['prompt_tokens'] += usage_metadata.input_tokens
        if hasattr(usage_metadata, 'output_tokens'):
            cls.usage[model]['completion_tokens'] += usage_metadata.output_tokens
        if hasattr(usage_metadata, 'total_tokens'):
            cls.usage[model]['total_tokens'] += usage_metadata.total_tokens
        else:
            # Calculate total if not provided
            cls.usage[model]['total_tokens'] = cls.usage[model]['prompt_tokens'] + cls.usage[model]['completion_tokens']

    @classmethod
    def record_response_time(cls, model, response_time):
        if model not in cls.response_time:
            cls.response_time[model] = []
        cls.response_time[model].append(response_time)


def stringify_prompt(prompt):
    prompt_str = ''

    prompt_str += f'\n*** System:\n{prompt["system_message"]}\n'
    
    for user_message, assistant_message in prompt['conversation']:
        prompt_str += f'\n*** User:\n{user_message}\n'
        if assistant_message is not None:
            prompt_str += f'\n*** Assistant:\n{assistant_message}\n'

    return prompt_str

def zip_messages(system_message, user_messages, assistant_messages):
    conversation = list(zip(user_messages, assistant_messages))
    if len(user_messages) == len(assistant_messages) + 1:
        conversation.append((user_messages[-1], None))
    return {
        "system_message": system_message,
        "conversation": conversation
    }

def get_next_assistant_message(system_message, user_messages, assistant_messages=[], functions=[], model="gemini-2.5-flash", max_tokens=MAX_TOKENS, function_call_option=None):
    # Convert model name to the correct format if needed
    if model.startswith("gpt-"):
        model = "gemini-2.5-flash"  # Default fallback to Gemini 2.5 Flash
        logger.info(f'Converting OpenAI model to Gemini model: {model}')
    
    start_time = time.time()

    # Build conversation history
    conversation_parts = []
    
    # Add system message as the first part
    conversation_parts.append(system_message)
    
    # Add conversation history
    if len(user_messages) != len(assistant_messages) + 1:
        with open('errored_prompt.txt', 'w') as f:
            f.write(stringify_prompt(zip_messages(system_message, user_messages, assistant_messages)))
        raise ValueError('Number of user messages should be one more than the number of assistant messages: refer to `errored_prompt.txt`')
    
    for user_message, assistant_message in zip(user_messages[:-1], assistant_messages):
        if isinstance(user_message, str):
            conversation_parts.append(f"User: {user_message}")
        else:
            # Handle tool responses
            conversation_parts.append(f"Tool Response: {user_message.get('return_value', '')}")
        
        if isinstance(assistant_message, str):
            conversation_parts.append(f"Assistant: {assistant_message}")
        else:
            # Handle function calls
            conversation_parts.append(f"Assistant: Function call: {assistant_message}")
    
    # Add the current user message
    current_user_message = user_messages[-1]
    if isinstance(current_user_message, str):
        conversation_parts.append(f"User: {current_user_message}")
    else:
        conversation_parts.append(f"Tool Response: {current_user_message.get('return_value', '')}")
    
    # Combine all parts into a single prompt
    full_prompt = "\n\n".join(conversation_parts)
    
    response = None
    for _ in range(MAX_RETRY):
        try:
            # Configure generation settings
            config = types.GenerateContentConfig(
                temperature=TEMPERATURE,
                max_output_tokens=max_tokens,
                thinking_config=types.ThinkingConfig(thinking_budget=0)  # Disable thinking for faster response
            )
            
            # Generate content using the new API
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=config
            )
            
            break
            
        except Exception as e:
            logger.info(f'Google GenAI API request errored: {str(e)}. Retrying...')
            time.sleep(3)
            continue
        except KeyboardInterrupt as e:
            raise e

    if response is None:
        raise TimeoutError('Google GenAI API request errored multiple times')

    # Record usage and response time
    if hasattr(response, 'usage_metadata'):
        APIUsageManager.record_usage(model, response.usage_metadata)
    APIUsageManager.record_response_time(model, time.time() - start_time)

    # Extract response text
    if hasattr(response, 'text'):
        return response.text.strip()
    elif hasattr(response, 'candidates') and len(response.candidates) > 0:
        candidate = response.candidates[0]
        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
            return candidate.content.parts[0].text.strip()
    
    return "No response generated"

    