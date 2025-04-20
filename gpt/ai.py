import gpt_2_simple as gpt2
import os
import random

class ChatAI:
    """ ChatAI class handles GPT2 responses and learning """
    def __init__(self) -> None:
        self.sess = gpt2.start_tf_sess()


    def load_model(self) -> None:
        """ Load a pregenerated model to use to generate responses """
        gpt2.load_gpt2(self.sess)


    def generate_models(self, model_name: str, data_path: str) -> None:
        """ Generate new models given a model name and data source path. Data source path being a pre-existing gpt2 learning model """
        print(os.path.join("models", model_name))
        if not os.path.isdir(os.path.join("models", model_name)):
            print(f"Downloading {model_name} model...")
            gpt2.download_gpt2(model_name=model_name)

        gpt2.finetune(
            self.sess,
            data_path,
            learning_rate=0.0001, # 0.00001 if more than 10mb of training data
            model_name=model_name,
            checkpoint_dir="checkpoint",
            restore_from="latest",
            batch_size=1,
            steps=1000,
            print_every=5,
            sample_every=100,
            sample_length=100,
            save_every=200
            )
        gpt2.generate(self.sess)


    def get_bot_response(self, model_name: str, author: str, message: str) -> str:
        """ Get a response to a given message using GPT2 model """
        prompt = f"""
{author}: {message}

Lana:"""
        return gpt2.generate(self.sess,
                            model_name=model_name,
                            length=random.randint(10, 100),
                            prefix=prompt,
                            temperature=0.85,
                            include_prefix=False,
                            return_as_list=True,
                            )[0]