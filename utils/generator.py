# utils/generator.py
from transformers import pipeline

# 모델 로딩 (필요시 모델명을 변경하세요)
generator = pipeline("text-generation", model="gpt2")

def generate_paper_summary(prompt: str, max_length: int = 150) -> dict:
    """
    주어진 프롬프트를 기반으로 논문 요약(또는 초록)을 생성한다.
    반환값은 원문 prompt와 생성된 텍스트를 포함한 dict.
    """
    if not prompt:
        raise ValueError("prompt cannot be empty")
    results = generator(prompt, max_length=max_length, num_return_sequences=1)
    text = results[0]["generated_text"].strip()
    return {"prompt": prompt, "generated_summary": text}
