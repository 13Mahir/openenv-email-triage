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

            correctness_score = (correctness_points / max_points) * 0.5 if max_points > 0 else 0
            quality_score = min(1.0, reply_quality_points / max_reply_points) * 0.2
            
            efficiency_ratio = max(0.0, 1.0 - (abs(env.current_step - 6) / 20.0))
            if len(env.action_history) > 6: efficiency_ratio *= 0.5
            efficiency_score = efficiency_ratio * 0.2
            
            priority_score = priority_points * 0.1
            
            total_score = correctness_score + quality_score + efficiency_score + priority_score
            score = min(0.96, total_score)
            
            score = score * 2.5
            score = score * 0.6 + 0.05
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
    return EmailHardGrader()
