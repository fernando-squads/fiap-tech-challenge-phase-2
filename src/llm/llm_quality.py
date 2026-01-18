from src.monitoring import logging
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import re

logger = logging.getLogger(__name__)

class LLMQualityEvaluator:
    """Avaliador de qualidade de explicações geradas por LLM usando métricas ROUGE e BLEU"""
    
    def __init__(self):
        self.rouge = Rouge()
        self.medical_terms = {
            'diabetes', 'glicose', 'insulina', 'resistência', 'pré-diabetes',
            'hiperglicemia', 'hipoglicemia', 'neuropatia', 'retinopatia',
            'nefropatia', 'complicações', 'metabolismo', 'endócrino',
            'pâncreas', 'hemoglobina', 'triglicerídeos', 'colesterol',
            'pressão', 'risco', 'diagnóstico', 'tratamento', 'prevenção'
        }
        
    def calculate_rouge(self, reference: str, hypothesis: str) -> dict:
        """
        Calcula ROUGE scores entre texto de referência e hipótese
        
        ROUGE-1: Unigram (palavras individuais)
        ROUGE-2: Bigram (pares de palavras)
        ROUGE-L: Longest Common Subsequence
        
        Args:
            reference: Texto esperado/de referência
            hypothesis: Texto gerado pelo LLM
            
        Returns:
            Dict com scores ROUGE-1, ROUGE-2, ROUGE-L
        """
        try:
            scores = self.rouge.get_scores(hypothesis, reference)[0]
            return {
                "rouge1": scores['rouge1']['f'],
                "rouge2": scores['rouge2']['f'],
                "rougeL": scores['rougeL']['f'],
            }
        except Exception as e:
            logger.error(f"Erro ao calcular ROUGE: {e}")
            return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
    
    def calculate_bleu(self, reference: str, hypothesis: str) -> float:
        """
        Calcula BLEU score (Bilingual Evaluation Understudy)
        
        BLEU mede correspondência com texto de referência usando n-gramas
        (1 a 4 gramas com pesos iguais)
        
        Args:
            reference: Texto esperado/de referência
            hypothesis: Texto gerado pelo LLM
            
        Returns:
            Score BLEU entre 0 e 1
        """
        try:
            ref_tokens = reference.lower().split()
            hyp_tokens = hypothesis.lower().split()
            
            # BLEU usa 1-gramas até 4-gramas
            weights = (0.25, 0.25, 0.25, 0.25)
            smooth = SmoothingFunction().method1
            
            bleu = sentence_bleu(
                [ref_tokens],
                hyp_tokens,
                weights=weights,
                smoothing_function=smooth
            )
            return bleu
        except Exception as e:
            logger.error(f"Erro ao calcular BLEU: {e}")
            return 0.0
    
    def count_medical_terms(self, text: str) -> dict:
        """
        Conta termos médicos relevantes presentes no texto
        
        Args:
            text: Texto gerado pelo LLM
            
        Returns:
            Dict com contagem e lista de termos encontrados
        """
        text_lower = text.lower()
        found_terms = []
        
        for term in self.medical_terms:
            if term in text_lower:
                found_terms.append(term)
        
        return {
            "total_medical_terms": len(found_terms),
            "terms_found": found_terms,
            "medical_density": len(found_terms) / len(self.medical_terms)
        }
    
    def check_response_validity(self, text: str) -> dict:
        """
        Verifica características básicas de validade da resposta
        
        Args:
            text: Texto gerado pelo LLM
            
        Returns:
            Dict com checks de validade
        """
        checks = {
            "is_not_empty": len(text.strip()) > 0,
            "min_length": len(text.split()) >= 20,  # Mínimo 20 palavras
            "has_sentences": len(re.split(r'[.!?]', text)) > 2,
            "contains_medical_context": len(self.count_medical_terms(text)["terms_found"]) > 0,
        }
        return checks
    
    def evaluate_llm_output(self, 
                          hypothesis: str, 
                          reference: str = None,
                          patient_data: dict = None) -> dict:
        """
        Avaliação completa de qualidade da saída LLM
        
        Args:
            hypothesis: Texto gerado pelo LLM
            reference: Texto de referência (opcional)
            patient_data: Dados do paciente para contexto (opcional)
            
        Returns:
            Dict com todas as métricas de qualidade
        """
        logger.info("Iniciando avaliação de qualidade LLM...")
        
        results = {
            "hypothesis": hypothesis,
            "reference": reference,
        }
        
        # Validação básica
        results["validity"] = self.check_response_validity(hypothesis)
        
        # Termos médicos
        results["medical_terms"] = self.count_medical_terms(hypothesis)
        
        # ROUGE (se houver referência)
        if reference:
            results["rouge"] = self.calculate_rouge(reference, hypothesis)
            logger.info(f"ROUGE scores: {results['rouge']}")
        
        # BLEU (se houver referência)
        if reference:
            results["bleu"] = self.calculate_bleu(reference, hypothesis)
            logger.info(f"BLEU score: {results['bleu']:.4f}")
        
        # Score global
        validity_score = sum(results["validity"].values()) / len(results["validity"])
        medical_density = results["medical_terms"]["medical_density"]
        
        results["overall_quality_score"] = (validity_score * 0.4) + (medical_density * 0.3)
        
        if "rouge" in results:
            rouge_avg = (results["rouge"]["rouge1"] + results["rouge"]["rougeL"]) / 2
            results["overall_quality_score"] += (rouge_avg * 0.3)
        
        logger.info(f"Avaliação concluída. Score geral: {results['overall_quality_score']:.4f}")
        
        return results
