from functools import lru_cache
from typing import Optional, Type
import tiktoken

from pyprompt.chatgpt_models import GPTModel

encoding_er = tiktoken.get_encoding("cl100k_base")


@lru_cache(maxsize=128)
def count_token(string: Type[str], for_model: Optional[GPTModel] = None):
    """Count the number of tokens in the prompt."""
    num_tokens = len(encoding_er.encode(string))
    return num_tokens
