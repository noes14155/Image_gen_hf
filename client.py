import time
from gradio_client import Client
from server import gradio_server
def generate_image(prompt, model):
    client = Client("http://127.0.0.1:7860")
    start_time = time.time()
    job = client.submit(prompt, model, fn_index=1)
    while not job.done():
        time.sleep(0.5)
        end_time = time.time()
        print(f"Elapsed time: {time.strftime('%M:%S', time.gmtime(end_time - start_time))}")
    print(f"Remaining time: {time.strftime('%M:%S', time.gmtime(end_time - start_time))}")
    print(job.future.result())

def main():   
    gr = gradio_server()
    time.sleep(5)
    for model in gr.models:
        generate_image('house',model['name'])    
if __name__ == '__main__':
    main()
