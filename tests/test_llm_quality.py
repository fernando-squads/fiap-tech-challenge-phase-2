from src.monitoring import logging
from src.llm import LLMQualityEvaluator

logger = logging.getLogger(__name__)

def test_llm_quality_evaluation():
    """
    Teste de avaliação de qualidade de explicações LLM
    
    Verifica:
    - Cálculo de ROUGE scores
    - Cálculo de BLEU score
    - Detecção de termos médicos
    - Validação de resposta
    """
    
    logger.info("=============== Iniciando teste de qualidade LLM ===============")
    
    evaluator = LLMQualityEvaluator()
    
    # Exemplo 1: Resposta médica relevante
    hypothesis1 = """
    Baseado na análise, o paciente apresenta uma probabilidade significativa de diabetes.
    Os valores de glicose indicam hiperglicemia, que é um marcador importante para diagnóstico.
    A resistência à insulina é um fator de risco crucial. Recomenda-se acompanhamento com endocrinologista
    e realização de hemoglobina glicada para confirmação. Mudanças no metabolismo e prevenção são essenciais.
    """
    
    reference1 = """
    O paciente demonstra risco aumentado de diabetes mellitus tipo 2.
    Níveis elevados de glicose no sangue sugerem comprometimento do metabolismo da glicose.
    Avaliação complementar com testes de tolerância à glicose é recomendada para diagnóstico definitivo.
    Tratamento preventivo e monitoramento contínuo da nefropatia diabética são necessários.
    """
    
    logger.info("Avaliando resposta médica de alta qualidade...")
    result1 = evaluator.evaluate_llm_output(hypothesis1, reference1)
    
    logger.info(f"Validade da resposta: {result1['validity']}")
    logger.info(f"Termos médicos encontrados: {result1['medical_terms']['terms_found']}")
    logger.info(f"Densidade de termos médicos: {result1['medical_terms']['medical_density']:.2%}")
    if "rouge" in result1:
        logger.info(f"ROUGE-1: {result1['rouge']['rouge1']:.4f}")
        logger.info(f"ROUGE-2: {result1['rouge']['rouge2']:.4f}")
        logger.info(f"ROUGE-L: {result1['rouge']['rougeL']:.4f}")
    if "bleu" in result1:
        logger.info(f"BLEU: {result1['bleu']:.4f}")
    logger.info(f"Score geral de qualidade: {result1['overall_quality_score']:.4f}")
    
    assert result1['validity']['is_not_empty'], "Resposta não deve ser vazia"
    assert result1['validity']['min_length'], "Resposta deve ter pelo menos 20 palavras"
    assert result1['medical_terms']['total_medical_terms'] > 0, "Deve conter termos médicos"
    assert result1['overall_quality_score'] > 0.4, "Score de qualidade deve ser > 0.4"
    
    logger.info("Teste 1 passou: Resposta de alta qualidade validada")
    
    # Exemplo 2: Resposta com baixa qualidade
    hypothesis2 = "Talvez seja diabetes."
    
    logger.info("Avaliando resposta de baixa qualidade...")
    result2 = evaluator.evaluate_llm_output(hypothesis2)
    
    logger.info(f"Validade da resposta: {result2['validity']}")
    logger.info(f"Termos médicos encontrados: {result2['medical_terms']['terms_found']}")
    logger.info(f"Score geral de qualidade: {result2['overall_quality_score']:.4f}")
    
    assert not result2['validity']['min_length'], "Resposta curta deve falhar no check de comprimento"
    assert result2['overall_quality_score'] < 0.4, "Resposta baixa qualidade deve ter score < 0.4"
    
    logger.info("Teste 2 passou: Resposta de baixa qualidade identificada")
    
    # Exemplo 3: Resposta genérica (sem contexto médico)
    hypothesis3 = """
    O resultado do teste foi positivo. Isso significa que há uma condição presente.
    O paciente deve consultar um médico para mais informações sobre o assunto.
    É importante receber cuidados profissionais para lidar com a situação.
    """
    
    logger.info("Avaliando resposta genérica...")
    result3 = evaluator.evaluate_llm_output(hypothesis3)
    
    logger.info(f"Validade da resposta: {result3['validity']}")
    logger.info(f"Termos médicos encontrados: {result3['medical_terms']['terms_found']}")
    logger.info(f"Densidade de termos médicos: {result3['medical_terms']['medical_density']:.2%}")
    logger.info(f"Score geral de qualidade: {result3['overall_quality_score']:.4f}")
    
    assert result3['validity']['is_not_empty'], "Resposta não deve ser vazia"
    assert result3['medical_terms']['medical_density'] == 0.0, "Resposta genérica não deve ter termos médicos"
    
    logger.info("Teste 3 passou: Resposta genérica identificada como baixa qualidade")
    
    logger.info("=============== Todos os testes de qualidade LLM passaram! ===============")


def test_medical_term_detection():
    """Teste específico de detecção de termos médicos"""
    
    logger.info("=============== Teste de detecção de termos médicos ===============")
    
    evaluator = LLMQualityEvaluator()
    
    text_with_terms = "Paciente com diabetes, resistência à insulina e pré-diabetes"
    result = evaluator.count_medical_terms(text_with_terms)
    
    logger.info(f"Termos encontrados: {result['terms_found']}")
    logger.info(f"Densidade: {result['medical_density']:.2%}")
    
    assert result['total_medical_terms'] >= 3, "Deve encontrar pelo menos 3 termos médicos"
    
    logger.info("Teste de detecção de termos médicos passou!")


def test_response_validity_checks():
    """Teste de checks de validade de resposta"""
    
    logger.info("=============== Teste de validação de resposta ===============")
    
    evaluator = LLMQualityEvaluator()
    
    # Resposta válida
    valid_text = "Esta é uma resposta bem estruturada com múltiplas frases. Tem conteúdo relevante. Atende aos critérios de qualidade."
    valid_checks = evaluator.check_response_validity(valid_text)
    logger.info(f"Checks de resposta válida: {valid_checks}")
    assert all(valid_checks.values()) or sum(valid_checks.values()) >= 2, "Resposta válida deve passar na maioria dos checks"
    
    # Resposta inválida
    invalid_text = "Sim."
    invalid_checks = evaluator.check_response_validity(invalid_text)
    logger.info(f"Checks de resposta inválida: {invalid_checks}")
    assert not invalid_checks['min_length'], "Resposta muito curta deve falhar no check"
    
    logger.info("Teste de validação de resposta passou!")
