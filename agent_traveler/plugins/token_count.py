import logging

from google.adk.plugins import BasePlugin
from google.adk.models.llm_response import LlmResponse
from google.adk.agents.callback_context import CallbackContext
from google.genai.types import GenerateContentResponseUsageMetadata


class TokenCountPlugin(BasePlugin):
    def __init__(self):
        super().__init__(name="count_token")
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0
        self.total_thoughts_token_count = 0
        self.total_tool_use_prompt_token_count = 0
        self.agents = {}

    @staticmethod
    def token_usage(usage: GenerateContentResponseUsageMetadata):
        prompt_tokens = getattr(usage, "prompt_token_count", 0) or 0
        completion_tokens = getattr(usage, "candidates_token_count", 0) or 0
        thoughts_token_count = getattr(usage, "thoughts_token_count", 0) or 0
        tool_use_prompt_token_count = (
            getattr(usage, "tool_use_prompt_token_count", 0) or 0
        )
        total_tokens = getattr(usage, "total_token_count", 0) or 0

        return {
            "prompt": prompt_tokens,
            "completion": completion_tokens,
            "thoughts": thoughts_token_count,
            "tool_use_prompt": tool_use_prompt_token_count,
            "total": total_tokens,
        }

    def total_token_usage(self, usage: GenerateContentResponseUsageMetadata, name: str):
        tokens = TokenCountPlugin.token_usage(usage)

        self.total_prompt_tokens += tokens["prompt"]
        self.total_completion_tokens += tokens["completion"]
        self.total_thoughts_token_count += tokens["thoughts"]
        self.total_tool_use_prompt_token_count += tokens["tool_use_prompt"]
        self.total_tokens += tokens["total"]

        if not self.agents.get(name):
            self.agents[name] = {
                "total_prompt_tokens": 0,
                "total_completion_tokens": 0,
                "total_tokens": 0,
                "total_thoughts_token_count": 0,
                "total_tool_use_prompt_token_count": 0,
            }

        self.agents[name] = {
            "total_prompt_tokens": self.agents[name]["total_prompt_tokens"]
            + tokens["prompt"],
            "total_completion_tokens": self.agents[name]["total_completion_tokens"]
            + tokens["completion"],
            "total_thoughts_token_count": self.agents[name][
                "total_thoughts_token_count"
            ]
            + tokens["thoughts"],
            "total_tool_use_prompt_token_count": self.agents[name][
                "total_tool_use_prompt_token_count"
            ]
            + tokens["tool_use_prompt"],
            "total_tokens": self.agents[name]["total_tokens"] + tokens["total"],
        }

        return tokens

    async def after_model_callback(
        self,
        *,
        callback_context: CallbackContext,
        llm_response: LlmResponse,
    ) -> None:
        name = callback_context.agent_name
        if not (
            hasattr(llm_response, "usage_metadata") and llm_response.usage_metadata
        ):
            logging.debug(f"[{name}] No token usage")
            return None

        usage = llm_response.usage_metadata
        tokens = self.total_token_usage(usage, name)
        callback_context.state["usage_tokens"] = {
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_tokens,
            "total_thoughts_token_count": self.total_thoughts_token_count,
            "total_tool_use_prompt_token_count": self.total_tool_use_prompt_token_count,
            "agents": self.agents,
        }

        logging.info(
            f"""Token Usage [{name}]:
            Prompt tokens: {tokens["prompt"]}
            Completion tokens: {tokens["completion"]}
            Thoughts tokens: {tokens["thoughts"]}
            Tools tokens: {tokens["tool_use_prompt"]}
            Total tokens: {tokens["total"]}"""
        )
        logging.info(
            f"""Cumulative:
            Prompt: {self.total_prompt_tokens}
            Completion: {self.total_completion_tokens}
            Thoughts: {self.total_thoughts_token_count}
            Tools: {self.total_tool_use_prompt_token_count}
            Total: {self.total_tokens}"""
        )

        return None
