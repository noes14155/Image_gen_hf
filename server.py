from gradio_client import Client
import time
import gradio as gr
import threading

class gradio_server:
    def __init__(self) -> None:
        self.models = [
                {"name": "Deliberate", "url": "Masagin/Deliberate"},
                {"name": "Dreamlike Anime", "url": "dreamlike-art/dreamlike-anime-1.0"},
                ]
        #self.current_model = models[0]
        self.models2 = []
        for model in self.models:
            model_url = f"models/{model['url']}"
            loaded_model = gr.Interface.load(model_url, live=True)
            self.models2.append(loaded_model)
        self.interface()
        gradio_thread = threading.Thread(target=self.launch_gradio)
        gradio_thread.start()
    def send_it(self, inputs, model_choice):
        proc = self.models2[model_choice]
        return proc(inputs)

    def dropdown_change(self):
        self.send_it(self.input_text, self.model_name1)

    def interface(self):
        with gr.Blocks() as self.myface:
            gr.HTML()
            with gr.Column():
                with gr.Row():
                    self.input_text = gr.Textbox(label="Prompt idea",  placeholder="", lines=1)
                    self.model_name1 = gr.Dropdown(
                                label="Choose Model",
                                choices=[m["name"] for m in self.models],
                                type="index",
                                value=self.models[0]['name'],
                                interactive=True 
                    )

                    run = gr.Button("Generate Images", variant="primary")    
                with gr.Row():
                    output1 = gr.Image(label="")
            self.model_name1.change(self.send_it, inputs=[self.input_text, self.model_name1], outputs=[output1])
            run.click(self.send_it, inputs=[self.input_text, self.model_name1], outputs=[output1])
            self.myface.queue(concurrency_count=200)
    def launch_gradio(self):
        self.myface.launch(inline=True, server_port=7860)

