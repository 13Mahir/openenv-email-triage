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
            return float(max(0.0, min(1.0, score)))
        except Exception:
            return 0.0

def get_grader():
    return EmailEasyGrader()
