"""CheckItNow marketing landing — deploy on Streamlit Community Cloud."""

from __future__ import annotations

import streamlit as st

# Update this after Render deploy (Step 3).
DEMO_URL = "https://YOUR-APP.onrender.com"
CONTACT_EMAIL = "checkitnow123@gmail.com"

st.set_page_config(
    page_title="CheckItNow — Client & service CRM",
    page_icon="📋",
    layout="centered",
)

st.title("CheckItNow")
st.caption("Client & service CRM for solopreneurs")
st.markdown(
    """
Track clients, contract renewals, milestones, and reminders —
built for **tutors, coaches, agencies, and service businesses**.

No signup required for the live demo.
"""
)

col1, col2 = st.columns(2)
with col1:
    st.link_button("▶ Try live demo", DEMO_URL, use_container_width=True, type="primary")
with col2:
    st.link_button("✉ Contact us", f"mailto:{CONTACT_EMAIL}", use_container_width=True)

st.divider()
st.subheader("What you can try")
st.markdown(
    """
- Dashboard KPIs — click to filter clients instantly
- Clients list — search, groups, Excel export
- Milestones — session progress & completion log
- Reminder composer — SMS / email templates (EN + 中文)
"""
)

st.info(
    "Demo data resets when the server restarts. "
    "Your own branded desktop version is available on request."
)

st.caption(f"Questions? {CONTACT_EMAIL}")
