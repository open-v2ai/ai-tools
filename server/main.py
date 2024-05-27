import gradio as gr

from app.generate_content import build_content
from app.logout import logout_tab

from util.conf import get_conf

conf = get_conf()
auth_conf = conf["auth"]

if __name__ == '__main__':
    with gr.Blocks() as app:
        build_content()
        logout_tab()

    app.launch(auth=(auth_conf["username"], auth_conf["password"]), **conf["server"])
