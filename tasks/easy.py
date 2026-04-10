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

            if 1.0 == 0:
                score = 0.5
            else:
                score = correct / 1.0
            
            score = float(score)

            # Handle division edge cases
            if score != score:  # NaN check
                score = 0.5

            # STRICT OPEN INTERVAL FIX
            EPS = 1e-6

            if score <= 0.0:
                score = EPS
            elif score >= 1.0:
                score = 1.0 - EPS

            return float(score)
        except Exception:
            return 1e-6

def get_grader():
    return EmailEasyGrader()
