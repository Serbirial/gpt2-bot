from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen
import os
import random
tokenizer_file = "aitextgen.tokenizer.json" 

config = GPT2ConfigCPU()

class ChatAI:
    """ ChatAI class handles GPT2 responses and learning """
    def __init__(self) -> None:
        self.ai = aitextgen(tokenizer_file=tokenizer_file, config=config)


    def load_model(self) -> None:
        """ Load a pregenerated model to use to generate responses """
        self.ai = aitextgen(model_folder="trained_model",
                tokenizer_file=tokenizer_file)


    def generate_models(self, data_path: str) -> None:
        """ Generate new models given a model name and data source path. Data source path being a pre-existing gpt2 learning model """
        #print(os.path.join("models", model_name))
        #if not os.path.isdir(os.path.join("models", model_name)):
        #    print(f"Downloading {model_name} model...")
        #    gpt2.download_gpt2(model_name=model_name)

        train_tokenizer(data_path)
        data = TokenDataset(data_path, tokenizer_file=tokenizer_file, block_size=64)

        self.ai.train(data, batch_size=4, num_steps=5000, generate_every=5000, save_every=5000)

        #gpt2.finetune(
        #    self.sess,
        #    data_path,
        #    model_name=model_name,
        #    checkpoint_dir="checkpoint",
        #    restore_from="latest",
        #    batch_size=1,
        #    sample_every=100,
        #    sample_length=100,
        #    save_every=100
        #    )
        #gpt2.generate(self.sess)


    def get_bot_response(self, author: str, message: str) -> str:
        """ Get a response to a given message using GPT2 model """
        return self.ai.generate(
                            length=random.randint(10, 30),
                            prompt=author + ": " + message
                            )