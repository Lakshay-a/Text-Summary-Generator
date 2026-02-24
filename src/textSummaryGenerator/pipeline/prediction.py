from textSummaryGenerator.config.configuration import ConfigurationManager
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()
        if torch.cuda.is_available():
            self.device = "cuda"
        elif torch.backends.mps.is_available():
            self.device = "mps"
        else:
            self.device = "cpu"

        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(self.device)

    def predict(self, text: str):
        gen_kwargs = {
            "length_penalty": 0.8,
            "num_beams": 4,
            "max_length": 128,
        }

        print("Dialogue:")
        print(text)

        # T5 needs prefix
        input_text = "summarize: " + text

        inputs = self.tokenizer(
            input_text,
            max_length=1024,
            truncation=True,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        with torch.no_grad():
            summary_ids = self.model.generate(**inputs, **gen_kwargs)
        output = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        print("\nModel Summary:")
        print(output)

        return output
