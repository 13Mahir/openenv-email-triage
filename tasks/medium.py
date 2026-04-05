class EmailMediumGrader:
    def grade(self, env) -> float:
        labels = env.assigned_labels
        archived = env.archived_emails
        replied = env.replied_emails
        correct = 0.0
        
        for e in env.emails:
            if "boss" in e.sender.lower():
                if labels.get(e.id) in ["urgent", "important"]: correct += 1.0
            if "spam" in e.sender.lower():
                if e.id in archived: correct += 1.0
            if "customer" in e.sender.lower():
                if e.id in replied: correct += 1.0
                
        eff = max(0.0, 1.0 - (env.current_step / 10.0))
        return min(0.95, (correct/3.0) * 0.7 + eff * 0.3)

def get_grader():
    return EmailMediumGrader()
