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

            total = 3.0
            if total == 0:
                score = 0.5
            else:
                score = correct / total
            
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
    return EmailMediumGrader()
