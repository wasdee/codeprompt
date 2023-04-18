from typing import Optional
from pyprompt.chatgpt_models import GPTModel
from pyprompt.techniques.count_token import count_token


class PromptStr(str):
    for_model: Optional[GPTModel] = None

    def count_token(self):
        return count_token(self, for_model=self.for_model)
