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
            return float(max(0.0, min(1.0, score)))
        except Exception:
            return 0.0

def get_grader():
    return EmailMediumGrader()
