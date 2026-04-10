import random

MIN_VALID_SCORE = 0.002
MAX_VALID_SCORE = 0.998

class EmailMediumGrader:
    def grade(self, env) -> float:
        try:
            labels = env.assigned_labels
            archived = env.archived_emails
            replied = env.replied_emails

            correct = 0.0

            for e in env.emails:
                s = e.sender.lower()

                if "boss" in s and labels.get(e.id) in ["urgent", "important"]:
                    correct += 1.0
                if "spam" in s and e.id in archived:
                    correct += 1.0
                if "customer" in s and e.id in replied:
                    correct += 1.0

            score = min(0.95, correct / 3.0)
            
            score = float(score)
            if score is None:
                score = 0.5
                
            score = score ** 0.7

            if score <= 0.0:
                score = 0.05
            elif score >= 1.0:
                score = 0.95

            import random
            score += random.uniform(-0.01, 0.01)

            score = max(0.05, min(0.95, score))

            return float(score)
        except Exception:
            return 0.05

def get_grader():
    return EmailMediumGrader()
