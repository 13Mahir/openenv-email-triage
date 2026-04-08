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

            score = min(0.95, correct)
            
            score = float(score)
            if score is None:
                score = 0.5

            if score <= 0.0:
                score = 0.05
            elif score >= 1.0:
                score = 0.95

            score = max(MIN_VALID_SCORE, min(MAX_VALID_SCORE, score))
            return score
        except Exception:
            return MIN_VALID_SCORE

def get_grader():
    return EmailEasyGrader()
