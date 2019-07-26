from overrides import overrides
from pytorch_transformers import GPT2Config, GPT2LMHeadModel
import torch

from allennlp.modules.language_model_heads.language_model_head import LanguageModelHead


@LanguageModelHead.register('gpt2')
class Gpt2LanguageModelHead(LanguageModelHead):
    def __init__(self, model_name: str) -> None:
        super().__init__()
        config = GPT2Config.from_pretrained(model_name)
        self.input_dim = config.hidden_size
        self.output_dim = config.vocab_size
        gpt2_model = GPT2LMHeadModel.from_pretrained(model_name)
        self.gpt2_lm_head = gpt2_model.lm_head

    @overrides
    def get_input_dim(self) -> int:
        return self.input_dim

    @overrides
    def get_output_dim(self) -> int:
        return self.output_dim

    def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:
        return self.gpt2_lm_head(hidden_states)