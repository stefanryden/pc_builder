import streamlit as st
import json
import pandas as pd
import plotly.express as px
from utils.compatibility import get_compatible_components
from utils.price_analysis import calculate_total_price, get_price_rating, format_price
from utils.tradera_integration import get_tradera_suggestions

# Load component data
@st.cache_data
def load_component_data():
    with open('data/component_data.json', 'r') as f:
        return json.load(f)

# Page configuration
st.set_page_config(
    page_title="PC Byggare Pro",
    page_icon="🖥️",
    layout="wide"
)

# Title and description
st.title("🖥️ PC Byggare Pro")
st.markdown("""
Välkommen till PC Byggare Pro! Välj ett grafikkort för att börja bygga din anpassade dator. 
Vi hjälper dig att hitta kompatibla komponenter och analyserar priser för både nya och begagnade delar.
""")

try:
    # Load data
    components = load_component_data()

    # GPU Selection
    st.subheader("1. Välj ditt Grafikkort")
    selected_gpu = st.selectbox(
        "Välj GPU modell",
        options=components['gpus'],
        format_func=lambda x: x['name']
    )

    if selected_gpu:
        # Get compatible components
        compatible_components = get_compatible_components(selected_gpu, components)
        
        # Component selection
        st.subheader("2. Kompatibla Komponenter")
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_motherboard = st.selectbox(
                "Moderkort",
                options=compatible_components['motherboards'],
                format_func=lambda x: x['name']
            )
            
            selected_cpu = st.selectbox(
                "Processor",
                options=compatible_components['cpus'],
                format_func=lambda x: x['name']
            )
            
            selected_ram = st.selectbox(
                "Arbetsminne",
                options=compatible_components['ram'],
                format_func=lambda x: x['name']
            )
            
        with col2:
            selected_psu = st.selectbox(
                "Nätaggregat",
                options=compatible_components['psus'],
                format_func=lambda x: x['name']
            )
            
            selected_case = st.selectbox(
                "Chassi",
                options=compatible_components['cases'],
                format_func=lambda x: x['name']
            )
            
            selected_cooler = st.selectbox(
                "Processorkylare",
                options=compatible_components['coolers'],
                format_func=lambda x: x['name']
            )

        # Create selected build dictionary
        selected_build = {
            'gpu': selected_gpu,
            'motherboard': selected_motherboard,
            'cpu': selected_cpu,
            'ram': selected_ram,
            'psu': selected_psu,
            'case': selected_case,
            'cooler': selected_cooler
        }

        # Price Analysis
        st.subheader("3. Prisanalys")
        
        total_new = calculate_total_price(selected_build, 'new')
        total_used = calculate_total_price(selected_build, 'used')
        
        # Create price comparison table
        price_data = []
        for component_type, component in selected_build.items():
            price_data.append({
                'Component': {
                    'gpu': 'Grafikkort',
                    'motherboard': 'Moderkort',
                    'cpu': 'Processor',
                    'ram': 'Arbetsminne',
                    'psu': 'Nätaggregat',
                    'case': 'Chassi',
                    'cooler': 'Processorkylare'
                }[component_type],
                'Name': component['name'],
                'New Price': component['price_new'],
                'Used Price': component['price_used'],
                'New Price Display': format_price(component['price_new']),
                'Used Price Display': format_price(component['price_used']),
                'Rating': get_price_rating(component['price_new'], component['price_used'])
            })
        
        # Create display DataFrame
        df_display = pd.DataFrame(price_data)[['Component', 'Name', 'New Price Display', 'Used Price Display', 'Rating']]
        df_display.columns = ['Komponent', 'Namn', 'Nypris', 'Begagnat pris', 'Betyg']
        st.table(df_display)
        
        # Price summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Totalt Nypris", format_price(total_new))
        with col2:
            st.metric("Totalt Begagnat Pris", format_price(total_used))
        with col3:
            savings = total_new - total_used
            st.metric("Möjlig Besparing", format_price(savings))
        
        # Price visualization
        df_plot = pd.DataFrame(price_data)
        df_plot = df_plot.rename(columns={
            'New Price': 'Nypris',
            'Used Price': 'Begagnat pris'
        })
        
        fig = px.bar(
            df_plot,
            x='Component',
            y=['Nypris', 'Begagnat pris'],
            title='Prisjämförelse för Komponenter',
            barmode='group',
            labels={'value': 'Pris (kr)', 'variable': 'Pristyp', 'Component': 'Komponent'}
        )
        
        # Update layout with Swedish labels
        fig.update_layout(
            yaxis_title="Pris (kr)",
            xaxis_title="Komponent",
            legend_title="Pristyp",
            font=dict(family="Arial", size=12),
            legend=dict(
                title_text="Pristyp",
                itemsizing="constant",
                title_font_size=12,
                font=dict(size=10),
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01
            )
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Tradera Integration
        st.subheader("4. Tradera Förslag")
        
        tabs = st.tabs([
            {
                'gpu': 'Grafikkort',
                'motherboard': 'Moderkort',
                'cpu': 'Processor',
                'ram': 'Arbetsminne',
                'psu': 'Nätaggregat',
                'case': 'Chassi',
                'cooler': 'Processorkylare'
            }[comp_type] for comp_type in selected_build.keys()
        ])
        
        for tab, (comp_type, component) in zip(tabs, selected_build.items()):
            with tab:
                suggestions = get_tradera_suggestions(component)
                if suggestions:
                    auctions = [s for s in suggestions if s['listing_type'] == 'auction']
                    buy_now = [s for s in suggestions if s['listing_type'] == 'buy_now']
                    
                    if auctions:
                        st.subheader("🔨 Auktioner")
                        auctions_df = pd.DataFrame(auctions)
                        auctions_df['Nuvarande bud'] = auctions_df['current_bid'].apply(format_price)
                        auctions_df['Tid kvar'] = auctions_df['time_remaining']
                        auctions_df['Antal bud'] = auctions_df['num_bids']
                        
                        st.dataframe(
                            auctions_df[['title', 'Nuvarande bud', 'Tid kvar', 'Antal bud', 'condition', 'link']],
                            column_config={
                                "link": st.column_config.LinkColumn("Länk till annons"),
                                "title": "Objekt",
                                "Nuvarande bud": "Nuvarande bud",
                                "Tid kvar": "Tid kvar",
                                "Antal bud": "Antal bud",
                                "condition": "Skick"
                            },
                            hide_index=True
                        )
                    
                    if buy_now:
                        st.subheader("🛒 Köp Nu")
                        buy_now_df = pd.DataFrame(buy_now)
                        buy_now_df['Pris'] = buy_now_df['fixed_price'].apply(format_price)
                        
                        st.dataframe(
                            buy_now_df[['title', 'Pris', 'condition', 'link']],
                            column_config={
                                "link": st.column_config.LinkColumn("Länk till annons"),
                                "title": "Objekt",
                                "Pris": "Pris",
                                "condition": "Skick"
                            },
                            hide_index=True
                        )
                else:
                    st.info("Inga Tradera-objekt hittades för denna komponent.")
        
        # Export button
        st.download_button(
            label="Exportera bygget som CSV",
            data=df_display.to_csv(index=False).encode('utf-8'),
            file_name='pc_bygge.csv',
            mime='text/csv'
        )

except Exception as e:
    st.error(f"Ett fel uppstod: {str(e)}")
    st.error("Vänligen försök igen senare eller kontakta support om problemet kvarstår.")
