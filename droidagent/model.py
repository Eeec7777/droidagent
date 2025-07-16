from google import genai
from google.genai import types
import time
import os
import json
import warnings
from dotenv import load_dotenv 

from .config import agent_config
from .utils.logger import Logger

load_dotenv()

logger = Logger(__name__)

# Disable telemetry to avoid capture() errors
os.environ['GOOGLE_GENAI_DISABLE_TELEMETRY'] = '1'
os.environ['GOOGLE_ANALYTICS_DISABLED'] = '1'
os.environ['GOOGLE_CLOUD_DISABLE_TELEMETRY'] = '1'

# Suppress telemetry warnings
warnings.filterwarnings('ignore', message='.*telemetry.*')

# Configure Gemini API with error handling
try:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    logger.info("Gemini client initialized successfully")
except Exception as e:
    # If there's an error during client initialization, try without telemetry
    logger.warning(f"Error initializing Gemini client: {e}")
    logger.info("Attempting to initialize without telemetry...")
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

TIMEOUT = 60
MAX_TOKENS = 8000
MAX_RETRY = 1000
TEMPERATURE = 0.6

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
    
    # Handle function calls
    if functions and function_call_option != "none":
        # If functions are provided, add function call instructions
        function_descriptions = []
        for func in functions:
            func_info = func.get('function', {})
            name = func_info.get('name', '')
            description = func_info.get('description', '')
            parameters = func_info.get('parameters', {})
            
            function_descriptions.append(f"Function: {name}")
            function_descriptions.append(f"Description: {description}")
            if parameters.get('properties'):
                function_descriptions.append(f"Parameters: {parameters}")
        
        function_prompt = "\n\nAvailable functions:\n" + "\n".join(function_descriptions)
        function_prompt += "\n\nTo call a function, respond with JSON format: {\"function\": {\"name\": \"function_name\", \"arguments\": {\"param1\": \"value1\", \"param2\": \"value2\"}}}"
        
        full_prompt += function_prompt
    
    response = None
    for retry_count in range(MAX_RETRY):
        try:
            logger.info(f'Sending request to Gemini API (attempt {retry_count + 1}/{MAX_RETRY})')
            
            # Configure generation settings
            config_params = {
                'temperature': TEMPERATURE,
                'max_output_tokens': max_tokens,
            }
            
            # Only add thinking_config for newer models that support it
            # Currently only Gemini 2.5 Flash and newer versions support thinking_config
            thinking_supported_models = ["gemini-2.5-flash", "gemini-2.0-flash-exp"]
            if model in thinking_supported_models:
                config_params['thinking_config'] = types.ThinkingConfig(thinking_budget=0)  # Disable thinking for faster response
            
            config = types.GenerateContentConfig(**config_params)
            
            # Add 1 second delay before API request
            time.sleep(1)
            
            # Generate content using the new API
            response = client.models.generate_content(
                model=model,
                contents=full_prompt,
                config=config
            )
            
            logger.info(f'Received response from Gemini API successfully')
            break
            
        except Exception as e:
            logger.warning(f'Google GenAI API request errored (attempt {retry_count + 1}/{MAX_RETRY}): {str(e)}')
            if retry_count < MAX_RETRY - 1:
                logger.info('Retrying in 3 seconds...')
                time.sleep(3)
            continue
        except KeyboardInterrupt as e:
            raise e

    if response is None:
        logger.error('Google GenAI API request failed after all retries')
        raise TimeoutError('Google GenAI API request errored multiple times')

    # Record usage and response time
    if hasattr(response, 'usage_metadata'):
        usage = response.usage_metadata
        
        # Extract token counts using the correct attribute names
        input_tokens = getattr(usage, 'prompt_token_count', 0)
        output_tokens = getattr(usage, 'candidates_token_count', 0)
        total_tokens = getattr(usage, 'total_token_count', input_tokens + output_tokens)
        
        print(f"\n📊 Token Usage - Model: {model}")
        print(f"   Input tokens: {input_tokens:,}")
        print(f"   Output tokens: {output_tokens:,}")
        print(f"   Total tokens: {total_tokens:,}")
        print(f"   Response time: {time.time() - start_time:.2f}s")
        print()
        
        APIUsageManager.record_usage(model, response.usage_metadata)
    APIUsageManager.record_response_time(model, time.time() - start_time)

    # Extract response text
    response_text = ""
    if hasattr(response, 'text'):
        response_text = response.text.strip()
    elif hasattr(response, 'candidates') and len(response.candidates) > 0:
        candidate = response.candidates[0]
        if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
            response_text = candidate.content.parts[0].text.strip()
    
    if not response_text:
        return "No response generated"
    
    # Check if response is a function call
    if functions and function_call_option != "none":
        # Try to parse JSON function call
        try:
            import json
            # Look for JSON in the response
            if response_text.startswith('{') and response_text.endswith('}'):
                parsed_response = json.loads(response_text)
                if 'function' in parsed_response:
                    # Return function call format expected by the code
                    return {
                        'id': f'call_{int(time.time() * 1000)}',
                        'function': parsed_response['function']
                    }
        except (json.JSONDecodeError, KeyError):
            # If JSON parsing fails, check for function call in text
            if "function" in response_text.lower() and "{" in response_text:
                # Try to extract JSON from the response
                import re
                json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
                if json_match:
                    try:
                        parsed_response = json.loads(json_match.group())
                        if 'function' in parsed_response:
                            return {
                                'id': f'call_{int(time.time() * 1000)}',
                                'function': parsed_response['function']
                            }
                    except json.JSONDecodeError:
                        pass
    
    return response_text

    