import os
from llama_cpp import Llama

class NaturalistAgent:
    def __init__(self, model_path="models/Llama-3.2-1B-Instruct-Q4_K_M.gguf"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model missing: {model_path}. Run ./download_models.sh")
        self.llm = Llama(model_path=model_path, n_ctx=512, n_threads=4, verbose=False)

    def generate_cue(self, species_name: str) -> str:
        prompt = (
            "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
            "You are a quiet backcountry trail guide. When given a creature name, "
            "reply with ONE short sentence (under 15 words) telling where to look. "
            "No conversational fluff.<|eot_id|>\n"
            "<|start_header_id|>user<|end_header_id|>\n"
            f"Detected species: {species_name}<|eot_id|>\n"
            "<|start_header_id|>assistant<|end_header_id|>\n"
        )
        out = self.llm(prompt, max_tokens=30, stop=["<|eot_id|>", "\n"], temperature=0.3)
        return out["choices"][0]["text"].strip().replace('"', '')
