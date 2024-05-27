import gradio as gr


def logout_tab():
    with gr.Tab("登出"):
        with gr.Row():
            logout_button = gr.Button("登出", link="/logout")
