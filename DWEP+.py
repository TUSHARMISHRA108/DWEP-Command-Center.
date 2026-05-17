import streamlit as st
import pandas as pd
import numpy as np
import time
from scipy.optimize import minimize

# 1. Page Configuration
st.set_page_config(page_title="DWEP+ Optimization Framework", layout="wide")

# 2. Plain Text Header Section
st.title("🌊 DWEP+ Hydro-Informatics Framework")
st.caption("Research Prototype: Multi-Node Decentralized Water Exchange Optimization & Cryptographic Gateway Verification")
st.write("This framework couples mathematical process optimization with simulated data streams to automate wastewater resource distribution across urban-industrial nodes.")

st.divider()

# 3. Sidebar Sensor Controls (Input Data)
st.sidebar.header("🔬 Input Telemetry Constraints")
st.sidebar.write("Configure real-time stream parameters from decentralized municipal treatment facilities.")

industry = st.sidebar.selectbox(
    "Industrial Offtaker Target", 
    ["Durgapur Steel Plant (DSP)", "DPL Thermal Unit", "Asansol Industrial Cluster"]
)
input_ph = st.sidebar.slider("Node-01: IoT Monitored pH Stream", 4.0, 10.0, 7.2, step=0.1)
input_tds = st.sidebar.slider("Node-01: IoT Monitored TDS (ppm)", 200, 3500, 850)

st.sidebar.divider()
st.sidebar.header("📐 Optimization Parameters")
target_max_tds = st.sidebar.slider("Maximum Allowed Blended TDS (ppm)", 500, 2000, 1200)

# --- MATHEMATICAL CORE: WATER BLENDING OPTIMIZATION (SCIPY) ---
# Simulating blending with a secondary local water source (Node-02) to achieve target specifications at minimal cost
node2_tds = 1800
node2_ph = 6.1
cost_node1 = 12.0  # Sourcing cost in INR per kL
cost_node2 = 5.0   # Sourcing cost in INR per kL

def objective(x):
    # Minimize total procurement cost: (Fraction_1 * Cost_1) + (Fraction_2 * Cost_2)
    return (x[0] * cost_node1) + (x[1] * cost_node2)

# Operational constraints: 
# 1. Fractions must sum up to exactly 1.0 (100% volume)
# 2. Resulting blended TDS must remain below the industry threshold
constraints = [
    {'type': 'eq', 'fun': lambda x: x[0] + x[1] - 1.0},
    {'type': 'ineq', 'fun': lambda x: target_max_tds - (x[0] * input_tds + x[1] * node2_tds)}
]
bounds = ((0, 1), (0, 1))

# Run the numerical optimizer
res = minimize(objective, [0.5, 0.5], method='SLSQP', bounds=bounds, constraints=constraints)

if res.success:
    opt_node1, opt_node2 = res.x[0], res.x[1]
    blended_tds = (opt_node1 * input_tds) + (opt_node2 * node2_tds)
    blended_cost = res.fun
    opt_success = True
else:
    opt_success = False
    blended_tds = input_tds
    blended_cost = cost_node1

# --- EVALUATE GATEWAY STATUS ---
is_quality_safe = (6.0 <= input_ph <= 8.5) and (blended_tds <= target_max_tds)

# 4. Standard Metric Displays (KPIs)
st.subheader("📊 Operational Telemetry Overview")
m1, m2, m3, m4 = st.columns(4)

m1.metric(label="Target Infrastructure Node", value=industry[:22])
m2.metric(label="Measured Stream Node-01", value=f"{input_ph} pH")
m3.metric(label="Calculated Grid Blend", value=f"{int(blended_tds)} ppm")
m4.metric(
    label="Gatekeeper Valve State", 
    value="DISPATCH OPEN" if is_quality_safe else "RECIRCULATION",
    delta="System Cleared" if is_quality_safe else "Loop Intercepted",
    delta_color="normal" if is_quality_safe else "inverse"
)

st.divider()

# 5. Optimization Algorithm Performance Data
st.subheader("🧮 Numerical Optimization Summary")
st.write("Using Sequential Least-Squares Programming (SLSQP) to establish algorithmic blending criteria:")

if opt_success:
    c1, c2, c3 = st.columns(3)
    c1.metric("Optimal Blend Ratio: Node-01", f"{opt_node1 * 100:.1f} %")
    c2.metric("Optimal Blend Ratio: Node-02", f"{opt_node2 * 100:.1f} %")
    c3.metric("Calculated Marginal Cost", f"₹ {blended_cost:.2f} / kL")
else:
    st.warning("⚠️ Constraints Unsatisfiable: Input physical parameters cannot be mathematically optimized to meet target values. Grid injection is suspended.")

st.divider()

# 6. Physical Infrastructure Stage Diagnostics
st.subheader("⚙️ Multi-Tier Physical and Chemical Treatment Steps")
st.write("Baseline engineering status inside municipal Sewage Treatment Plant (STP) units:")

t1, t2, t3 = st.columns(3)
with t1:
    st.markdown("**Stage 1: Biological Treatment**")
    st.write("Technology: Moving Bed Biofilm Reactor (MBBR)")
    st.write("Objective: Reduces baseline Biochemical Oxygen Demand (BOD) dynamics via structured fluidized biomass arrays.")
    st.caption("Status: Nominal Continuous Operation")

with t2:
    st.markdown("**Stage 2: Separation Layer**")
    st.write("Technology: Ultrafiltration (UF) Module Arrays")
    st.write("Objective: Mechanical isolation filtration down to 0.01 microns protecting distribution piping networks from suspended solids.")
    st.caption("Status: Nominal Continuous Operation")

with t3:
    st.markdown("**Stage 3: Chemical Stabilization**")
    st.write("Technology: Activated Carbon + Programmatic pH Dosing")
    st.write("Objective: Adsorbs aromatic traces; uses computerized feed-forward pump adjustments to balance parameters.")
    if is_quality_safe:
        st.caption("Status: Active Stabilization Loop Running")
    else:
        st.caption("Status: Emergency Diversion Mode Engaged")

st.divider()

# 7. Stochastic Process Simulation Chart
st.subheader("🛰️ Continuous Sensor Historical Log (Markov Chain Simulation)")
st.write("This index models real-time sensor fluctuation metrics using an Auto-Regressive Stochastic Process Model rather than static inputs.")

np.random.seed(42)
time_steps = 30
simulated_ph = []
current_ph = input_ph

for _ in range(time_steps):
    # Mathematical auto-regressive step: fluctuates randomly but balances back toward current slider setting
    current_ph = 0.8 * current_ph + 0.2 * input_ph + np.random.normal(0, 0.07)
    simulated_ph.append(max(4.0, min(10.0, current_ph)))

df_chart = pd.DataFrame({'Simulated Continuous pH Stream': simulated_ph})
st.line_chart(df_chart)

# --- SYSTEM DECISION STATE ALERTS ---
if is_quality_safe:
    st.success(f"**Verification Passed:** Water sample data complies with parameters. Cryptographic clearing verified. Payload released to {industry} distribution pipeline.")
else:
    st.error("**System Threshold Fault:** Water variables crossed safety parameters. Automated valves engaged. Fluid stream redirected back to primary polishing infrastructure.")

st.divider()

# 8. Pure Distributed Ledger Verification Proofs
st.subheader("⛓️ Web3 Distributed State Verification Ledger")
st.write("Immutable programmatic audit records matching validation transactions:")

status_label = "TX_COMMITTED // VALID" if is_quality_safe else "TX_REJECTED // RECIRCULATE"

log_data = {
    "Cryptographic Block Hash": ["0x7d9a8e...3b12", "0x4f1c8a...9e51", f"0x9b4e{'1a' if is_quality_safe else '9f'}...7c84"],
    "System Timestamp": [time.strftime("%Y-%m-%d %H:%M:%S UTC")] * 3,
    "Mean Computed TDS": [f"{int(blended_tds)} ppm"] * 3,
    "Consensus Layer State": [status_label] * 3
}

st.dataframe(pd.DataFrame(log_data), use_container_width=True)

# 9. Settlement Trigger Button
st.write("### Interactive Transaction Layer")
if st.button("Simulate Smart Contract Ledger Commit"):
    if is_quality_safe:
        st.balloons()
        st.success("Consensus Complete. Escrow parameters satisfied. Sourcing value automatically transferred from client account to municipal node wallet.")
    else:
        st.snow()
        st.error("Transaction Aborted: Validation criteria did not resolve successfully. Escrow release suspended across distributed nodes.")