from src.monitoring import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

def explain_with_llm(features, shap_values, prob):
    logger.info(f"Utilizando LLM...")
    metrics = "{'accuracy': 0.7467532467532467, 'recall': 0.6296296296296297, 'f1': 0.6355140186915887, 'fitness': 0.6706322983581551}";
    prompt = f"""
    Criamos um modelo utilizando rede neural que que possui as seguintes métricas {metrics}

    Foi passado para o modelo as informações abaixo:
        Parâmetros: {features}
        Valores: {shap_values}

    O resultado da previsão foi {prob}

    Explique em linguagem médica o diagnóstico de diabetes baseado nas informações acima
    """

    client = OpenAI()

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    logger.info(f"Utilizando LLM...(OK)")

    return response.output_text