from typing import Tuple, Dict, Any, List, Optional
import random
from models import Observation, Action, Email

class OpenEnv:
    def __init__(self, seed: int = 42):
        import time
        self.max_steps = 20
        self.current_step = 0
        self.seed = int(time.time() * 1000) % 100000
        self.rng = random.Random(self.seed)
        
        base_emails = [
            ("boss@corp.com", ["Urgent: Server Down", "Emergency: PROD Down", "Critical Outage"], ["Fix it now!", "Server is unresponsive, look into it immediately!", "Immediate action needed."]),
            ("spam@offer.com", ["Win $1000", "Claim your prize", "You won a car"], ["Click here to win!", "You are selected for a $1000 gift card.", "Act now and claim."]),
            ("customer@client.com", ["Help with login", "Login issue", "Cannot access account"], ["I can't login.", "Reset my password please, I am locked out.", "App keeps crashing during login."]),
            ("hr@corp.com", ["Policy Update", "New HR Policy", "Important Benefits Update"], ["Please read attached.", "Check the updated employee handbook.", "Read the annual compliance policy."]),
            ("dev@corp.com", ["PR Review", "Code Review Request", "Please review code"], ["Review my PR.", "Can you approve my merge request?", "I fixed the bugs, please review."]),
            ("newsletter@corp.com", ["Weekly Digest", "Tech News", "Company Newsletter"], ["Here is what happened this week.", "Top articles for you.", "Read our monthly recap."]),
            ("noreply@system.com", ["Notice of maintenance", "System update", "Build Failed"], ["Expect downtime this weekend.", "We are updating features.", "Your pipeline failed."])
        ]
        
        self.emails = []
        for i, (sender, subjs, bodies) in enumerate(base_emails):
            if "boss" not in sender and "customer" not in sender:
                if self.rng.random() < 0.2:
                    continue 

            subj = self.rng.choice(subjs)
            body = self.rng.choice(bodies)
            eid = f"msg_{self.rng.randint(1000, 9999)}_{i}"
            self.emails.append(Email(id=eid, sender=sender, subject=subj, body=body))
            
        for i in range(self.rng.randint(0, 2)):
            eid = f"msg_{self.rng.randint(1000, 9999)}_ext_{i}"
            n_type = self.rng.choice(["newsletter", "spam", "noreply"])
            if n_type == "newsletter":
                self.emails.append(Email(id=eid, sender="newsletter@corp.com", subject="Extra updates", body="Daily digest."))
            elif n_type == "spam":
                self.emails.append(Email(id=eid, sender="spam@offer.com", subject="You are the 100th visitor!", body="Claim prize."))
            else:
                self.emails.append(Email(id=eid, sender="noreply@system.com", subject="Alert", body="Storage full."))

        self.rng.shuffle(self.emails)
        
        self.assigned_labels: Dict[str, str] = {}
        self.archived_emails: List[str] = []
        self.replied_emails: Dict[str, str] = {}
        self.action_history: set = set()
        self.resolved_emails: List[str] = []
        self.last_reply_text: str = ""

    def reset(self) -> Observation:
        self.current_step = 0
        self.assigned_labels = {}
        self.archived_emails = []
        self.replied_emails = {}
        self.action_history = set()
        self.resolved_emails = []
        self.last_reply_text = ""
        return self._get_observation()

    def state(self) -> Observation:
        return self._get_observation()

    def _get_observation(self) -> Observation:
        truncated_inbox = []
        for e in self.emails:
            if e.id not in self.archived_emails:
                truncated_inbox.append(Email(
                    id=e.id, 
                    sender=e.sender, 
                    subject=e.subject, 
                    body=e.body[:50]
                ))
                
        return Observation(
            inbox=truncated_inbox,
            assigned_labels=self.assigned_labels,
            archived_emails=self.archived_emails,
            replied_emails=self.replied_emails,
            available_actions=["assign_label", "archive", "reply", "finish"]
        )

    def _get_email_by_id(self, email_id: str) -> Optional[Email]:
        return next((e for e in self.emails if e.id == email_id), None)

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict[str, Any]]:
        self.current_step += 1
        reward = -0.01  
        done = False
        info = {"msg": "Action executed."}

        action_hash = f"{action.action_type}_{action.email_id}"
        if action_hash in self.action_history and action.action_type != "finish":
            reward -= 0.1
            info["msg"] = "Repeated action penalty."
        
        if action.action_type != "finish":
            self.action_history.add(action_hash)

        target_email = self._get_email_by_id(action.email_id) if action.email_id else None

        if target_email and target_email.id not in self.resolved_emails:
            self.resolved_emails.append(target_email.id)
            
            if len(self.resolved_emails) == 1 and ("boss" in target_email.sender.lower() or "urgent" in target_email.subject.lower()):
                reward += 0.1
            
            if "customer" in target_email.sender.lower():
                dev_processed = any("dev" in self._get_email_by_id(i).sender.lower() for i in self.resolved_emails if self._get_email_by_id(i))
                if not dev_processed:
                    reward += 0.1

        if action.action_type == "assign_label" and target_email and action.label:
            lbl = action.label.lower()
            self.assigned_labels[target_email.id] = lbl
            info["msg"] = f"Label '{lbl}' assigned to {target_email.id}"
            
            sender = target_email.sender.lower()
            subj = target_email.subject.lower()
            
            if "boss" in sender or "urgent" in subj or "emergency" in subj:
                if lbl == "urgent": reward += 0.1
                elif lbl == "important": reward += 0.05
                else: reward -= 0.1
            elif "hr" in sender:
                if lbl == "internal" or lbl == "hr": reward += 0.1
                else: reward -= 0.1
            elif "dev" in sender:
                if lbl == "review" or lbl == "pr": reward += 0.1
                else: reward -= 0.1
            else:
                reward -= 0.05
                
        elif action.action_type == "archive" and target_email:
            if target_email.id not in self.archived_emails:
                self.archived_emails.append(target_email.id)
            info["msg"] = f"Email {target_email.id} archived."
            
            sender = target_email.sender.lower()
            body = target_email.body.lower()
            
            if "spam" in sender or "win" in body or "prize" in body:
                reward += 0.15
            elif "newsletter" in sender:
                reward += 0.1
            elif "boss" in sender or "customer" in sender:
                reward -= 0.3
            else:
                reward -= 0.1
                
        elif action.action_type == "reply" and target_email and action.reply_text:
            self.replied_emails[target_email.id] = action.reply_text
            info["msg"] = f"Replied to {target_email.id}."
            
            sender = target_email.sender.lower()
            r_txt = action.reply_text.lower()
            
            if len(self.replied_emails) > 2:
                reward -= 0.1
                
            if self.last_reply_text == r_txt:
                reward -= 0.15
            self.last_reply_text = r_txt
            
            if "noreply" in sender:
                reward -= 0.25
                
            if "customer" in sender:
                reward += 0.05
                qual_rew = 0.0
                if "sorry" in r_txt or "apologize" in r_txt: qual_rew += 0.1
                if "help" in r_txt or "resolve" in r_txt or "reset" in r_txt or "fix" in r_txt: qual_rew += 0.1
                if "\n" in r_txt or len(action.reply_text) > 30: qual_rew += 0.1
                
                if len(action.reply_text) < 10:
                    reward -= 0.1
                else:
                    reward += qual_rew
            elif "spam" in sender:
                reward -= 0.2
            elif "newsletter" in sender:
                reward -= 0.1
            else:
                reward += 0.02
                
        elif action.action_type == "finish":
            done = True
            info["msg"] = "Task finished."
            if len(self.action_history) > 6:
                reward -= 0.2
        else:
            info["msg"] = "Invalid action."
            reward -= 0.1

        if self.current_step >= self.max_steps:
             done = True

        reward += 0.01 * (self.max_steps - self.current_step)

        return self._get_observation(), round(reward, 2), done, info
