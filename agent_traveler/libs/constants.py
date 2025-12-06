"""
Defines all the models that will be used in each agent.
"""

from google.adk.models.google_llm import Gemini
from google.genai import types

# Retry configuration
retry_config = types.HttpRetryOptions(
    attempts=10,  # Maximum retry attempts
    exp_base=7,  # Delay multiplier
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
)

DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_MODEL_RETRY = Gemini(model=DEFAULT_MODEL, retry_options=retry_config)

# Agents
ROOT_AGENT_MODEL = DEFAULT_MODEL_RETRY

VALIDATE_INPUT_AGENT_MODEL = DEFAULT_MODEL_RETRY
EXTRACT_DATA_AGENT_MODEL = DEFAULT_MODEL_RETRY
REPORT_AGENT_MODEL = DEFAULT_MODEL_RETRY
OUTPUT_AGENT_MODEL = DEFAULT_MODEL_RETRY

RESEARCH_AGENT_MODEL = DEFAULT_MODEL_RETRY
DESTIONATION_AGENT_MODEL = DEFAULT_MODEL_RETRY
WHAT_TO_PACK_MODEL = DEFAULT_MODEL_RETRY
VERIFY_PROBLEM_AGENT_MODEL = DEFAULT_MODEL_RETRY
POI_MODEL = DEFAULT_MODEL_RETRY
RESEARCH_CITY_MODEL = DEFAULT_MODEL_RETRY


# Tools
SEARCH_TOOL_MODEL = DEFAULT_MODEL_RETRY
