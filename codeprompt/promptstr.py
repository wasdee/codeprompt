from typing import Optional
from codeprompt.chatgpt_models import GPTModel
from codeprompt.techniques.count_token import count_token


class PromptStr(str):
    for_model: Optional[GPTModel] = None

    def count_token(self):
        return count_token(self, for_model=self.for_model)
