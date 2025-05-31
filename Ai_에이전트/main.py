from rl_core.agent import RLAgent
from rl_core.reward_system import evaluate_experiment_result
from utils.idea_extractor import extract_ideas_from_summary

def simulate_experiment(idea):
    print(f"\n[실행 중] 아이디어: {idea}")
    fake_result = "Experiment with accuracy 0.81"
    print("[결과]:", fake_result)
    return fake_result

def main():
    # 가짜 논문 요약 하나 예시
    summary = "이 논문은 BERT 기반 텍스트 분류 기법을 제안하고, zero-shot 학습의 가능성을 탐구한다."

    # 자동으로 실험 아이디어 추출
    ideas = extract_ideas_from_summary(summary)
    state = {"ideas": ideas}

    print("📄 요약:", summary)
    print("🧠 추출된 실험 아이디어:", ideas)

    agent = RLAgent()

    for _ in range(3):
        action = agent.choose_action(state)
        if not action:
            print("더 이상 실행할 아이디어 없음")
            break

        result = simulate_experiment(action)
        reward = evaluate_experiment_result(result)
        agent.receive_reward(action, reward)

    print("\n📊 실행 결과 정리:")
    for action, score in agent.summarize_knowledge():
        print(f"{action} → 보상: {score}")

if __name__ == "__main__":
    main()
