import random

MIN_VALID_SCORE = 0.002
MAX_VALID_SCORE = 0.998

class EmailHardGrader:
    def grade(self, env) -> float:
        try:
            labels = env.assigned_labels
            archived = env.archived_emails
            replied = env.replied_emails
            resolved_order = getattr(env, 'resolved_emails', [])
            
            correctness_points = 0.0
            max_points = len(env.emails) * 1.0
            
            reply_quality_points = 0.0
            max_reply_points = 1.0
            
            priority_points = 0.0
            
            boss_id = None
            customer_id = None
            dev_id = None
            
            for email in env.emails:
                sender = email.sender.lower()
                subj = email.subject.lower()
                body = email.body.lower()
                eid = email.id
                
                if "boss" in sender or "urgent" in subj:
                    boss_id = eid
                    if labels.get(eid) in ["urgent", "important", "high"]: correctness_points += 1.0
                elif "spam" in sender or "win" in body:
                    if eid in archived: correctness_points += 1.0
                elif "customer" in sender:
                    customer_id = eid
                    if eid in replied:
                        correctness_points += 1.0
                        r_txt = replied[eid].lower()
                        if "sorry" in r_txt or "apologize" in r_txt: reply_quality_points += 0.4
                        if "resolve" in r_txt or "reset" in r_txt or "fix" in r_txt: reply_quality_points += 0.4
                        if "\n" in r_txt or len(r_txt) > 30: reply_quality_points += 0.2
                elif "hr" in sender:
                    if labels.get(eid) in ["internal", "hr", "policy"]: correctness_points += 1.0
                elif "dev" in sender:
                    dev_id = eid
                    if labels.get(eid) in ["review", "pr", "dev"]: correctness_points += 1.0

            if resolved_order:
                if boss_id and resolved_order[0] == boss_id:
                    priority_points += 0.5
                
                if customer_id and dev_id:
                    if customer_id in resolved_order and dev_id in resolved_order:
                        if resolved_order.index(customer_id) < resolved_order.index(dev_id):
                            priority_points += 0.5
                    elif customer_id in resolved_order:
                        priority_points += 0.5

            if max_points == 0:
                c_ratio = 0.0
            else:
                c_ratio = correctness_points / max_points
            
            score = 0.1 # Base score for hard
            
            if correctness_points > 0:
                score += c_ratio * 0.4
                
            if reply_quality_points > 0:
                q_ratio = min(1.0, reply_quality_points / 1.0)
                score += q_ratio * 0.2
                
            if priority_points > 0:
                score += priority_points * 0.1
                
            score += min(0.19, len(env.action_history) * 0.02)
            
            score = float(score)

            # Handle invalid values
            if score is None or score != score:
                score = 0.5

            # Hardcode bounds between 0.05 and 0.95 as requested
            score = max(0.05, min(0.95, score))

            return float(score)
        except Exception:
            return 0.5

def get_grader():
    return EmailHardGrader()
