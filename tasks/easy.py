import random

MIN_VALID_SCORE = 0.002
MAX_VALID_SCORE = 0.998

class EmailEasyGrader:
    def grade(self, env) -> float:
        try:
            labels = env.assigned_labels
            correct = 0.0

            for e in env.emails:
                if "boss" in e.sender.lower():
                    if labels.get(e.id) in ["urgent", "important"]:
                        correct = 1.0

            score = 0.5 # Base score for easy
            
            if correct > 0:
                score += 0.3
                
            score += min(0.15, len(env.action_history) * 0.02)
            
            score = float(score)

            # Handle invalid values
            if score is None or score != score:
                score = 0.5

            # Hardcode bounds between 0.05 and 0.95 as requested
            score = max(0.05, min(0.95, score))

            return float(score)
        except Exception:
            return 0.5

def get_grader():
    return EmailEasyGrader()
