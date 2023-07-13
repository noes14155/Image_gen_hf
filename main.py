from gradio_client import Client
import time
import gradio as gr
import threading
models = [
    {"name": "Deliberate", "url": "Masagin/Deliberate"},
    {"name": "Dreamlike Anime", "url": "dreamlike-art/dreamlike-anime-1.0"},
    
]

current_model = models[0]

models2 = []
for model in models:
    model_url = f"models/{model['url']}"
    loaded_model = gr.Interface.load(model_url, live=True)
    models2.append(loaded_model)

def send_it(inputs, model_choice):
    proc = models2[model_choice]
    return proc(inputs)

def dropdown_change():
    send_it(input_text, model_name1)

with gr.Blocks() as myface:
    gr.HTML()

    with gr.Column():
        with gr.Row():
            input_text = gr.Textbox(label="Prompt idea",  placeholder="", lines=1)
            model_name1 = gr.Dropdown(
                        label="Choose Model",
                        choices=[m["name"] for m in models],
                        type="index",
                        value=current_model["name"],
                        interactive=True 
            )
        
            run = gr.Button("Generate Images", variant="primary")    
        with gr.Row():
            output1 = gr.Image(label="")
    model_name1.change(send_it, inputs=[input_text, model_name1], outputs=[output1])
    run.click(send_it, inputs=[input_text, model_name1], outputs=[output1])

myface.queue(concurrency_count=200)
def launch_gradio():
    myface.launch(inline=True, server_port=7860)
def generate_image(prompt,model):
    client = Client("http://127.0.0.1:7860")
    job = client.submit(prompt,model,fn_index=1)

    statuses = []
    while not job.done():
        time.sleep(0.5)
        print("in progress")
    print(job.future.result())
def main():
    gradio_thread = threading.Thread(target=launch_gradio)
    gradio_thread.start()
    time.sleep(5)
    for model in models:
        generate_image('house',model['name'])
    
if __name__ == '__main__':
    main()
