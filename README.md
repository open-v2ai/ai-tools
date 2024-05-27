# AI Tools

🔥快捷好用的 AI 工具！

## Getting started

默认使用阿里云的千问模型，可以在这里开通[「API」](https://bailian.console.aliyun.com/)。

```shell
llm:
  tongyi:
    model: "qwen-long"
    base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    api_key: ""
```

本地运行：

```shell
conda create -n ai-tools python=3.8
conda activate ai-tools

pip install -r requirements.txt

python -m server.main
```

服务器部署：(需要先创建 `conf/default.prod.yaml`)

```shell
DATETIME=$(date +%Y%m%d-%H%M%S)

docker build -t ai-tools:$DATETIME .

docker rm -f ai-tools

docker run -d --restart=always --name ai-tools \
  -p 10002:8000 -e ENV=prod \
  -v $PWD/conf:/app/conf \
  -v $PWD/data:/app/data \
  ai-tools:$DATETIME

docker logs -f ai-tools
```

## Reference

- [Running a Gradio App on your Web Server with Nginx](https://www.gradio.app/guides/running-gradio-on-your-web-server-with-nginx)
