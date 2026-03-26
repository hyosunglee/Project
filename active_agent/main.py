import time
import os
import sys

# Standard relative pathing for a modular agent
# Ensure the parent directory is in sys.path to resolve internal modules correctly.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from monitor.system import get_memory_usage
from monitor.research import search_ai_feedback_loop_papers
from brain.gemini import judge_intervention
from output.notifier import notify
from config.settings import USER_CONTEXT, POLLING_INTERVAL_SECONDS, NOTIF_TITLE

def run_loop():
    print(f"🚀 Active AI Agent started. Polling every {POLLING_INTERVAL_SECONDS/60} minutes...")

    while True:
        try:
            # 1. Monitoring
            print("🔍 Monitoring system and research...")
            memory_info = get_memory_usage()
            # Search with the user's core interest
            research_results = search_ai_feedback_loop_papers(max_results=3)

            # 2. Judgment
            print("🧠 Asking Gemini for intervention advice...")
            should_intervene, decision = judge_intervention(memory_info, research_results, USER_CONTEXT)

            # 3. Intervention
            if should_intervene:
                message = decision.get("message", "새로운 정보가 있습니다!")
                print(f"✨ Intervention triggered: {message}")
                notify(NOTIF_TITLE, message)
            else:
                reason = decision.get("reason", "No intervention needed.")
                print(f"✅ No intervention: {reason}")

        except Exception as e:
            print(f"🔥 Unexpected error in loop: {e}")
            import traceback
            traceback.print_exc()

        # 4. Wait for the next poll
        print(f"⏳ Waiting for next check...")
        time.sleep(POLLING_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_loop()
