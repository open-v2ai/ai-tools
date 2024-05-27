from datetime import datetime

import pandas as pd
import gradio as gr

from util.conf import get_conf
from util.llm import get_client


conf = get_conf()
client = get_client(conf)


def preview_table(file):
    if file is None:
        return None, gr.update(visible=False), None, None
    else:
        df = pd.read_csv(file.name) if file.name.endswith('.csv') else pd.read_excel(file.name)
        if df.shape[0] == 0:
            return None, gr.update(visible=False), None, None
        else:
            if "内容" not in df.columns:
                raise gr.Error("表格中未找到「内容」列")
            else:
                return df.head(), gr.update(visible=True), df, df["内容"][0]


def openai_chat(content, prompt):
    if client.api_key == "":
        raise gr.Error("请先在 conf/default.yaml 中配置 api_key")

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"## 原内容\n{content}\n\n## 生成要求\n{prompt}\n\n## 改写内容"
            }
        ],
        max_tokens=1000,
        model=conf["llm"]["tongyi"]["model"]
    )
    return response.choices[0].message.content


def gen_all_content(df, prompt, progress=gr.Progress()):
    gen_content_list = []
    for content in progress.tqdm(df["内容"], total=len(df["内容"])):
        gen_content_list.append(openai_chat(content, prompt))

    df["生成的内容"] = gen_content_list
    file_path = f"./data/输出-{datetime.now()}.xlsx"
    df.to_excel(file_path, index=False)
    return file_path


def build_content():
    with gr.Tab("批量内容生成"):
        with gr.Row():
            with gr.Column():
                gr.Markdown("## 1 输入表格")

                file_input = gr.File(label="上传表格文件")
                input_preview = gr.DataFrame(label="表格预览", visible=False)

                origin_table = gr.DataFrame(label="表格数据", visible=False)

            with gr.Column():
                gr.Markdown("## 2 写提示词")

                preview_single_content = gr.Textbox("", label="预览单条内容", lines=10, show_copy_button=True)

                input_prompt = gr.Textbox(conf["prompt"], label="请输入提示词", lines=6, show_copy_button=True)

                gen_once_button = gr.Button("生成单条")
                gen_all_button = gr.Button("生成所有", variant="primary")

            with gr.Column():
                gr.Markdown("## 3 输出表格")

                preview_single_result = gr.Textbox(label="预览单条结果", lines=10, show_copy_button=True)

                output_file = gr.File(label="下载表格文件")

    file_input.change(preview_table,
                      inputs=file_input,
                      outputs=[input_preview, input_preview, origin_table, preview_single_content])

    gen_once_button.click(openai_chat,
                          inputs=[preview_single_content, input_prompt],
                          outputs=[preview_single_result])
    gen_all_button.click(gen_all_content,
                         inputs=[origin_table, input_prompt],
                         outputs=[output_file])
