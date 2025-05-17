import streamlit as st


def home_page():
    # Page title and main header with logo/emoji styling
    st.markdown("""
    # 🏢 Bangalore Apartment Finder & Analysis
    *Your complete solution for finding and analyzing apartments in Bangalore*
    """)
    
    # Brief introduction section
    st.markdown("""
    ## About This App
    
    This application helps you navigate Bangalore's real estate market with data-driven insights.
    Whether you're buying, renting, or just researching, our tools provide valuable information
    to make informed decisions about properties across Bangalore.
    """)
    
    # Key statistics in expander
    with st.expander("📊 Current Market Snapshot", expanded=True):
        # Create 4 columns for key stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Properties Listed", value="5,345", delta="152 new")
            
        with col2:
            st.metric(label="Avg. Price", value="₹2.04 Cr", delta="-3.2%")
            
        with col3:
            st.metric(label="Avg. Price/sqft", value="₹9,855", delta="2.5%")
            
        with col4:
            st.metric(label="Avg. Area", value="1,679 sqft", delta=None)
    
    # Features section with cards
    st.markdown("## 🛠️ Our Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔮 Price Predictor
        
        Get estimated prices for apartments in Bangalore based on:
        - Zone/Sector (East, North, South, West)
        - Built Up Area (sq.ft.)
        - Number of Bedrooms
        - Construction Status (New Property, etc.)
        - Facility Category
        
        Our ML model analyzes these inputs to provide accurate price estimates for your potential investment.
        """)

        
    with col2:
        st.markdown("""
        ### 📈 Analysis Dashboard
        
        Visualize market trends and property distribution with our interactive dashboard:
        - Overview tab with key property metrics
        - Price Analysis tab for detailed price trends
        - Filter by zone, BHK type, and construction status
        - Analyze property distribution across Bangalore
        """)
    
    st.markdown("---")
    
    
    
    st.markdown("""
        ### 🔍 Recommend Similar Apartments
        
        Find apartments in Bangalore based on:
        - Similarity to other properties
        - Location proximity
        - Customizable recommendation algorithm
        
        Adjust the importance of location, amenities, and price to tailor recommendations to your preferences.
        """)
 
        

    

    
    # User tips section
    with st.expander("💡 Pro Tips for Using This App"):
        st.write("### How to get the most from each tool:")
        
        st.markdown("""
        **Price Predictor:**
        - Enter accurate built-up area for precise estimates
        - Compare predictions across different zones
        - New properties typically command higher prices
        
        **Analysis Dashboard:**
        - Use the filters to narrow down properties by zone and BHK type
        - The Overview tab shows high-level statistics
        - Price Analysis tab helps identify value opportunities
        
        **Recommend Apartments:**
        - Start with an apartment you like (e.g., "21st Castle Green Boulevard")
        - Adjust the recommendation weights to match your priorities
        - Try both Similar Apartments and Nearby Locations tabs
        """)
    
    # Footer
    st.markdown("""
    ---
    ### Get Started
    
    Select any option from the sidebar to begin exploring Bangalore's real estate market.
    
    *Data last updated: May 10, 2025*
    """)


if __name__ == "__main__":
    # Set page configuration
    st.set_page_config(
        page_title="Bangalore Apartment Finder",
        page_icon="🏢",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state for navigation
    if 'page' not in st.session_state:
        st.session_state.page = "Home"
    
    # Call the home page function
    home_page()
