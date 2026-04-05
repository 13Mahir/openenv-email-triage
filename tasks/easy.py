class EmailEasyGrader:
    def grade(self, env) -> float:
        labels = env.assigned_labels
        correct = 0.0
        for e in env.emails:
            if "boss" in e.sender.lower():
                if labels.get(e.id) in ["urgent", "important"]: correct = 1.0
                
        eff = max(0.0, 1.0 - (env.current_step / 10.0))
        return min(0.95, correct * 0.7 + eff * 0.3)

def get_grader():
    return EmailEasyGrader()
