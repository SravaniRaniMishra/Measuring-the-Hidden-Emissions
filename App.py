import streamlit as st
import requests

# Hardcoded API Key
API_KEY = "nH0h936qthlpdKntSvHq"  # Replace with your actual API key

# Constants
CO2_ABSORBED_PER_TREE_PER_MONTH = 1.81  # kg CO2 per tree per month

# Function to fetch carbon intensity and power breakdown data
def get_carbon_data(region):
    """
    Fetch carbon intensity (gCO2/kWh) and power breakdown for a given region.
    """

    try:
        response = response = requests.get("https://api.electricitymap.org/v3/carbon-intensity/latest?zone=US-CAL-CISO",headers={"auth-token": f"nH0h936qthlpdKntSvHq"})
        print(response.json())
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        
        # Extract carbon intensity and power breakdown
        carbon_intensity = data.get("carbonIntensity", 0)  # gCO2/kWh
        power_breakdown = data.get("powerConsumptionBreakdown", {})  # Power sources
        
        return carbon_intensity, power_breakdown
    except requests.exceptions.HTTPError as e:
        st.error(f"HTTP Error: {e}")
        st.error(f"Response: {response.text}")  # Print the API response for debugging
        return 0, {}
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return 0, {}

# Function to estimate emissions for AI training
def estimate_ai_emissions(runtime_hours, carbon_intensity):
    """
    Estimate emissions for AI model training.
    Assumes an average power consumption of 400W for a GPU.
    """
    power_consumption_kW = 0.4  # 400W in kW
    energy_consumption_kWh = power_consumption_kW * runtime_hours
    emissions_kgCO2 = energy_consumption_kWh * (carbon_intensity / 1000)  # Convert gCO2 to kgCO2
    return emissions_kgCO2

# Function to estimate emissions for blockchain transactions
def estimate_blockchain_emissions(num_transactions, carbon_intensity):
    """
    Estimate emissions for blockchain transactions.
    Assumes an average energy consumption of 700 kWh per transaction (e.g., Bitcoin).
    """
    energy_consumption_kWh = 700 * num_transactions
    emissions_kgCO2 = energy_consumption_kWh * (carbon_intensity / 1000)  # Convert gCO2 to kgCO2
    return emissions_kgCO2

# Function to estimate emissions for data centers
def estimate_datacenter_emissions(server_power_kW, runtime_hours, carbon_intensity):
    """
    Estimate emissions for data center operations.
    """
    energy_consumption_kWh = server_power_kW * runtime_hours
    emissions_kgCO2 = energy_consumption_kWh * (carbon_intensity / 1000)  # Convert gCO2 to kgCO2
    return emissions_kgCO2

# Function to calculate compensation (number of trees to plant)
def calculate_compensation(total_emissions_kgCO2):
    """
    Calculate the number of trees needed to offset the emissions.
    """
    return total_emissions_kgCO2 / CO2_ABSORBED_PER_TREE_PER_MONTH

# Streamlit App
def main():
    st.title("Carbon Emission Tracker for Digital Technologies")
    st.write("Estimate the carbon emissions of AI, blockchain, and data center operations.")

    # Sidebar for user inputs
    st.sidebar.header("Input Parameters")
    region = st.sidebar.text_input("Enter Region Code (e.g., US-CAL-CISO for California)", "US-CAL-CISO")

    st.sidebar.subheader("AI Training")
    ai_runtime_hours = st.sidebar.slider("Training Runtime (hours)", 1, 100, 10, key="ai_runtime")

    st.sidebar.subheader("Blockchain")
    num_transactions = st.sidebar.slider("Number of Transactions", 1, 1000, 100, key="blockchain")

    st.sidebar.subheader("Data Center")
    server_power_kW = st.sidebar.slider("Server Power Consumption (kW)", 1, 100, 10, key="server_power")
    dc_runtime_hours = st.sidebar.slider("Runtime (hours)", 1, 100, 10, key="dc_runtime")

    # Fetch carbon intensity and power breakdown for the region
    carbon_intensity, power_breakdown = get_carbon_data(region)
    
    # Display carbon intensity and power breakdown
    st.sidebar.write(f"Carbon Intensity in {region}: {carbon_intensity} gCO2/kWh")
    st.sidebar.write("Power Breakdown:")
    for source, value in power_breakdown.items():
        st.sidebar.write(f"- {source}: {value}%")

    # Calculate emissions for all technologies
    if st.sidebar.button("Calculate Emissions"):
        ai_emissions = estimate_ai_emissions(ai_runtime_hours, carbon_intensity)
        blockchain_emissions = estimate_blockchain_emissions(num_transactions, carbon_intensity)
        dc_emissions = estimate_datacenter_emissions(server_power_kW, dc_runtime_hours, carbon_intensity)

        # Total emissions
        total_emissions = ai_emissions + blockchain_emissions + dc_emissions

        # Display emissions
        st.write(f"Estimated Emissions for AI Training: {ai_emissions:.2f} kg CO2")
        st.write(f"Estimated Emissions for Blockchain Transactions: {blockchain_emissions:.2f} kg CO2")
        st.write(f"Estimated Emissions for Data Center Operations: {dc_emissions:.2f} kg CO2")
        st.write(f"**Total Emissions:** {total_emissions:.2f} kg CO2")

        # Calculate compensation (number of trees to plant)
        trees_needed = calculate_compensation(total_emissions)
        st.write(f"**Compensation:** To offset these emissions, you need to plant approximately **{trees_needed:.2f} trees per month**.")

        # Visualize emissions in a bar chart
        emissions_data = {
            "AI Training": ai_emissions,
            "Blockchain": blockchain_emissions,
            "Data Center": dc_emissions,
        }
        st.bar_chart(emissions_data)
        st.markdown(
            f"**Take Action:** [ 🌳Click here to donate and plant trees 🌳](https://onetreeplanted.org/)"

        )

# Run the app
if __name__ == "__main__":
    main()
