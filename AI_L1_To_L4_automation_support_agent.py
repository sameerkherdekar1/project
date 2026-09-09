AI_CONFIG = {
    "AI_L1_TIMEOUT_MINS": 2,
    "AI_L2_TIMEOUT_MINS": 10,
    "AI_L3_TIMEOUT_MINS": 30,
    "AI_L4_TIMEOUT_MINS": 60,
    "AI_REPEAT_LIMIT": 3,
    "AI_HARASSMENT_PROTECTION_ENABLED": True,
    "AI_COMPANY": "Portfolio - Compatible with Microsoft Tech"
}

AI_Ticket_History = {}
AI_KB_Database_Global = {
    "Outlook not opening": "Restart Outlook, Repair Office via Company Portal",
    "Desktop App Installation Failed": "Check Intune Logs: C:\\ProgramData\\Microsoft\\IntuneManagementExtension\\Logs",
    "Intune Policy Not Received": "Force Sync: Get-ScheduledTask -TaskName PushLaunch | Start-ScheduledTask",
    "Software Install": "Push via Intune Company Portal",
    "VPN Issue": "Reset VPN, Client"
}

class AI_L1_Agent:
    def AI_Solve(self, ticket):
        print(f"[AI_L1_Agent] Processing: {ticket['issue']}")
        if ticket['issue'] in AI_KB_Database_Global:
            return {"status": "success", "solution": AI_KB_Database_Global[ticket['issue']], "solved_by": "AI_L1_Agent"}
        return {"status": "fail", "logs": "L1 logs"}

class AI_L2_Agent:
    def AI_Solve(self, ticket):
        print(f"[AI_L2_Agent] Investigating: {ticket['issue']}")
        return {"status": "success", "solution": "Fixed by L2 - Force Intune Sync & Policy Re-push", "solved_by": "AI_L2_Agent"}

class AI_L3_Agent:
    def AI_Solve(self, ticket):
        print(f"[AI_L3_Agent] RCA for: {ticket['issue']}")
        ps_script = f"""
        # PowerShell for {ticket['id']}
        $AppPath = "\\\\fileserver\\apps\\CustomApp\\setup.msi"
        Start-Process msiexec.exe -ArgumentList "/i $AppPath /qn /log C:\\Temp\\AI_Install.log" -Wait
        if(Test-Path "C:\\Program Files\\CustomApp\\app.exe"){{ exit 0 }} else {{ exit 1 }}
        """
        AI_KB_Database_Global[ticket['issue']] = "Permanent Fix by AI_L3"
        return {"status": "success", "solution": "Permanent Fix Applied", "script": ps_script, "solved_by": "AI_L3_Agent"}

class AI_L4_Agent:
    def AI_Solve(self, ticket):
        return {"status": "escalated", "solution": "Vendor Escalation Report Sent to Microsoft", "solved_by": "AI_L4_Agent"}

class AI_Manual_Butler:
    def AI_Handle(self, ticket):
        print(f"[AI_Manual_Butler] Human Assigned for {ticket['user_id']} - Repeat {ticket['repeat_count']}")
        return {"status": "assigned_to_human", "solution": "Human Engineer will call", "solved_by": "AI_Manual_Butler"}

class AI_PM_Agent:
    def AI_Monitor(self, ticket, result):
        print(f"[AI_PM_Agent] Ticket {ticket['id']} Solved by {result['solved_by']}")

class AI_Orchestrator:
    def _init_(self):
        self.AI_L1 = AI_L1_Agent()
        self.AI_L2 = AI_L2_Agent()
        self.AI_L3 = AI_L3_Agent()
        self.AI_L4 = AI_L4_Agent()
        self.AI_PM = AI_PM_Agent()
        self.AI_Butler = AI_Manual_Butler()

    def AI_Process_Ticket(self, ticket):
        user = ticket['user_id']
        AI_Ticket_History[user] = AI_Ticket_History.get(user, 0) + 1
        ticket['repeat_count'] = AI_Ticket_History[user]
        if AI_CONFIG["AI_HARASSMENT_PROTECTION_ENABLED"] and ticket['repeat_count'] >= AI_CONFIG["AI_REPEAT_LIMIT"]:
            result = self.AI_Butler.AI_Handle(ticket)
            self.AI_PM.AI_Monitor(ticket, result)
            return result
        result = self.AI_L1.AI_Solve(ticket)
        if result['status'] == 'success':
            self.AI_PM.AI_Monitor(ticket, result)
            return result
        result = self.AI_L2.AI_Solve(ticket)
        if result['status'] == 'success':
            self.AI_PM.AI_Monitor(ticket, result)
            return result
        result = self.AI_L3.AI_Solve(ticket)
        if result['status'] == 'success':
            self.AI_PM.AI_Monitor(ticket, result)
            return result
        result = self.AI_L4.AI_Solve(ticket)
        self.AI_PM.AI_Monitor(ticket, result)
        return result

if __name__ == "_main_":
    print("=== AI_L1toL4Automation_Support_Agent Started ===")
    AI_System = AI_Orchestrator()
    tests = [
        {"id": "INC001", "user_id": "user1@company.com", "issue": "Outlook not opening"},
        {"id": "INC002", "user_id": "user2@company.com", "issue": "Desktop App Installation Failed"},
    ]
    for t in tests:
        print(f"\n--- Processing {t['id']} ---")
        print(AI_System.AI_Process_Ticket(t))
    print("\n=== System Ready for GitHub & Interview ===")

