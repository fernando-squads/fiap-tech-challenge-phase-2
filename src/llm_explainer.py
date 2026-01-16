from openai import OpenAI

def explain_with_llm(features, shap_values):
    prompt = f"""
    Explique em linguagem médica simples o diagnóstico de diabetes
    com base nos seguintes fatores:

    Features: {features}
    Importâncias: {shap_values}
    """

    client = OpenAI()




    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.choices[0].message.content