# -*- coding: utf-8 -*-

"""
AiChatDuel.py
두 AI 주어진 토픽에 대해 번갈아가며 토론하는 시뮬레이터입니다.
- Groq API 사용 (환경변수 Groq_API_KEY 필요)
"""

from groq import Groq

def judge_ai(topic, history):
    history_text = "\n".join(history)

    prompt = f"""
토론 주제: {topic}

다음은 두 AI(A, B)의 전체 토론 내용이다:

{history_text}

● 너는 공정한 심판 AI이고, AI_A, AI_B의 주장을 평가해야 한다.
● 평가 기준: 논리적 일관성, 근거의 강도, 반박 능력, 명확성.
● 'AI_A' 또는 'AI_B' 중 승자를 선택하고, 반드시 5문장 이내로 이유를 설명하라.
● 출력 형식:
승자: AI_A 또는 AI_B
이유: (이유 작성)
주의: 출력은 반드시 100% 자연스러운 한국어로만 작성하라.
중국어, 일본어, 베트남어, 러시아어 등 한국어 외 다른 언어 문자가 포함되면 안 된다.
단어가 끊기거나 비정상적으로 띄어쓰기 되지 않도록 하라.

"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=470,
        temperature=0.3,
    )
    return response.choices[0].message.content

def ask_ai(model, last_message):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "너는 토론 AI다. 상대의 주장을 분석하고 새로운 논리를 사용해 반박하라. "
                    "절대 같은 문장을 반복하지 마라."
                    "말은 길게 하지 말고 명확하게, 5문장 이하로 제한한다."
                    "출력은 반드시 100% 자연스러운 한국어로만 작성하라. 중국어, 일본어, 베트남어, 러시아어 등 한국어 외 다른 언어 문자가 절대로 포함되면 안 된다."
                    "단어가 끊기거나 비정상적으로 띄어쓰기 되지 않도록 하라."
                )
            },
            {"role": "user", "content": last_message}
        ],
        max_tokens=250,
        temperature=0.8,
        stop=["\n\n"],
    )
    return response.choices[0].message.content

def ai_duel():
    topic = input("토론 주제: ") # 적극적 안락사 합법화, 할부 vs 일시불, 과거로 돌아가기 vs 미래 보기
    print(f"토론 시작! 주제: {topic}")

    model_a = "llama-3.1-8b-instant"       
    model_b = "llama-3.3-70b-versatile"    

    last_message = f"주제: {topic}\n이 주제에 대해 첫 주장을 제시하라."

    history = []

    # 5턴 진행
    for turn in range(1, 6):
        print(f"\n--- 턴 {turn} ---")

        # A 발언
        a_msg = ask_ai(model_a, last_message)
        print("AI_A:", a_msg)
        history.append(f"[턴 {turn}] AI_A: {a_msg}")

        # B 발언
        b_msg = ask_ai(model_b, a_msg)
        print("AI_B:", b_msg)
        history.append(f"[턴 {turn}] AI_B: {b_msg}")

        last_message = b_msg

    print("\n=== 심판 판정 ===")
    judge_result = judge_ai(topic, history)
    print(judge_result)

    print("\n=== 대전 종료 ===")

if __name__ == "__main__":
    ai_duel()