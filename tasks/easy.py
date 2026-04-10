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

            # Handle invalid values
            if score is None or score != score:
                score = 0.5

            EPS = 1e-6

            # Enforce strict open interval (0,1)
            score = max(EPS, min(1.0 - EPS, score))

            return float(score)
        except Exception:
            return 0.5

def get_grader():
    return EmailEasyGrader()
