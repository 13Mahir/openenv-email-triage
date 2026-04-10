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
    return EmailMediumGrader()
