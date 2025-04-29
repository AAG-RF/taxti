import json
import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ——— CONFIG: Business-Deductible Subscriptions ———
SUBSCRIPTION_GROUPS = {
    "AI Assistants": [
        "OpenAI - ChatGPT Plus",
        "OpenAI - ChatGPT Pro",
        "Anthropic - Claude Pro",
        "Anthropic - Claude Max",
        "xAI - SuperGrok",  
        "GitHub Copilot",
        "Grammarly Premium/Business",
        "Jasper AI Business",  
        "Perplexity Pro",  
        "QuillBot Premium",  
        "Otter.ai Business"  
    ],
    "Accounting & Finance": [
        "Xero",
        "QuickBooks Online",
        "FreshBooks",  
        "Wave Accounting Premium",  
        "Zoho Books",  
        "Sage Business Cloud Accounting",  
        "Bench Bookkeeping"  
    ],
    "Office & Productivity": [
        "Microsoft 365 Personal",
        "Microsoft 365 Family",
        "Google Workspace Business",
        "Notion Team/Business",
        "Zoom Pro/Business",
        "Microsoft Teams",
        "Airtable Pro/Business",  
        "ClickUp Business",  
        "Todoist Business",  
        "Evernote Business",  
        "Zoho Workplace"  
    ],
    "Creative Tools": [
        "Adobe Creative Cloud",
        "Canva Pro",
        "Excalidraw",
        "LucidCharts",
        "Adobe Stock",
        "Figma Professional",  
        "Sketch Business",  
        "CorelDRAW Graphics Suite",  
        "Affinity Designer/Serif",  
        "Procreate Dreams",  
        "Envato Elements"  
    ],
    "Storage": [
        "Dropbox Business",
        "OneDrive for Business",
        "Google One / Google Drive",
        "Box Business", 
        "pCloud Business", 
        "Mega Business",  
        "iCloud+ for Business"  
    ],
    "AI Agents": [
        "MidJourney",
        "Agno",
        "RunwayML", 
        "Runway AI Pro",  
        "Replicate",
        "Fal.ai",
        "DALL·E 3 API",  
        "Synthesia Professional",  
        "Descript Overdub"
    ],
    "Cloud Services": [
        "Microsoft Azure",
        "Vercel",
        "Amazon Web Services",
        "Google Cloud Platform",
        "IBM Cloud",  
        "Oracle Cloud",  
        "DigitalOcean",  
        "Linode (Akamai Cloud)",  
        "Heroku"  
    ],
    "Communication & Collaboration": [
        "Slack Standard/Plus",
        "Cisco Webex Business",  
        "RingCentral MVP",  
        "Flock Pro",  
        "Mattermost Enterprise",  
        "Rocket.Chat Team"  
    ],
    "Project Management": [
        "Monday.com",
        "Asana Premium/Business",
        "Trello Business Class",
        "Jira Software",  
        "ClickUp Business",  
        "Smartsheet Business",  
        "Basecamp Business",  
        "Wrike Business"  
    ],
    "CRM & Marketing": [
        "Salesforce Sales Cloud",
        "HubSpot CRM",
        "Mailchimp Premium",
        "Zoho CRM Plus",  
        "Pipedrive",  
        "ActiveCampaign",  
        "Constant Contact",  
        "Keap Pro",  
        "Marketo Engage"  
    ],
    "E-commerce": [
        "Shopify",
        "Stripe",
        "BigCommerce",  
        "WooCommerce",  
        "Squarespace Commerce",  
        "Magento Commerce",  
        "Wix eCommerce"  
    ],
    "Other": [
        "Other (Manual Entry)",
        "Zapier Business",  
        "Hootsuite Professional",  
        "Sprout Social",  
        "LastPass Business",  
        "1Password Business",
        "Bitwarden",  
        "Tableau",  
        "SurveyMonkey Team",  
        "DocuSign Business Pro"  
    ]
}

# ——— DEFAULTS ———
first_group = list(SUBSCRIPTION_GROUPS.keys())[0]
DEFAULTS = {
    "sub_group": first_group,
    "sub_choice": "",                # force user to pick
    "manual_name": "",
    "monthly_cost": 0.0,
    "months_paid": 0,
    "work_use_percent": 100,
}

# ——— INIT SESSION STATE ———
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)
st.session_state.setdefault("subscriptions", [])

# ——— CALLBACKS ———
def reset_sub_choice():
    """Clear the subscription choice whenever the group changes."""
    st.session_state.sub_choice = ""

def add_and_reset():
    grp    = st.session_state.sub_group
    choice = st.session_state.sub_choice
    name   = (
        st.session_state.manual_name
        if choice == "Other (Manual Entry)"
        else choice
    )
    cost   = st.session_state.monthly_cost
    months = st.session_state.months_paid
    pct    = st.session_state.work_use_percent

    # —— VALIDATION ——  
    if not choice:
        st.warning("❗ Please select a subscription before adding.")
        return
    if choice == "Other (Manual Entry)" and not name:
        st.warning("❗ Enter a name for your manual subscription.")
        return
    if cost <= 0:
        st.warning("❗ Monthly cost must be greater than $0.")
        return
    if months <= 0:
        st.warning("❗ Months paid must be at least 1.")
        return

    # —— APPEND ——  
    st.session_state.subscriptions.append({
        "Group": grp,
        "Name": name,
        "Monthly Cost": cost,
        "Months Paid": months,
        "Work Use (%)": pct,
        "Deductible Amount": cost * months * (pct / 100)
    })

    # —— RESET ——  
    for k, v in DEFAULTS.items():
        st.session_state[k] = v

# ——— APP UI ———
st.title("📜 Subscription Tax Deduction Calculator (Australia)")
st.write("Enter your business-related subscriptions below to estimate your deductible amounts.")

# 1. Parent dropdown: Selecting a group resets the child dropdown
st.selectbox(
    "Subscription Group",
    list(SUBSCRIPTION_GROUPS.keys()),
    key="sub_group",
    on_change=reset_sub_choice
)

# 2. Child dropdown: Options depend on the selected group
raw_opts = SUBSCRIPTION_GROUPS[st.session_state.sub_group]
opts = [""] + raw_opts
st.selectbox(
    "Subscription",
    opts,
    key="sub_choice",
    format_func=lambda x: "— select one —" if x == "" else x
)

# 3. The rest of the form
with st.form("add_subscription"):
    if st.session_state.sub_choice == "Other (Manual Entry)":
        st.text_input("Enter Subscription Name", key="manual_name")

    st.number_input("Monthly Cost (AUD)", min_value=0.0, format="%.2f", key="monthly_cost")
    st.number_input("Months Paid", min_value=0, step=1, key="months_paid")
    st.slider("Work Usage (%)", min_value=0, max_value=100, key="work_use_percent")

    st.form_submit_button("Add Subscription", on_click=add_and_reset)

# ——— DISPLAY & EXPORT ———
if st.session_state.subscriptions:
    df = pd.DataFrame(st.session_state.subscriptions)
    st.write("### Your Subscriptions")
    st.dataframe(df.style.format({
        "Monthly Cost": "${:.2f}",
        "Deductible Amount": "${:.2f}"
    }))

    total = df["Deductible Amount"].sum()
    st.write(f"## 🧮 Estimated Total Deduction: **${total:,.2f}**")

    # prepare CSV
    csv_str   = df.to_csv(index=False)
    csv_bytes = csv_str.encode("utf-8")

    # Download button
    st.download_button(
        "📥 Download CSV",
        data=csv_bytes,
        file_name="subscriptions.csv",
        mime="text/csv",
    )

    # Copy to clipboard button
    copy_html = f"""
    <button id="copy-btn" style="
        padding:8px 16px;
        font-size:14px;
        margin-top:8px;
        cursor:pointer;
    ">
        📋 Copy CSV to clipboard
    </button>
    <script>
        const csvData = {json.dumps(csv_str)};
        document.getElementById("copy-btn").addEventListener("click", () => {{
            navigator.clipboard.writeText(csvData)
            .then(() => {{
                document.getElementById("copy-btn").innerText = "✅ Copied!";
            }})
            .catch(console.error);
        }});
    </script>
    """
    components.html(copy_html, height=80, scrolling=False)

# ——— RESET ALL ———
if st.button("Reset All"):
    st.session_state.subscriptions.clear()
