# Migration from OpenAI to Gemini 2.5 Flash

This document outlines the changes made to migrate DroidAgent from OpenAI to Google's Gemini 2.5 Flash API.

## Overview of Changes

### 1. Dependencies Updated
- **Removed**: `openai` package
- **Added**: `google-genai==1.25.0` (latest version)
- **Added**: `python-dotenv>=0.19.0` for environment variable management
- **Added**: `requests>=2.25.0` for HTTP requests

### 2. API Client Changes
- **Before**: `openai.OpenAI(api_key=...)`
- **After**: `genai.Client(api_key=...)`

### 3. Model Configuration
All models now use Gemini 2.5 Flash:
- `actor_model`: `gemini-2.5-flash`
- `observer_model`: `gemini-2.5-flash`
- `planner_model`: `gemini-2.5-flash`
- `reflector_model`: `gemini-2.5-flash`

### 4. API Call Changes
- **Before**: `client.chat.completions.create(...)`
- **After**: `client.models.generate_content(...)`

### 5. Response Handling
- **Before**: `response.choices[0].message.content`
- **After**: `response.text` or `response.candidates[0].content.parts[0].text`

### 6. Error Handling
- **Before**: `openai.APITimeoutError`, `openai.APIConnectionError`, etc.
- **After**: Generic `Exception` handling with specific error logging

## Configuration

### Environment Variables
Update your `.env` file:
```bash
# Old
OPENAI_API_KEY=sk-...

# New
GEMINI_API_KEY=AIzaSy...
```

### API Key Setup
1. Go to [Google AI Studio](https://ai.google.dev/gemini-api/docs/quickstart?hl=zh-tw)
2. Create a new API key
3. Add it to your `.env` file

## Testing
Run the included test script to verify the migration:
```bash
python test_gemini.py
```

## Benefits of Gemini 2.5 Flash
- **Faster**: Lower latency compared to OpenAI models
- **More efficient**: Better token usage
- **Latest technology**: Access to Google's most recent LLM capabilities
- **Cost-effective**: Competitive pricing structure

## Backwards Compatibility
The migration maintains the same interface, so existing code using `get_next_assistant_message()` continues to work without changes.

## Files Modified
- `droidagent/model.py`: Complete rewrite for Gemini API
- `droidagent/config.py`: Updated model configurations
- `droidagent/_actor_gptdroid.py`: Removed OpenAI dependencies
- `requirements.txt`: Updated dependencies
- `README.md`: Updated documentation
- `.env.example`: Updated example configuration

## Troubleshooting
If you encounter issues:
1. Verify your Gemini API key is valid
2. Check that `google-genai==1.25.0` is installed
3. Run the test script to identify specific problems
4. Check the logs for detailed error messages
