# Aetheris - Enterprise Autonomous Operations Control Center
import streamlit as st
import pandas as pd
import time

# Set wide layout and page config
st.set_page_config(
    page_title="Aetheris - Enterprise Agentic Operations",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for premium dark-theme look, typography, and card grids
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    /* Global Background and Fonts */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #030712 !important;
        font-family: 'Outfit', sans-serif !important;
        color: #f3f4f6 !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #090d1f !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* Header and Subtitles */
    .op-header {
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    .accent-cyan {
        color: #06b6d4;
        text-shadow: 0 0 10px rgba(6, 182, 212, 0.2);
    }
    
    /* Premium Dashboard Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.45);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1.25rem;
    }
    
    /* Visual Agent Status Cards Grid */
    .agent-status-container {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-gap: 12px;
        margin-top: 10px;
    }
    .agent-card {
        background: rgba(30, 41, 59, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.04);
        border-radius: 12px;
        padding: 1rem;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .agent-card.active {
        background: rgba(6, 182, 212, 0.05);
        border-color: #06b6d4;
        box-shadow: 0 0 15px rgba(6, 182, 212, 0.25);
    }
    .agent-card-title {
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #e5e7eb;
    }
    .agent-card.active .agent-card-title {
        color: #06b6d4;
    }
    .agent-card-status {
        font-size: 0.75rem;
        color: #6b7280;
        margin-top: 6px;
        font-family: 'JetBrains Mono', monospace;
    }
    .agent-card.active .agent-card-status {
        color: #22d3ee;
        font-weight: 600;
        animation: pulse-text 2s infinite;
    }
    .agent-card.pending .agent-card-status {
        color: #f59e0b;
        font-weight: 600;
    }
    .agent-card.pending {
        border-color: #f59e0b;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
    }
    
    /* Custom Console Design */
    .console-terminal {
        background: #010413;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        line-height: 1.5;
        height: 220px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 5px;
    }
    .console-row {
        color: #9ca3af;
    }
    .console-row.highlight { color: #06b6d4; }
    .console-row.success { color: #10b981; }
    .console-row.warning { color: #f59e0b; }
    .console-row.danger { color: #ef4444; }
    
    /* Animations */
    @keyframes pulse-text {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# DATABASE INITIALIZATION
# ----------------------------------------------------
if "db" not in st.session_state:
    st.session_state.db = {
        "it": {
            "identity": [
                { "User": "Alex Rivera", "Role": "Sales Executive", "Apps": "Salesforce, Slack" },
                { "User": "Marcus Chen", "Role": "Frontend Engineer", "Apps": "GitHub, Figma, Slack" },
                { "User": "Sophia Patel", "Role": "HR Generalist", "Apps": "Workday, Slack" }
            ],
            "inventory": [
                { "Asset": "Laptops", "Stock Count": 12, "Status": "In Stock" },
                { "Asset": "Monitors", "Stock Count": 5, "Status": "Low Stock" },
                { "Asset": "Keyboards", "Stock Count": 8, "Status": "In Stock" },
                { "Asset": "Headsets", "Stock Count": 15, "Status": "In Stock" }
            ],
            "tickets": [
                { "Ticket ID": "INC-301", "Summary": "Reset Okta MFA", "Stage": "Support", "Status": "Resolved" },
                { "Ticket ID": "INC-302", "Summary": "Requesting Slack access", "Stage": "Identity", "Status": "Resolved" }
            ]
        },
        "hr": {
            "profiles": [
                { "Employee": "Marcus Chen", "Onboarding Stage": "Onboarded", "Forms": "4/4 Complete" },
                { "Employee": "Sophia Patel", "Onboarding Stage": "Onboarded", "Forms": "4/4 Complete" }
            ],
            "compliance": [
                { "Document": "I-9 Verification", "Verified Type": "US Passport", "Status": "Verified" },
                { "Document": "Direct Deposit Setup", "Verified Type": "ACH Form", "Status": "Verified" }
            ]
        },
        "finance": {
            "ap": [
                { "Invoice ID": "INV-9020", "Vendor": "Slack Technologies", "Amount": "$8,450.00", "Status": "Paid" },
                { "Invoice ID": "INV-9021", "Vendor": "Globex Hosting", "Amount": "$3,120.00", "Status": "Pending" }
            ],
            "audit": [
                { "PO Ref": "PO-7001", "Bank Details": "Silicon Valley Bank ****9021", "Anomaly Score": 0.02 },
                { "PO Ref": "PO-7002", "Bank Details": "JPMorgan Chase ****4423", "Anomaly Score": 0.05 }
            ]
        },
        "legal": {
            "playbook": [
                { "Clause Category": "Governing Law", "Approved Requirement": "New York or Delaware Only", "Risk Level": "Low" },
                { "Clause Category": "Non-Solicitation", "Approved Requirement": "Minimum 24 Months duration", "Risk Level": "Medium" },
                { "Clause Category": "Indemnification", "Approved Requirement": "Capped at 1x contract value", "Risk Level": "High" }
            ],
            "vault": [
                { "Contract ID": "CTR-401", "Counterparty": "Stark Industries", "Status": "Compliant", "Deviations": "None" },
                { "Contract ID": "CTR-402", "Counterparty": "Oscorp Corp", "Status": "Under Review", "Deviations": "Jurisdiction: NJ" }
            ]
        },
        "sales": {
            "crm": [
                { "Contact": "Sarah Jenkins", "Company": "SecureNet LLC", "Intent Score": 45, "Assigned Rep": "David Kim" },
                { "Contact": "Richard Hendricks", "Company": "Pied Piper", "Intent Score": 92, "Assigned Rep": "Jared Dunn" }
            ],
            "outbox": [
                { "To": "richard@piedpiper.com", "Subject": "Compression Scaling Support at Pied Piper" }
            ]
        },
        "procurement": {
            "suppliers": [
                { "Vendor": "Cloudflare CDN", "Services": "Edge Routing & Security", "SOC2": "Verified", "ESG Rating": "AA" },
                { "Vendor": "AWS Cloud", "Services": "Elastic Infrastructure & S3", "SOC2": "Verified", "ESG Rating": "A" }
            ],
            "rfp": [
                { "Vendor": "Fastly Edge", "Latency": "21ms", "Quote / GB": "$0.008", "Status": "Compliant" }
            ]
        }
    }

if "active_dept" not in st.session_state:
    st.session_state.active_dept = "it"

if "logs" not in st.session_state:
    st.session_state.logs = []


if "chat_history" not in st.session_state:
    st.session_state.chat_history = {
        "it": [{"role": "assistant", "text": "Hello! I am the IT Agentic Coordinator. Select a scenario or enter a custom request."}],
        "hr": [{"role": "assistant", "text": "Welcome! I manage onboarding flows and handbook policy queries. Select a scenario or ask a question."}],
        "finance": [{"role": "assistant", "text": "Awaiting invoice submission. I can perform 3-way matching and flag payment anomalies."}],
        "legal": [{"role": "assistant", "text": "Awaiting contract submission. I will parse it against the legal playbook."}],
        "sales": [{"role": "assistant", "text": "Submit a prospect profile. I will scrape public signals and score buying intent."}],
        "procurement": [{"role": "assistant", "text": "Provide CDN or sourcing requisitions. I will coordinate RFP bids and verify SOC2 compliance."}]
    }

if "active_agent" not in st.session_state:
    st.session_state.active_agent = "none"

if "ticket_counter" not in st.session_state:
    st.session_state.ticket_counter = 303
if "contract_counter" not in st.session_state:
    st.session_state.contract_counter = 403

if "approval_pending" not in st.session_state:
    st.session_state.approval_pending = {"active": False, "ticket_id": "", "metadata": {}}

if "outbox_emails" not in st.session_state:
    st.session_state.outbox_emails = []

# Configurations mapping
dept_configs = {
    "it": {
        "title": "IT Support Operations",
        "desc": "Zero-touch client workspace provisioning, credentials deployment, and telemetry client diagnostics.",
        "nodes": {
            "coord": {"label": "IT Coordinator", "icon": "🤖"},
            "left": {"label": "Identity Agent", "icon": "🔑"},
            "right": {"label": "Asset Manager", "icon": "📦"},
            "bottom": {"label": "Diagnostician", "icon": "🔧", "visible": True}
        }
    },
    "hr": {
        "title": "HR Onboarding & Advisory",
        "desc": "Onboarding document compliance checks, Workday profiles setup, and benefits policy RAG.",
        "nodes": {
            "coord": {"label": "Onboarding Coord", "icon": "👥"},
            "left": {"label": "Benefits Advisor", "icon": "📚"},
            "right": {"label": "Compliance Officer", "icon": "📑"},
            "bottom": {"label": "IT Setup Agent", "icon": "🤖", "visible": True}
        }
    },
    "finance": {
        "title": "Finance & Accounts Payable",
        "desc": "Invoice OCR parsing, 3-way PO reference validation matching, and fraud check alarms.",
        "nodes": {
            "coord": {"label": "Audit Coordinator", "icon": "💰"},
            "left": {"label": "Invoice Parser", "icon": "📑"},
            "right": {"label": "Treasury Agent", "icon": "🏦"},
            "bottom": {"label": "Supplier Agent", "icon": "✉️", "visible": True}
        }
    },
    "legal": {
        "title": "Legal Contract Intelligence",
        "desc": "Agreement clause scanning, playbook standard audits, and redlining markups.",
        "nodes": {
            "coord": {"label": "Contract Parser", "icon": "⚖️"},
            "left": {"label": "Playbook Auditor", "icon": "📘"},
            "right": {"label": "Risk Assessor", "icon": "⚡"},
            "bottom": {"label": "", "icon": "", "visible": False}
        }
    },
    "sales": {
        "title": "Sales & Marketing Growth Loop",
        "desc": "Lead signal enrichment crawling, CRM registry intent scoring, and outreach writing.",
        "nodes": {
            "coord": {"label": "Intent Scorer", "icon": "🎯"},
            "left": {"label": "Lead Enricher", "icon": "🔍"},
            "right": {"label": "Email Generator", "icon": "✍️"},
            "bottom": {"label": "", "icon": "", "visible": False}
        }
    },
    "procurement": {
        "title": "Smart Sourcing & Procurement",
        "desc": "Supplier discovery, RFP latency and quotation comparison, and SOC2 certification audits.",
        "nodes": {
            "coord": {"label": "RFP Coordinator", "icon": "🛒"},
            "left": {"label": "Sourcing Agent", "icon": "🌍"},
            "right": {"label": "Compliance Auditor", "icon": "🛡️"},
            "bottom": {"label": "Negotiator", "icon": "🤝", "visible": True}
        }
    }
}

# ----------------------------------------------------
# VISUAL RENDERING (DYNAMIC CARDS & LOGS)
# ----------------------------------------------------
def draw_agent_cards(active_agent):
    config = dept_configs[st.session_state.active_dept]["nodes"]
    
    def get_card_class(node_key):
        if active_agent == node_key:
            return "active"
        if node_key == "left" and st.session_state.approval_pending["active"] and st.session_state.approval_pending["metadata"]["agent"] == "Identity Agent":
            return "pending"
        return ""
        
    def get_status_label(node_key, label_idle):
        if active_agent == node_key:
            return "ACTIVE"
        if node_key == "left" and st.session_state.approval_pending["active"] and st.session_state.approval_pending["metadata"]["agent"] == "Identity Agent":
            return "AWAITING APPROVAL"
        return label_idle

    bottom_html = ""
    if config["bottom"]["visible"]:
        bottom_html = (
            f'<div class="agent-card {get_card_class("bottom")}">'
            f'<div class="agent-card-title">{config["bottom"]["icon"]} {config["bottom"]["label"]}</div>'
            f'<div class="agent-card-status">{get_status_label("bottom", "IDLE")}</div>'
            f'</div>'
        )

    cards_html = (
        f'<div class="agent-status-container">'
        f'<div class="agent-card {get_card_class("coord")}">'
        f'<div class="agent-card-title">{config["coord"]["icon"]} {config["coord"]["label"]}</div>'
        f'<div class="agent-card-status">{get_status_label("coord", "IDLE")}</div>'
        f'</div>'
        f'<div class="agent-card {get_card_class("left")}">'
        f'<div class="agent-card-title">{config["left"]["icon"]} {config["left"]["label"]}</div>'
        f'<div class="agent-card-status">{get_status_label("left", "IDLE")}</div>'
        f'</div>'
        f'<div class="agent-card {get_card_class("right")}">'
        f'<div class="agent-card-title">{config["right"]["icon"]} {config["right"]["label"]}</div>'
        f'<div class="agent-card-status">{get_status_label("right", "IDLE")}</div>'
        f'</div>'
        f'{bottom_html}'
        f'</div>'
    )
    return cards_html


def draw_console_terminal():
    terminal_rows = ""
    for log in st.session_state.logs:
        # Determine CSS row color class based on log keywords
        row_class = "console-row"
        text_lower = log.lower()
        if "[fail]" in text_lower or "error" in text_lower or "declined" in text_lower or "discrepancy" in text_lower:
            row_class += " danger"
        elif "[success]" in text_lower or "verified" in text_lower or "approved" in text_lower:
            row_class += " success"
        elif "warning" in text_lower or "requires" in text_lower:
            row_class += " warning"
        elif "ingested" in text_lower or "closed" in text_lower:
            row_class += " highlight"
            
        terminal_rows += f'<div class="{row_class}">&gt; {log}</div>'
        
    if not terminal_rows:
        terminal_rows = '<div class="console-row" style="color: #4b5563;">&gt; System waiting. Select a scenario to start operations...</div>'
        
    terminal_html = f'<div class="console-terminal">{terminal_rows}</div>'
    return terminal_html

# ----------------------------------------------------
# VIEW PLACEMENT FUNCTION (DYNAMIC RENDER)
# ----------------------------------------------------
def update_topology_view(placeholder):
    with placeholder.container():
        st.write("### Agent Status Center")
        st.markdown(draw_agent_cards(st.session_state.active_agent), unsafe_allow_html=True)

def update_terminal_view(placeholder):
    with placeholder.container():
        st.write("### Agent Live Trace Logs")
        st.markdown(draw_console_terminal(), unsafe_allow_html=True)

# ----------------------------------------------------
# AGENT WORKFLOW ENGINE (LOOP)
# ----------------------------------------------------
def execute_agent_pipeline(steps, db_updates=None, final_bot_msg=None, approval_meta=None):
    st.session_state.logs = []
    
    for step in steps:
        agent = step["agent"].lower()
        
        # Highlight active agent
        if "coordinator" in agent or "support" in agent or "audit" in agent or "parser" in agent and not "invoice" in agent or "scorer" in agent or "rfp" in agent:
            st.session_state.active_agent = "coord"
        elif "identity" in agent or "advisor" in agent or "enricher" in agent or "sourcing" in agent or "playbook" in agent:
            st.session_state.active_agent = "left"
        elif "asset" in agent or "compliance" in agent or "treasury" in agent or "assessor" in agent or "email" in agent:
            st.session_state.active_agent = "right"
        elif "diagnostician" in agent or "supplier" in agent or "negotiator" in agent or "it setup" in agent:
            st.session_state.active_agent = "bottom"
            
        # Add log statement
        st.session_state.logs.append(f"[{step['agent']}] {step['message']}")
        
        # Rerender UI panels instantly
        update_topology_view(topo_placeholder)
        update_terminal_view(term_placeholder)
        time.sleep(1.1)
        
    # Reset active status
    st.session_state.active_agent = "none"
    
    # Save database updates
    if db_updates:
        for k, v in db_updates.items():
            st.session_state.db[k] = v
            
    # Trigger gate or append final bot response
    if approval_meta:
        st.session_state.approval_pending = {
            "active": True,
            "ticket_id": approval_meta["ticket_id"],
            "metadata": approval_meta
        }
    elif final_bot_msg:
        st.session_state.chat_history[st.session_state.active_dept].append({"role": "assistant", "text": final_bot_msg})
        
    # Single clean rerun to update tables and states globally
    st.rerun()

# ----------------------------------------------------
# SCENARIOS IMPLEMENTATIONS
# ----------------------------------------------------
def run_it_scenario_1():
    t_id = f"INC-{st.session_state.ticket_counter}"
    st.session_state.ticket_counter += 1
    
    it_db = st.session_state.db["it"]
    it_db["tickets"].insert(0, { "Ticket ID": t_id, "Summary": "Request Salesforce + Monitor Replacement", "Stage": "Triage", "Status": "Processing" })
    
    steps = [
        { "agent": "IT Coordinator", "message": f"Ingested request {t_id}. Parsing natural language parameters...", "type": "system" },
        { "agent": "IT Coordinator", "message": "Parsed intent: Software (Salesforce) & Hardware (Monitor). Dispatching sub-threads.", "type": "system" },
        { "agent": "Identity Agent", "message": "Checking Okta role policies for Alex Rivera...", "type": "agent" },
        { "agent": "Identity Agent", "message": "User belongs to Sales. Pre-approved for Salesforce. Calling Okta API...", "type": "success" }
    ]
    
    for u in it_db["identity"]:
        if u["User"] == "Alex Rivera" and "Salesforce" not in u["Apps"]:
            u["Apps"] += ", Salesforce"
            
    steps.extend([
        { "agent": "Asset Manager", "message": "Querying hardware storage list for Monitor stock...", "type": "agent" },
        { "agent": "Asset Manager", "message": "Monitor located. Reserving unit and adjusting stock level...", "type": "success" },
        { "agent": "Asset Manager", "message": "Locker pickup code generated: QR-AETH-902.", "type": "success" },
        { "agent": "IT Coordinator", "message": f"All sub-agent runs verified. Resolving ticket {t_id}.", "type": "system" }
    ])
    
    for item in it_db["inventory"]:
        if item["Asset"] == "Monitors":
            item["Stock Count"] -= 1
            
    it_db["tickets"][0]["Stage"] = "Support"
    it_db["tickets"][0]["Status"] = "Resolved"
    
    execute_agent_pipeline(steps, {"it": it_db}, f"Ticket {t_id} resolved! Salesforce provisioned. Retrieve your monitor from Locker #3 with code QR-AETH-902.")

def run_it_scenario_2():
    t_id = f"INC-{st.session_state.ticket_counter}"
    st.session_state.ticket_counter += 1
    
    it_db = st.session_state.db["it"]
    it_db["tickets"].insert(0, { "Ticket ID": t_id, "Summary": "VPN connection failing", "Stage": "Triage", "Status": "Processing" })
    
    steps = [
        { "agent": "IT Coordinator", "message": f"Ingested request {t_id}. Routing to Diagnostician.", "type": "system" },
        { "agent": "Diagnostician", "message": "Opening remote telemetry session to client device AETH-882...", "type": "agent" },
        { "agent": "Diagnostician", "message": "Testing handshake logs: [FAIL] Certificate handshake mismatch.", "type": "danger" },
        { "agent": "Diagnostician", "message": "Checking software version: VPN client is outdated (v4.2.1). Upgrade required.", "type": "warning" },
        { "agent": "Diagnostician", "message": "Pushing installation package v4.3.0 via background MDM installer...", "type": "tool" },
        { "agent": "Diagnostician", "message": "Upgrade completed. Flushing DNS cache and renewing routes...", "type": "tool" },
        { "agent": "Diagnostician", "message": "Rerunning handshake check: [SUCCESS] Secure connection established.", "type": "success" },
        { "agent": "IT Coordinator", "message": f"Connection verified. Resolving ticket {t_id}.", "type": "system" }
    ]
    
    it_db["tickets"][0]["Stage"] = "Diagnostics"
    it_db["tickets"][0]["Status"] = "Resolved"
    
    execute_agent_pipeline(steps, {"it": it_db}, f"Diagnostics completed on ticket {t_id}. We upgraded your VPN client to v4.3.0 and flushed local DNS routes. Handshake restored.")

def run_it_scenario_3():
    t_id = f"INC-{st.session_state.ticket_counter}"
    st.session_state.ticket_counter += 1
    
    it_db = st.session_state.db["it"]
    it_db["tickets"].insert(0, { "Ticket ID": t_id, "Summary": "Request Figma Access", "Stage": "Triage", "Status": "Processing" })
    
    steps = [
        { "agent": "IT Coordinator", "message": f"Access request {t_id} received. Forwarding to Identity Agent.", "type": "system" },
        { "agent": "Identity Agent", "message": "Auditing role parameters for Alex Rivera (Sales)...", "type": "agent" },
        { "agent": "Identity Agent", "message": "Figma access is restricted. Triggering override manager authorization gate...", "type": "warning" }
    ]
    
    execute_agent_pipeline(steps, {"it": it_db}, approval_meta={
        "ticket_id": t_id,
        "agent": "Identity Agent",
        "action": "Restricted Access override: Figma",
        "user": "Alex Rivera"
    })

def run_hr_scenario_1():
    hr_db = st.session_state.db["hr"]
    it_db = st.session_state.db["it"]
    
    steps = [
        { "agent": "Onboarding Coordinator", "message": "HR Trigger: Clara Vance signed contract agreement.", "type": "system" },
        { "agent": "Compliance Officer", "message": "Scanning and parsing uploaded identity document (Passport scan)...", "type": "agent" },
        { "agent": "Compliance Officer", "message": "Passport authenticated. Compliance checks passed. I-9 form: VERIFIED.", "type": "success" }
    ]
    
    hr_db["profiles"].append({ "Employee": "Clara Vance", "Onboarding Stage": "Ready", "Forms": "4/4 Complete" })
    hr_db["compliance"].insert(0, { "Document": "I-9 Form - C. Vance", "Verified Type": "US Passport", "Status": "Verified" })
    it_db["identity"].append({ "User": "Clara Vance", "Role": "Software Engineer", "Apps": "GitHub, Slack" })
    
    steps.extend([
        { "agent": "IT Setup Agent", "message": "Cross-department trigger: Provisioning corporate account and ordering developer machine...", "type": "tool" },
        { "agent": "IT Setup Agent", "message": "Okta credentials created. Laptop dispatched.", "type": "success" },
        { "agent": "Onboarding Coordinator", "message": "Generating welcome guides and orientation calendar slots.", "type": "system" }
    ])
    
    execute_agent_pipeline(steps, {"hr": hr_db, "it": it_db}, "Onboarding setup completed for Clara Vance. Document compliance checks verified, corporate accounts activated, and welcome guides sent.")

def run_hr_scenario_2():
    steps = [
        { "agent": "Onboarding Coordinator", "message": "Inquiry: 'Is acupuncture covered under my plan?'", "type": "system" },
        { "agent": "Benefits Advisor", "message": "Querying handbook embedding vector database using semantic matching...", "type": "tool" },
        { "agent": "Benefits Advisor", "message": "Match located: Section 7.2 (Alternative Care Benefits).", "type": "success" }
    ]
    execute_agent_pipeline(steps, None, "Based on the Benefits handbook (Section 7.2), acupuncture is covered under Choice B. You are allowed up to 12 sessions per calendar year with a flat $20 copay per session.")

def run_finance_scenario_1():
    fin_db = st.session_state.db["finance"]
    fin_db["ap"].insert(0, { "Invoice ID": "INV-9022", "Vendor": "ACME Corp", "Amount": "$15,200.00", "Status": "Pending" })
    
    steps = [
        { "agent": "Audit Coordinator", "message": "Ingested Invoice INV-9022. Routing to OCR parser...", "type": "system" },
        { "agent": "Invoice Parser", "message": "Extracting line items, totals, and bank credentials...", "type": "agent" },
        { "agent": "Invoice Parser", "message": "OCR extract: Total $15,200.00. Reference PO: PO-7003.", "type": "success" },
        { "agent": "Audit Coordinator", "message": "Performing 3-Way Match (Invoice total vs PO-7003 vs Goods Receipt)...", "type": "tool" },
        { "agent": "Audit Coordinator", "message": "Match verified. Pricing terms match PO. Laptop delivery confirmed.", "type": "success" },
        { "agent": "Treasury Agent", "message": "Posting transaction to ledger. Scheduling Net-30 payout date...", "type": "agent" }
    ]
    
    fin_db["ap"][0]["Status"] = "Paid"
    fin_db["audit"].insert(0, { "PO Ref": "PO-7003", "Bank Details": "Wells Fargo Bank ****2210", "Anomaly Score": 0.01 })
    
    execute_agent_pipeline(steps, {"finance": fin_db}, "Invoice INV-9022 audited successfully! 3-way match verified. Net-30 payment scheduled.")

def run_finance_scenario_2():
    fin_db = st.session_state.db["finance"]
    fin_db["ap"].insert(0, { "Invoice ID": "INV-9023", "Vendor": "ACME Corp", "Amount": "$15,200.00", "Status": "Pending" })
    
    steps = [
        { "agent": "Audit Coordinator", "message": "Ingested Invoice INV-9023. Routing to parser...", "type": "system" },
        { "agent": "Invoice Parser", "message": "OCR scan: Bank routing details updated to Chase ****9044 (Historic: Wells Fargo).", "type": "warning" },
        { "agent": "Audit Coordinator", "message": "Discrepancy check: Bank details mismatch. High anomaly risk scored (0.98).", "type": "danger" },
        { "agent": "Supplier Agent", "message": "Creating dispute ticket. Email notification drafted requesting verification callback...", "type": "tool" }
    ]
    
    fin_db["ap"][0]["Status"] = "Disputed"
    fin_db["audit"].insert(0, { "PO Ref": "PO-7003", "Bank Details": "Chase Bank ****9044 (UNMATCHED)", "Anomaly Score": 0.98 })
    
    execute_agent_pipeline(steps, {"finance": fin_db}, "⚠️ WARNING: Invoice INV-9023 flagged for fraud audit. Bank routing details do not match vendor registry. Dispute notice sent.")

def run_legal_scenario_1():
    c_id = f"CTR-{st.session_state.contract_counter}"
    st.session_state.contract_counter += 1
    
    leg_db = st.session_state.db["legal"]
    leg_db["vault"].insert(0, { "Contract ID": c_id, "Counterparty": "Initech Corp", "Status": "Under Review", "Deviations": "Audit pending" })
    
    steps = [
        { "agent": "Contract Parser", "message": f"Scanning Contract {c_id} (Mutual NDA - Initech)...", "type": "system" },
        { "agent": "Playbook Auditor", "message": "Matching clauses against corporate standard playbook criteria...", "type": "agent" },
        { "agent": "Playbook Auditor", "message": "Deviation: Governing Law is California (Playbook requires NY/DE). Risk: Low.", "type": "warning" },
        { "agent": "Playbook Auditor", "message": "Deviation: Non-Solicitation is set to 12 months (Playbook minimum: 24). Risk: Medium.", "type": "warning" },
        { "agent": "Risk Assessor", "message": "Reverting Non-Solicitation to 24 months. Drafting redline comments...", "type": "tool" }
    ]
    
    leg_db["vault"][0]["Deviations"] = "Non-Solicit, Jurisdiction"
    
    execute_agent_pipeline(steps, {"legal": leg_db}, f"Audited NDA {c_id} with Initech! Playbook deviations resolved. Redlines drafted and saved for council signature.")

def run_sales_scenario_1():
    sales_db = st.session_state.db["sales"]
    
    steps = [
        { "agent": "Intent Scorer", "message": "Ingested profile: David Sacks (VP Cloud Strategy at Craft Ventures).", "type": "system" },
        { "agent": "Lead Enricher", "message": "Querying Crunchbase, LinkedIn, and public news feeds...", "type": "agent" },
        { "agent": "Lead Enricher", "message": "Signal: Craft Ventures backed multi-cloud. Hiring 5 DevOps engineers.", "type": "success" },
        { "agent": "Intent Scorer", "message": "Buying intent score: 95 (High). Saving lead in CRM...", "type": "success" }
    ]
    
    sales_db["crm"].insert(0, { "Contact": "David Sacks", "Company": "Craft Ventures", "Intent Score": 95, "Assigned Rep": "Jared Dunn" })
    
    steps.extend([
        { "agent": "Email Generator", "message": "Drafting context-relevant outbound email templates based on multi-cloud signals...", "type": "tool" },
        { "agent": "Email Generator", "message": "Email draft completed and queued in outbox.", "type": "success" }
    ])
    
    sales_db["outbox"].insert(0, { "To": "sacks@craftventures.com", "Subject": "Optimizing Craft Ventures Multi-Cloud Operations" })
    
    email_body = "Hi David,\n\nI noticed Craft Ventures is scaling its multi-cloud initiative. Our dashboard can help you automate compliance audits and cut configuration MTTR. Let's schedule a call.\n\nBest,\nJared Dunn"
    st.session_state.outbox_emails.insert(0, {"to": "sacks@craftventures.com", "subject": "Optimizing Craft Ventures Multi-Cloud Operations", "body": email_body})
    
    execute_agent_pipeline(steps, {"sales": sales_db}, "Enriched lead David Sacks! CRM profile created with intent score 95. Outbox draft generated.")

def run_procurement_scenario_1():
    proc_db = st.session_state.db["procurement"]
    proc_db["rfp"].insert(0, { "Vendor": "Cloudflare Edge", "Latency": "18ms", "Quote / GB": "$0.009", "Status": "Compliant" })
    proc_db["rfp"].insert(0, { "Vendor": "Akamai", "Latency": "25ms", "Quote / GB": "$0.006", "Status": "Pending" })
    
    steps = [
        { "agent": "RFP Coordinator", "message": "Ingested edge CDN sourcing requisition request.", "type": "system" },
        { "agent": "Sourcing Agent", "message": "Dispatched RFP requests and collecting vendor responses...", "type": "agent" },
        { "agent": "Compliance Auditor", "message": "Verifying security and ESG metrics for bids...", "type": "agent" },
        { "agent": "Compliance Auditor", "message": "Cloudflare CDN has valid SOC 2 compliance. ESG: AA.", "type": "success" },
        { "agent": "Compliance Auditor", "message": "Akamai has expired security certification. Flagging NON-COMPLIANT bid.", "type": "danger" }
    ]
    
    proc_db["rfp"][0]["Status"] = "Non-Compliant"
    
    steps.extend([
        { "agent": "Negotiator", "message": "Drafting discount strategy for Cloudflare based on a 24-month contract.", "type": "tool" }
    ])
    
    execute_agent_pipeline(steps, {"procurement": proc_db}, "CDN sourcing RFP audited! Cloudflare selected as compliant supplier; Akamai bid rejected due to expired SOC2.")

# Resolve approval decision callback
def resolve_override_decision(approved):
    meta = st.session_state.approval_pending["metadata"]
    st.session_state.approval_pending = {"active": False, "ticket_id": "", "metadata": {}}
    
    it_db = st.session_state.db["it"]
    
    if approved:
        steps = [
            { "agent": "Identity Agent", "message": "Manager approved Figma access override request.", "type": "success" },
            { "agent": "Identity Agent", "message": "Adding license. Registering Okta application...", "type": "tool" },
            { "agent": "Identity Agent", "message": "Provisioning complete. Access is active.", "type": "success" }
        ]
        for u in it_db["identity"]:
            if u["User"] == "Alex Rivera" and "Figma" not in u["Apps"]:
                u["Apps"] += ", Figma"
        it_db["tickets"][0]["Status"] = "Resolved"
        bot_msg = "Great news! Your request for Figma has been approved and access is now active."
    else:
        steps = [
            { "agent": "Identity Agent", "message": "Manager declined Figma access override request.", "type": "danger" },
            { "agent": "Identity Agent", "message": "Cancelling provisioning. Ticket closed as declined.", "type": "system" }
        ]
        it_db["tickets"][0]["Status"] = "Rejected"
        bot_msg = "Your Figma access override request was declined by your manager."
        
    it_db["tickets"][0]["Stage"] = "Identity"
    execute_agent_pipeline(steps, {"it": it_db}, bot_msg)

# ----------------------------------------------------
# DATABASE REGISTRY RENDERER
# ----------------------------------------------------
def update_db_view(placeholder):
    with placeholder.container():
        dept = st.session_state.active_dept
        
        # Render using st.data_editor so fields are resizable and editable
        if dept == "it":
            st.markdown("### 🔑 Identity Registry (Okta)")
            st.session_state.db["it"]["identity"] = st.data_editor(
                st.session_state.db["it"]["identity"],
                use_container_width=True,
                num_rows="dynamic",
                key="it_ident_editor"
            )
            
            st.markdown("### 📦 Hardware Inventory")
            st.session_state.db["it"]["inventory"] = st.data_editor(
                st.session_state.db["it"]["inventory"],
                use_container_width=True,
                num_rows="dynamic",
                key="it_inv_editor"
            )
            
            st.markdown("### 📋 ServiceNow Tickets")
            st.session_state.db["it"]["tickets"] = st.data_editor(
                st.session_state.db["it"]["tickets"],
                use_container_width=True,
                num_rows="dynamic",
                key="it_ticket_editor"
            )
            
        elif dept == "hr":
            st.markdown("### 👥 Workday Employee Profiles")
            st.session_state.db["hr"]["profiles"] = st.data_editor(
                st.session_state.db["hr"]["profiles"],
                use_container_width=True,
                num_rows="dynamic",
                key="hr_prof_editor"
            )
            
            st.markdown("### 📑 Compliance Document Vault")
            st.session_state.db["hr"]["compliance"] = st.data_editor(
                st.session_state.db["hr"]["compliance"],
                use_container_width=True,
                num_rows="dynamic",
                key="hr_comp_editor"
            )
            
        elif dept == "finance":
            st.markdown("### 💰 Accounts Payable Ledger")
            st.session_state.db["finance"]["ap"] = st.data_editor(
                st.session_state.db["finance"]["ap"],
                use_container_width=True,
                num_rows="dynamic",
                key="fin_ap_editor"
            )
            
            st.markdown("### ⚙️ 3-Way Match Verification")
            st.session_state.db["finance"]["audit"] = st.data_editor(
                st.session_state.db["finance"]["audit"],
                use_container_width=True,
                num_rows="dynamic",
                key="fin_aud_editor"
            )
            
        elif dept == "legal":
            st.markdown("### ⚖️ Legal Playbook Standard")
            st.session_state.db["legal"]["playbook"] = st.data_editor(
                st.session_state.db["legal"]["playbook"],
                use_container_width=True,
                num_rows="dynamic",
                key="leg_pb_editor"
            )
            
            st.markdown("### 📝 Corporate Contract Vault")
            st.session_state.db["legal"]["vault"] = st.data_editor(
                st.session_state.db["legal"]["vault"],
                use_container_width=True,
                num_rows="dynamic",
                key="leg_vt_editor"
            )
            
        elif dept == "sales":
            st.markdown("### 🚀 Hubspot CRM Leads")
            st.session_state.db["sales"]["crm"] = st.data_editor(
                st.session_state.db["sales"]["crm"],
                use_container_width=True,
                num_rows="dynamic",
                key="sl_crm_editor"
            )
            
            st.markdown("### ✉️ Outreach Outbox")
            st.session_state.db["sales"]["outbox"] = st.data_editor(
                st.session_state.db["sales"]["outbox"],
                use_container_width=True,
                num_rows="dynamic",
                key="sl_out_editor"
            )
            
        elif dept == "procurement":
            st.markdown("### 🛒 SAP Supplier Registry")
            st.session_state.db["procurement"]["suppliers"] = st.data_editor(
                st.session_state.db["procurement"]["suppliers"],
                use_container_width=True,
                num_rows="dynamic",
                key="proc_sup_editor"
            )
            
            st.markdown("### 📑 RFP Responses & LATENCY Bids")
            st.session_state.db["procurement"]["rfp"] = st.data_editor(
                st.session_state.db["procurement"]["rfp"],
                use_container_width=True,
                num_rows="dynamic",
                key="proc_rfp_editor"
            )

# ----------------------------------------------------
# SIDEBAR NAVIGATION & TELEMETRY
# ----------------------------------------------------
with st.sidebar:
    st.markdown("## ▲ AETHERIS OP-CENTER")
    st.markdown("### Selected Department")
    
    st.session_state.active_dept = st.radio(
        "Select Internal Function",
        options=["it", "hr", "finance", "legal", "sales", "procurement"],
        format_func=lambda x: {
            "it": "🤖 IT Support",
            "hr": "👥 HR Operations",
            "finance": "💰 Finance & AP",
            "legal": "⚖️ Legal Contract",
            "sales": "🚀 Sales & Marketing",
            "procurement": "🛒 Procurement"
        }[x],
        label_visibility="collapsed"
    )
    st.markdown("---")
    
    # Render mini-status checklist of agents in sidebar for high-fidelity look
    st.markdown("### Agent Telemetry Network")
    active_dept_nodes = dept_configs[st.session_state.active_dept]["nodes"]
    for node_key, node_val in active_dept_nodes.items():
        if node_key == "bottom" and not node_val["visible"]:
            continue
        status_label = "IDLE"
        status_color = "gray"
        if st.session_state.active_agent == node_key:
            status_label = "ACTIVE"
            status_color = "green"
        elif node_key == "left" and st.session_state.approval_pending["active"] and st.session_state.approval_pending["metadata"]["agent"] == "Identity Agent":
            status_label = "PENDING APPROVAL"
            status_color = "orange"
        
        icon = node_val["icon"]
        label = node_val["label"]
        st.markdown(f"**{icon} {label}**: :{status_color}[{status_label}]")

# ----------------------------------------------------
# MAIN UI DISPATCHER (TABS SYSTEM)
# ----------------------------------------------------
dept_meta = dept_configs[st.session_state.active_dept]

st.markdown(f"""
<div class="op-header">
    <h1 style="margin: 0; padding-bottom: 5px;">Aetheris: <span class="accent-cyan">{dept_meta['title']}</span></h1>
    <p style="margin: 0; color: #9ca3af; font-size: 1rem;">{dept_meta['desc']}</p>
</div>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

tab_console, tab_db_view = st.tabs(["🎮 Operations Control Console", "📋 Enterprise Database Registry"])

# TAB 1: OPERATIONS CONSOLE
with tab_console:
    col_c1, col_c2 = st.columns([1.0, 1.0])
    
    # Right Column: Agent Nodes & Live trace logs
    # MUST define placeholders first so they are bound when scenarios trigger execute_agent_pipeline
    with col_c2:
        topo_placeholder = st.empty()
        term_placeholder = st.empty()
        
        # Draw initial status and logs
        update_topology_view(topo_placeholder)
        update_terminal_view(term_placeholder)
        
    # Left Column: Chat Intake & Presets
    with col_c1:
        st.write("### Intake Console")
        
        # Chat bubbles
        for msg in st.session_state.chat_history[st.session_state.active_dept]:
            with st.chat_message(msg["role"]):
                st.write(msg["text"])
                
        # Custom input
        chat_text = st.chat_input("Ask a question or enter a custom request...")
        if chat_text:
            st.session_state.chat_history[st.session_state.active_dept].append({"role": "user", "text": chat_text})
            
            txt_lower = chat_text.lower()
            if st.session_state.active_dept == "it":
                if "vpn" in txt_lower or "wifi" in txt_lower or "dns" in txt_lower:
                    run_it_scenario_2()
                elif "figma" in txt_lower or "adobe" in txt_lower:
                    run_it_scenario_3()
                else:
                    run_it_scenario_1()
            elif st.session_state.active_dept == "hr":
                if "onboard" in txt_lower or "new hire" in txt_lower:
                    run_hr_scenario_1()
                else:
                    run_hr_scenario_2()
            elif st.session_state.active_dept == "finance":
                if "fraud" in txt_lower or "discrepancy" in txt_lower or "bank" in txt_lower:
                    run_finance_scenario_2()
                else:
                    run_finance_scenario_1()
            elif st.session_state.active_dept == "legal":
                run_legal_scenario_1()
            elif st.session_state.active_dept == "sales":
                run_sales_scenario_1()
            elif st.session_state.active_dept == "procurement":
                run_procurement_scenario_1()
            st.rerun()

        # Presets dropdown
        st.write("---")
        st.write("**Simulation Preset Scenarios**")
        
        dept = st.session_state.active_dept
        if dept == "it":
            preset = st.selectbox("Select Scenario Preset", [
                "Select...",
                "Scenario 1: Salesforce & Monitor Provisioning",
                "Scenario 2: VPN Telemetry Diagnostics",
                "Scenario 3: Restricted Access Gate (Figma)"
            ], key="it_sel_preset")
            if st.button("Run Scenario", key="it_btn_run") and preset != "Select...":
                if preset.startswith("Scenario 1"):
                    st.session_state.chat_history["it"].append({"role": "user", "text": "Request Salesforce and a replacement monitor"})
                    run_it_scenario_1()
                elif preset.startswith("Scenario 2"):
                    st.session_state.chat_history["it"].append({"role": "user", "text": "My VPN connection keeps failing"})
                    run_it_scenario_2()
                elif preset.startswith("Scenario 3"):
                    st.session_state.chat_history["it"].append({"role": "user", "text": "I need access to Figma"})
                    run_it_scenario_3()
                st.rerun()
                
        elif dept == "hr":
            preset = st.selectbox("Select Scenario Preset", [
                "Select...",
                "Scenario 1: Onboard New Developer (Clara Vance)",
                "Scenario 2: Handbook Benefits RAG (Acupuncture Coverage)"
            ], key="hr_sel_preset")
            if st.button("Run Scenario", key="hr_btn_run") and preset != "Select...":
                if preset.startswith("Scenario 1"):
                    run_hr_scenario_1()
                elif preset.startswith("Scenario 2"):
                    st.session_state.chat_history["hr"].append({"role": "user", "text": "Is acupuncture covered under my benefits plan?"})
                    run_hr_scenario_2()
                st.rerun()
                
        elif dept == "finance":
            preset = st.selectbox("Select Scenario Preset", [
                "Select...",
                "Scenario 1: Process ACME Invoice (3-Way Match)",
                "Scenario 2: Anomaly Check (Discrepancy Alarm)"
            ], key="fin_sel_preset")
            if st.button("Run Scenario", key="fin_btn_run") and preset != "Select...":
                if preset.startswith("Scenario 1"):
                    run_finance_scenario_1()
                elif preset.startswith("Scenario 2"):
                    run_finance_scenario_2()
                st.rerun()
                
        elif dept == "legal":
            preset = st.selectbox("Select Scenario Preset", [
                "Select...",
                "Scenario 1: Scan NDA Playbook Deviations"
            ], key="leg_sel_preset")
            if st.button("Run Scenario", key="leg_btn_run") and preset != "Select...":
                if preset.startswith("Scenario 1"):
                    run_legal_scenario_1()
                st.rerun()
                
        elif dept == "sales":
            preset = st.selectbox("Select Scenario Preset", [
                "Select...",
                "Scenario 1: Enrich Lead (Intent Score 95)"
            ], key="sl_sel_preset")
            if st.button("Run Scenario", key="sl_btn_run") and preset != "Select...":
                if preset.startswith("Scenario 1"):
                    run_sales_scenario_1()
                st.rerun()
                
        elif dept == "procurement":
            preset = st.selectbox("Select Scenario Preset", [
                "Select...",
                "Scenario 1: Source Edge CDN RFP"
            ], key="proc_sel_preset")
            if st.button("Run Scenario", key="proc_btn_run") and preset != "Select...":
                if preset.startswith("Scenario 1"):
                    run_procurement_scenario_1()
                st.rerun()

        # Render approval buttons in Left Column under chat
        if st.session_state.approval_pending["active"]:
            st.markdown("---")
            meta = st.session_state.approval_pending["metadata"]
            st.markdown(f"""<div class="glass-card" style="border: 1px solid #f59e0b; background: rgba(245, 158, 11, 0.05); box-shadow: 0 0 15px rgba(245, 158, 11, 0.1);">
<h4 style="margin: 0; color: #f59e0b; display: flex; align-items: center; gap: 8px;">
    ⚠️ ACTION REQUIRES HUMAN AUTHORIZATION
</h4>
<div style="margin-top: 10px; font-size: 0.9rem;">
    <p style="margin: 3px 0;"><b>Agent:</b> <code style="color: #f59e0b;">{meta['agent']}</code></p>
    <p style="margin: 3px 0;"><b>Action:</b> <code>{meta['action']}</code></p>
    <p style="margin: 3px 0;"><b>Target:</b> <code>{meta['user']}</code></p>
</div>
</div>""", unsafe_allow_html=True)
            
            btn_cols = st.columns(2)
            if btn_cols[0].button("Approve & Execute", key="op_approve_btn"):
                resolve_override_decision(True)
                st.rerun()
            if btn_cols[1].button("Reject Request", key="op_reject_btn"):
                resolve_override_decision(False)
                st.rerun()

        # Sales outbox preview
        if st.session_state.active_dept == "sales" and len(st.session_state.outbox_emails) > 0:
            st.markdown("---")
            mail = st.session_state.outbox_emails[0]
            st.markdown(f"""<div class="glass-card" style="border-left: 4px solid #06b6d4;">
<h4 style="margin: 0; color: #06b6d4;">✉️ Outbound Email Draft</h4>
<p style="margin: 5px 0 0 0; font-size: 0.9rem;"><b>To:</b> {mail['to']}</p>
<p style="margin: 3px 0 10px 0; font-size: 0.9rem;"><b>Subject:</b> {mail['subject']}</p>
<div style="background: rgba(0, 0, 0, 0.2); padding: 10px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; font-size: 0.85rem;">{mail['body']}</div>
</div>""", unsafe_allow_html=True)

# TAB 2: SYSTEM DATABASES (Full width, completely visible)
with tab_db_view:
    st.write("## Dynamic System Registries")
    st.write("All fields in the database tables are fully resizable and editable. Changes will be persisted dynamically in memory.")
    
    db_editor_placeholder = st.empty()
    update_db_view(db_editor_placeholder)

