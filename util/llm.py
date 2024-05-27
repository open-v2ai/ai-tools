from openai import OpenAI


def get_client(conf):
    return OpenAI(
        api_key=conf["llm"]["tongyi"]["api_key"],
        base_url=conf["llm"]["tongyi"]["base_url"],
    )
