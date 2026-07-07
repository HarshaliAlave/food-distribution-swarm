import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import time
import pandas as pd
import random
from graph import app_graph

# ==========================================
# 1. PAGE SETUP & PREMIUM GLOBAL STYLING
# ==========================================
st.set_page_config(page_title="EcoFeast AI Control Tower", layout="wide", page_icon="♻️")

# High-end production styling overrides
st.markdown("""
    <style>
    /* Branding & Headline Grouping to fill the left layout beautifully */
    .brand-hero-container {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 20px;
    }
    .brand-hero-logo {
        font-size: 38px;
        line-height: 1;
    }
    .premium-hero-title {
        font-size: 54px !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
        margin-bottom: 15px !important;
        background: linear-gradient(135deg, #FFFFFF 30%, #2E8B57 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    /* Elegant gray subtitle prose */
    .premium-hero-subtitle {
        font-size: 17.5px !important;
        color: #A0AEC0 !important;
        margin-bottom: 35px !important;
        line-height: 1.6 !important;
    }
    /* Sleek container badge */
    .tech-badge {
        background: rgba(46, 139, 87, 0.12);
        color: #34D399;
        padding: 6px 16px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.5px;
        border: 1px solid rgba(46, 139, 87, 0.25);
        display: inline-block;
    }
    /* Clean custom card utility */
    .premium-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 16px;
        padding: 24px;
        height: 100%;
    }
    /* Hero Interactive Visualization Panel */
    .hero-vis-panel {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

if "started" not in st.session_state:
    st.session_state.started = False

if "registered_users" not in st.session_state:
    st.session_state.registered_users = {
        "Starbucks Downtown": {"password": "123", "role": "Restaurant"},
        "Dream House": {"password": "123", "role": "NGO"}
    }

if "active_contracts" not in st.session_state:
    st.session_state.active_contracts = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "current_run_state" not in st.session_state:
    st.session_state.current_run_state = None
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = "Standard Portal Access"

if "editable_inventory" not in st.session_state:
    st.session_state.editable_inventory = pd.DataFrame([
        {"item": "Fresh Salads", "quantity": 30, "type": "Perishable"},
        {"item": "Whole Milk Gallons", "quantity": 15, "type": "Dairy"},
        {"item": "Oatmeal Cookies", "quantity": 25, "type": "Bakery"}
    ])

def logout():
    st.session_state.logged_in = False
    st.session_state.user_role = None
    st.session_state.user_name = ""
    st.session_state.current_run_state = None
    st.rerun()

# ==========================================
# 2. VIEW RENDERERS (RESTAURANT & NGO)
# ==========================================
def render_restaurant_view(user_name):
    st.markdown(f"### 🏪 Restaurant Portal: <span style='color:#2E8B57;'>{user_name}</span>", unsafe_allow_html=True)
    
    st.warning("⚠️ **AI Warning:** Anomalous weather framework detected. Predictive engines forecast a **20% demand collapse** on fresh items.")
    
    total_co2 = 142 + sum([c["metrics"]["co2_saved_kg"] for c in st.session_state.active_contracts])
    total_meals = 184 + sum([sum([int(i["quantity"]) for i in c["items"] if str(i["quantity"]).isdigit()]) for c in st.session_state.active_contracts])
    
    m1, m2, m3 = st.columns(3)
    m1.markdown(f"<small>🌱 Carbon Saved</small><br><strong style='font-size:24px;'>{total_co2:.1f} kg CO₂</strong>", unsafe_allow_html=True)
    m2.markdown(f"<small>📦 Batches Sent</small><br><strong style='font-size:24px;'>{max(1, len(st.session_state.active_contracts))}</strong>", unsafe_allow_html=True)
    m3.markdown(f"<small>🥗 Meals Donated</small><br><strong style='font-size:24px;'>{int(total_meals)}</strong>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)
    st.write("📋 **Live Pitch Workspace: Adjust Surplus Inventory**")
    edited_df = st.data_editor(
        st.session_state.editable_inventory,
        use_container_width=True,
        num_rows="dynamic",
        key="inventory_editor"
    )
    st.session_state.editable_inventory = edited_df
    
    if st.button("🚀 Trigger Surplus Redistribution Loop", type="primary", key=f"btn_{user_name}", use_container_width=True):
        with st.status("🧠 Swarm executing via LangGraph...", expanded=False) as status:
            live_surplus_payload = edited_df.to_dict(orient="records")
            initial_state = {
                "surplus_items": live_surplus_payload,
                "selected_ngo": {},
                "negotiation_log": [],
                "status": "idle",
                "esg_metrics": {"co2_saved_kg": 0, "tax_deduction_usd": 0},
                "logistics_data": {"lat": 40.7128, "lon": -74.0060, "eta": "Calculating...", "distance": "Calculating..."}
            }
            time.sleep(0.5)
            
            final_state = app_graph.invoke(initial_state)
            status.update(label="✅ Loop Complete!", state="complete", expanded=False)
            st.session_state.current_run_state = final_state
            
            assigned_ngo = final_state.get('selected_ngo', {}).get('shelter_name')
            if not assigned_ngo or assigned_ngo == "Dream House":
                assigned_ngo = random.choice(["Hope House", "Salvation Hub", "City Food Bank", "Dream House"])
            
            total_items_qty = sum([int(row['quantity']) for row in live_surplus_payload if str(row['quantity']).isdigit()])
            calc_co2 = round(total_items_qty * 1.5, 1)
            calc_tax = round(total_items_qty * 3.0, 2)
            
            st.session_state.active_contracts.append({
                "id": f"#{random.randint(4000, 9999)}",
                "sender": user_name,
                "target_ngo": assigned_ngo,
                "items": live_surplus_payload,
                "metrics": {"co2_saved_kg": calc_co2, "tax_deduction_usd": calc_tax},
                "logistics": {
                    "lat": 40.7128 + random.uniform(-0.05, 0.05),
                    "lon": -74.0060 + random.uniform(-0.05, 0.05),
                    "eta": f"{random.randint(8, 28)} Mins",
                    "distance": f"{round(random.uniform(1.5, 7.2), 1)} miles"
                }
            })
            st.rerun()

    if st.session_state.current_run_state is not None:
        latest_run = st.session_state.active_contracts[-1] if st.session_state.active_contracts else None
        if latest_run:
            st.success(f"📍 **Assigned:** {latest_run['target_ngo']}")
            
            i1, i2 = st.columns(2)
            i1.markdown(f"<small>🌱 Carbon Averted</small><br><strong style='font-size:24px;'>{latest_run['metrics']['co2_saved_kg']} kg</strong>", unsafe_allow_html=True)
            i2.markdown(f"<small>💰 Tax Write-off</small><br><strong style='font-size:24px;'>${latest_run['metrics']['tax_deduction_usd']}</strong>", unsafe_allow_html=True)
            
            with st.expander("📦 View Redirected Inventory Manifesto JSON"):
                st.json(latest_run["items"])
                
            with st.expander("🗺️ View Active Transit Courier Map"):
                st.write(f"**ETA:** {latest_run['logistics']['eta']} | **Distance:** {latest_run['logistics']['distance']}")
                map_df = pd.DataFrame({'lat': [latest_run['logistics']["lat"]], 'lon': [latest_run['logistics']["lon"]]})
                st.map(map_df, zoom=11, use_container_width=True)

def render_ngo_view(user_name):
    st.markdown(f"### 🤝 NGO Logistics Portal: <span style='color:#4682B4;'>{user_name}</span>", unsafe_allow_html=True)
    
    my_contracts = st.session_state.active_contracts
    added_weight = sum([sum([int(i["quantity"]) for i in c["items"] if str(i["quantity"]).isdigit()]) for c in my_contracts])
    
    n1, n2, n3 = st.columns(3)
    n1.markdown(f"<small>⏳ Storage Left</small><br><strong style='font-size:24px;'>{max(15, 65 - len(my_contracts)*5)}%</strong>", unsafe_allow_html=True)
    n2.markdown(f"<small>🚚 Active Fleets</small><br><strong style='font-size:24px;'>{len(my_contracts) if my_contracts else 1}</strong>", unsafe_allow_html=True)
    n3.markdown(f"<small>📈 Total Inflow</small><br><strong style='font-size:24px;'>{165 + added_weight} lbs</strong>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin-bottom:30px;'></div>", unsafe_allow_html=True)
    st.markdown("##### 📊 Warehouse Intake Timeline Schedule")
    
    base_slots = [
        {"Time Slot": "03:00 PM", "Scheduled Volume (lbs)": 180, "Vehicle": "Courier-Gamma", "Status": "In-Transit"},
        {"Time Slot": "06:00 PM", "Scheduled Volume (lbs)": 45,  "Vehicle": "Courier-Delta", "Status": "Pending"},
        {"Time Slot": "09:00 AM", "Scheduled Volume (lbs)": 120, "Vehicle": "Courier-Alpha", "Status": "Delivered"},
        {"Time Slot": "12:00 PM", "Scheduled Volume (lbs)": 250, "Vehicle": "Courier-Beta", "Status": "Delivered"}
    ]
    
    if my_contracts:
        latest = my_contracts[-1]
        vol = sum([int(i["quantity"]) for i in latest["items"] if str(i["quantity"]).isdigit()])
        base_slots.insert(0, {
            "Time Slot": "Just Now", 
            "Scheduled Volume (lbs)": vol, 
            "Vehicle": "EcoRunner-Swarm", 
            "Status": "Dispatched"
        })
        
    df_analytics = pd.DataFrame(base_slots)
    st.bar_chart(df_analytics, x="Time Slot", y="Scheduled Volume (lbs)", color="#4682B4", use_container_width=True)
    
    with st.expander("📋 View Intake Cargo Ledger Details"):
        st.dataframe(df_analytics, use_container_width=True, hide_index=True)
        
    st.markdown("### 🗺️ Active Inbound Secure Contracts")
    if len(my_contracts) == 0:
        st.caption("No active inbound courier contracts found yet. Try triggering a loop on the restaurant side!")
    else:
        for contract in reversed(my_contracts):
            with st.chat_message("user", avatar="🚚"):
                st.write(f"**Shipment {contract['id']}** from *{contract['sender']}*")
                st.write(f"**Status:** En route | **ETA:** {contract['logistics']['eta']}")
                with st.expander("View Payload Inventory Ledger"):
                    st.write(pd.DataFrame(contract["items"]))


# ==========================================
# 3. GLOBAL ROUTING CONTROLLER
# ==========================================

# 3A. PREMIUM APP WELCOME PAGE INTERFACE
if not st.session_state.started:
    st.markdown("<div style='margin-top:30px;'></div>", unsafe_allow_html=True)
    
    # Hero Split Columns: 55% Text Layout & 45% Dynamic Visualization Map
    hero_left, hero_right = st.columns([1.2, 1.0], gap="large")
    
    with hero_left:
        # Combined Branding Row
        st.markdown("""
            <div class='brand-hero-container'>
                <div class='brand-hero-logo'>♻️ <strong>EcoFeast</strong></div>
                <div class='tech-badge'>⚡ Powered by LangGraph Multi-Agent Swarms</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<h1 class='premium-hero-title'>Autonomous Surplus Supply Chains.<br>Zero Waste Value Chains.</h1>", unsafe_allow_html=True)
        st.markdown("<p class='premium-hero-subtitle'>EcoFeast bridges localized retail surplus with non-profit logistical networks dynamically. We coordinate real-time programmatic asset matching, optimize courier routing states, and automate verifiable compliance reporting seamlessly.</p>", unsafe_allow_html=True)
        
        # CTA Buttons Row
        b1, b2 = st.columns([1, 1])
        with b1:
            if st.button("Launch Control Tower →", type="primary", use_container_width=True):
                st.session_state.started = True
                st.rerun()
        with b2:
            if st.button("Explore Portal Access", use_container_width=True):
                st.session_state.started = True
                st.rerun()

    with hero_right:
        # Beautiful Map visualization block filling out the right layout beautifully
        st.markdown("""
            <div class='hero-vis-panel'>
                <div style='display:flex; justify-content:between; align-items:center; margin-bottom:12px;'>
                    <span style='font-size:14px; font-weight:700; color:#FFFFFF;'>🛰️ LIVE MONITOR: LOCALIZED REDISTRIBUTION MATRIX</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Generates synthetic active swarm locations dynamically for visual flair
        swarm_mock_data = pd.DataFrame({
            'lat': [40.7128, 40.7306, 40.7589, 40.7061],
            'lon': [-74.0060, -73.9352, -73.9851, -73.9969],
            'size': [120, 90, 150, 70]
        })
        st.map(swarm_mock_data, latitude='lat', longitude='lon', size='size', zoom=11, use_container_width=True)
        st.caption("🟢 4 Active Autonomous Courier Nodes Routing Across Metro Hubs")
            
    st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)
    st.markdown("#### 🛠️ Core Technical Pillars")
    
    # Modular High-Performance Tech Stack Presentation Grid
    f1, f2, f3, f4 = st.columns(4, gap="medium")
    with f1:
        st.markdown("""
            <div class='premium-card'>
                <h3 style='margin-bottom:8px;'>🧠</h3>
                <h5 style='color:#FFFFFF; margin-bottom:6px;'>LangGraph Core</h5>
                <p style='font-size:13px; color:#A0AEC0; margin-bottom:0;'>Autonomous state machine routing data payloads securely between independent node systems.</p>
            </div>
        """, unsafe_allow_html=True)
    with f2:
        st.markdown("""
            <div class='premium-card'>
                <h3 style='margin-bottom:8px;'>📋</h3>
                <h5 style='color:#FFFFFF; margin-bottom:6px;'>Live Ledger Matrix</h5>
                <p style='font-size:13px; color:#A0AEC0; margin-bottom:0;'>Dynamic multi-tenant tables tracking active logistics metrics across global interfaces instantly.</p>
            </div>
        """, unsafe_allow_html=True)
    with f3:
        st.markdown("""
            <div class='premium-card'>
                <h3 style='margin-bottom:8px;'>🚚</h3>
                <h5 style='color:#FFFFFF; margin-bottom:6px;'>Fleet Despatch Engine</h5>
                <p style='font-size:13px; color:#A0AEC0; margin-bottom:0;'>Predictive automated distance matrices pairing surplus inventory with real-time field couriers.</p>
            </div>
        """, unsafe_allow_html=True)
    with f4:
        st.markdown("""
            <div class='premium-card'>
                <h3 style='margin-bottom:8px;'>🌱</h3>
                <h5 style='color:#FFFFFF; margin-bottom:6px;'>ESG Optimization</h5>
                <p style='font-size:13px; color:#A0AEC0; margin-bottom:0;'>Instantaneous validation curves monitoring tax reductions alongside actual carbon mitigation stats.</p>
            </div>
        """, unsafe_allow_html=True)

# 3B. INTERNAL SYSTEM CONTROL APPLICATION
else:
    with st.sidebar:
        st.markdown("## 🛠️ Pitch Controls")
        st.session_state.demo_mode = st.radio(
            "Select Layout View:",
            ["Standard Portal Access", "📋 Side-by-Side Live Swarm Monitor"]
        )
        st.markdown("---")
        if st.button("↩️ Return to Welcome Page", use_container_width=True):
            st.session_state.started = False
            st.rerun()

    if st.session_state.demo_mode == "📋 Side-by-Side Live Swarm Monitor":
        st.title("🎛️ Swarm Monitor Control Tower")
        
        left_pane, right_pane = st.columns(2, gap="large")
        with left_pane:
            current_restaurant = st.session_state.user_name if st.session_state.user_role == "Restaurant" else "Starbucks Downtown"
            render_restaurant_view(current_restaurant)
        with right_pane:
            if st.session_state.active_contracts:
                current_ngo_view = st.session_state.active_contracts[-1]["target_ngo"]
            else:
                current_ngo_view = "Hope House"
            render_ngo_view(current_ngo_view)

    else:
        if not st.session_state.logged_in:
            st.markdown("## ♻️ EcoFeast AI Entry Portal")
            
            col1, _ = st.columns([1.2, 1])
            with col1:
                selected_role_type = st.selectbox("Select Organization Type:", ["🏪 Restaurant", "🤝 NGO"])
                auth_tab, register_tab = st.tabs(["🔒 Sign In to Account", "📝 Register New Partner"])
                
                with auth_tab:
                    login_username = st.text_input("Organization Name", key="login_user")
                    login_password = st.text_input("Password", type="password", key="login_pass")
                    
                    if st.button("Log In", type="primary", use_container_width=True):
                        if login_username.strip():
                            st.session_state.logged_in = True
                            st.session_state.user_name = login_username
                            st.session_state.user_role = "Restaurant" if "Restaurant" in selected_role_type else "NGO"
                            st.rerun()
                
                with register_tab:
                    reg_username = st.text_input("New Organization Name", key="reg_user")
                    reg_password = st.text_input("Create Password", type="password", key="reg_pass")
                    
                    if st.button("Register Partner", type="primary", use_container_width=True):
                        if reg_username.strip():
                            assigned_role = "Restaurant" if "Restaurant" in selected_role_type else "NGO"
                            st.session_state.registered_users[reg_username] = {"password": reg_password, "role": assigned_role}
                            st.session_state.logged_in = True
                            st.session_state.user_name = reg_username
                            st.session_state.user_role = assigned_role
                            st.success(f"Successfully registered {reg_username}!")
                            time.sleep(0.4)
                            st.rerun()
        else:
            st.sidebar.button("Log Out Account", on_click=logout)
            if st.session_state.user_role == "Restaurant":
                render_restaurant_view(st.session_state.user_name)
            elif st.session_state.user_role == "NGO":
                render_ngo_view(st.session_state.user_name)
                