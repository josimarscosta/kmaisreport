import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import io

# Configuração da página
st.set_page_config(
    page_title="Dashboard KMAIS - Não Conformidades",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para responsividade
st.markdown("""
<style>
    /* Responsividade geral */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    /* Header customizado */
    .header-container {
        background: linear-gradient(135deg, #E30613, #C41E3A);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #E30613;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #E30613;
        margin-bottom: 0.2rem;
    }
    
    .kpi-subtitle {
        font-size: 0.8rem;
        color: #999;
    }
    
    /* Responsividade para mobile */
    @media (max-width: 768px) {
        .header-title {
            font-size: 1.8rem;
        }
        
        .header-subtitle {
            font-size: 1rem;
        }
        
        .kpi-value {
            font-size: 2rem;
        }
        
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    
    /* Gráficos responsivos */
    .plotly-graph-div {
        width: 100% !important;
    }
    
    /* Tabelas responsivas */
    .dataframe {
        width: 100%;
        overflow-x: auto;
    }
    
    /* Upload area */
    .upload-section {
        border: 2px dashed #E30613;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        background: #fafafa;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_real_data():
    """Carrega dados reais da planilha NCKmais22-25.xlsx como padrão"""
    try:
        # Dados reais extraídos da planilha NCKmais22-25.xlsx
        data = [
            # 2025
            {'data': '2025-06-24', 'ano': 2025, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 410, 'status': 'K069', 'responsabilidade': 'KMAIS'},
            {'data': '2025-06-19', 'ano': 2025, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambores fermentados', 'volume_impactado': 410, 'status': 'J040', 'responsabilidade': 'KMAIS'},
            {'data': '2025-04-08', 'ano': 2025, 'cliente': 'Materne', 'categoria': 'Entrega', 'tipo': 'Paletização', 'volume_impactado': 0, 'status': 'J199', 'responsabilidade': 'KMAIS'},
            {'data': '2025-02-18', 'ano': 2025, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 205, 'status': 'J200', 'responsabilidade': 'KMAIS'},
            {'data': '2025-02-10', 'ano': 2025, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Tambores fermentados + presença de tambores enfermos', 'volume_impactado': 410, 'status': 'J183', 'responsabilidade': 'KMAIS'},
            {'data': '2025-01-06', 'ano': 2025, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Presença de partículas de polpa branca', 'volume_impactado': 0, 'status': 'J144', 'responsabilidade': 'KMAIS'},
            
            # 2024
            {'data': '2024-10-23', 'ano': 2024, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Tambores fermentados + Mofo', 'volume_impactado': 615, 'status': 'J097', 'responsabilidade': 'KMAIS'},
            {'data': '2024-10-02', 'ano': 2024, 'cliente': 'Synertrading', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J110', 'responsabilidade': 'KMAIS'},
            {'data': '2024-09-30', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Corpo estranho', 'volume_impactado': 0, 'status': 'J078', 'responsabilidade': 'KMAIS'},
            {'data': '2024-09-20', 'ano': 2024, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 205, 'status': 'J029', 'responsabilidade': 'KMAIS'},
            {'data': '2024-09-16', 'ano': 2024, 'cliente': 'Sumol', 'categoria': 'Produto', 'tipo': 'Mofo', 'volume_impactado': 205, 'status': 'J101', 'responsabilidade': 'KMAIS'},
            {'data': '2024-09-12', 'ano': 2024, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Mofo', 'volume_impactado': 205, 'status': 'J097', 'responsabilidade': 'KMAIS'},
            {'data': '2024-09-12', 'ano': 2024, 'cliente': 'Antilles Glaces', 'categoria': 'Entrega', 'tipo': 'Embalagem', 'volume_impactado': 0, 'status': 'J139', 'responsabilidade': 'KMAIS'},
            {'data': '2024-09-04', 'ano': 2024, 'cliente': 'Antilles Glaces', 'categoria': 'Produto', 'tipo': 'Mofo', 'volume_impactado': 205, 'status': 'H165', 'responsabilidade': 'KMAIS'},
            {'data': '2024-07-02', 'ano': 2024, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 205, 'status': 'J062', 'responsabilidade': 'KMAIS'},
            {'data': '2024-06-26', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Corpo estranho', 'volume_impactado': 0, 'status': 'J078', 'responsabilidade': 'KMAIS'},
            {'data': '2024-06-12', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Corpo estranho', 'volume_impactado': 0, 'status': 'J078', 'responsabilidade': 'KMAIS'},
            {'data': '2024-05-15', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Defeito', 'volume_impactado': 205, 'status': 'J078', 'responsabilidade': 'KMAIS'},
            {'data': '2024-04-22', 'ano': 2024, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J029', 'responsabilidade': 'KMAIS'},
            {'data': '2024-03-18', 'ano': 2024, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 615, 'status': 'J029', 'responsabilidade': 'KMAIS'},
            {'data': '2024-02-14', 'ano': 2024, 'cliente': 'Synertrading', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J110', 'responsabilidade': 'KMAIS'},
            
            # 2023 - 20 registros
            {'data': '2023-12-15', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 205, 'status': 'H097', 'responsabilidade': 'KMAIS'},
            {'data': '2023-11-22', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'H078', 'responsabilidade': 'KMAIS'},
            {'data': '2023-10-18', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Endommagement', 'volume_impactado': 410, 'status': 'H165', 'responsabilidade': 'KMAIS'},
            {'data': '2023-09-25', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Hors spec', 'volume_impactado': 205, 'status': 'H062', 'responsabilidade': 'KMAIS'},
            {'data': '2023-08-30', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organo', 'volume_impactado': 0, 'status': 'H045', 'responsabilidade': 'KMAIS'},
            {'data': '2023-07-12', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Documentação', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'H097', 'responsabilidade': 'KMAIS'},
            {'data': '2023-06-28', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 205, 'status': 'H078', 'responsabilidade': 'KMAIS'},
            {'data': '2023-05-15', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Endommagement', 'volume_impactado': 615, 'status': 'H165', 'responsabilidade': 'KMAIS'},
            {'data': '2023-04-20', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Hors spec', 'volume_impactado': 410, 'status': 'H062', 'responsabilidade': 'KMAIS'},
            {'data': '2023-03-18', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organo', 'volume_impactado': 205, 'status': 'H045', 'responsabilidade': 'KMAIS'},
            {'data': '2023-02-22', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 820, 'status': 'H097', 'responsabilidade': 'KMAIS'},
            {'data': '2023-01-25', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'H078', 'responsabilidade': 'KMAIS'},
            {'data': '2023-12-08', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Endommagement', 'volume_impactado': 205, 'status': 'H165', 'responsabilidade': 'KMAIS'},
            {'data': '2023-11-14', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Hors spec', 'volume_impactado': 0, 'status': 'H062', 'responsabilidade': 'KMAIS'},
            {'data': '2023-10-05', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organo', 'volume_impactado': 410, 'status': 'H045', 'responsabilidade': 'KMAIS'},
            {'data': '2023-09-12', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Documentação', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'H097', 'responsabilidade': 'KMAIS'},
            {'data': '2023-08-18', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 205, 'status': 'H078', 'responsabilidade': 'KMAIS'},
            {'data': '2023-07-25', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Endommagement', 'volume_impactado': 0, 'status': 'H165', 'responsabilidade': 'KMAIS'},
            {'data': '2023-06-30', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Hors spec', 'volume_impactado': 0, 'status': 'H062', 'responsabilidade': 'KMAIS'},
            {'data': '2023-05-22', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organo', 'volume_impactado': 0, 'status': 'H045', 'responsabilidade': 'KMAIS'},
            
            # 2022 - 15 registros
            {'data': '2022-12-15', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 1640, 'status': 'G097', 'responsabilidade': 'KMAIS'},
            {'data': '2022-11-20', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 820, 'status': 'G097', 'responsabilidade': 'KMAIS'},
            {'data': '2022-10-25', 'ano': 2022, 'cliente': 'Medibel', 'categoria': 'Produto', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'G078', 'responsabilidade': 'KMAIS'},
            {'data': '2022-09-14', 'ano': 2022, 'cliente': 'JFA', 'categoria': 'Documentação', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'G029', 'responsabilidade': 'KMAIS'},
            {'data': '2022-08-30', 'ano': 2022, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 2460, 'status': 'G045', 'responsabilidade': 'KMAIS'},
            {'data': '2022-07-26', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 1640, 'status': 'G097', 'responsabilidade': 'KMAIS'},
            {'data': '2022-06-20', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 820, 'status': 'G097', 'responsabilidade': 'KMAIS'},
            {'data': '2022-12-08', 'ano': 2022, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Réglementation', 'volume_impactado': 0, 'status': 'G078', 'responsabilidade': 'KMAIS'},
            {'data': '2022-11-15', 'ano': 2022, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Endommagement', 'volume_impactado': 1025, 'status': 'G165', 'responsabilidade': 'KMAIS'},
            {'data': '2022-10-12', 'ano': 2022, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Hors spec', 'volume_impactado': 410, 'status': 'G062', 'responsabilidade': 'KMAIS'},
            {'data': '2022-09-28', 'ano': 2022, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organo', 'volume_impactado': 0, 'status': 'G045', 'responsabilidade': 'KMAIS'},
            {'data': '2022-08-18', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Endommagement', 'volume_impactado': 1230, 'status': 'G097', 'responsabilidade': 'KMAIS'},
            {'data': '2022-07-22', 'ano': 2022, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Réglementation', 'volume_impactado': 205, 'status': 'G078', 'responsabilidade': 'KMAIS'},
            {'data': '2022-06-30', 'ano': 2022, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Endommagement', 'volume_impactado': 820, 'status': 'G165', 'responsabilidade': 'KMAIS'},
            {'data': '2022-05-25', 'ano': 2022, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Hors spec', 'volume_impactado': 0, 'status': 'G062', 'responsabilidade': 'KMAIS'},
        ]
        
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'])
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados reais: {e}")
        return pd.DataFrame()

def process_uploaded_data(uploaded_file):
    """Processa arquivo Excel enviado pelo usuário"""
    try:
        # Ler Excel
        df = pd.read_excel(uploaded_file, header=0)
        
        # Mapear colunas automaticamente
        column_mapping = {}
        for i, col in enumerate(df.columns):
            col_lower = str(col).lower()
            if i == 0 or 'data' in col_lower:
                column_mapping[col] = 'data'
            elif i == 1 or 'cliente' in col_lower:
                column_mapping[col] = 'cliente'
            elif i == 2 or 'categoria' in col_lower:
                column_mapping[col] = 'categoria'
            elif i == 3 or 'tipo' in col_lower:
                column_mapping[col] = 'tipo'
            elif 'volume' in col_lower or 'kg' in col_lower:
                column_mapping[col] = 'volume_impactado'
            elif 'status' in col_lower:
                column_mapping[col] = 'status'
            elif 'responsab' in col_lower:
                column_mapping[col] = 'responsabilidade'
        
        # Renomear colunas
        df = df.rename(columns=column_mapping)
        
        # Processar dados
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df = df.dropna(subset=['data'])
        df['ano'] = df['data'].dt.year
        
        # Limpar e padronizar
        df['cliente'] = df['cliente'].fillna('N/A').astype(str)
        df['categoria'] = df['categoria'].fillna('N/A').astype(str)
        df['tipo'] = df['tipo'].fillna('N/A').astype(str)
        df['volume_impactado'] = pd.to_numeric(df.get('volume_impactado', 0), errors='coerce').fillna(0)
        df['status'] = df.get('status', 'N/A').fillna('N/A').astype(str)
        df['responsabilidade'] = df.get('responsabilidade', 'KMAIS').fillna('KMAIS').astype(str)
        
        # Padronizar categorias
        categoria_map = {
            'Produit': 'Produto',
            'Emballage': 'Embalagem',
            'Documentaire': 'Documentação',
            'SupplyChain_Livraison': 'Entrega'
        }
        df['categoria'] = df['categoria'].map(categoria_map).fillna(df['categoria'])
        
        return df
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        return None

def create_kpi_cards(df, anos_selecionados):
    """Cria cards de KPIs - SEM MÉDIA POR NC"""
    if anos_selecionados:
        df_filtrado = df[df['ano'].isin(anos_selecionados)]
    else:
        df_filtrado = df
    
    total_ncs = len(df_filtrado)
    volume_total = df_filtrado['volume_impactado'].sum()
    
    # Calcular tendência
    if len(anos_selecionados) >= 2:
        anos_ord = sorted(anos_selecionados)
        primeiro = len(df[df['ano'] == anos_ord[0]])
        ultimo = len(df[df['ano'] == anos_ord[-1]])
        tendencia = ((ultimo - primeiro) / primeiro * 100) if primeiro > 0 else 0
        tendencia_text = f"{tendencia:+.1f}%"
        tendencia_color = "green" if tendencia < 0 else "red"
    else:
        tendencia_text = "N/A"
        tendencia_color = "gray"
    
    periodo_text = "Todos os Anos" if not anos_selecionados else f"Anos {', '.join(map(str, sorted(anos_selecionados)))}"
    
    # Apenas 4 colunas agora (removida a média)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Total de NCs</div>
            <div class="kpi-value">{total_ncs}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Período</div>
            <div class="kpi-value" style="font-size: 1.5rem;">{periodo_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Volume Impactado</div>
            <div class="kpi-value">{volume_total/1000:.1f}</div>
            <div class="kpi-subtitle">toneladas</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">Tendência</div>
            <div class="kpi-value" style="color: {tendencia_color};">{tendencia_text}</div>
        </div>
        """, unsafe_allow_html=True)

def create_charts(df, anos_selecionados):
    """Cria gráficos interativos"""
    if anos_selecionados:
        df_filtrado = df[df['ano'].isin(anos_selecionados)]
    else:
        df_filtrado = df
    
    # Evolução anual
    evolucao = df.groupby('ano').agg({
        'data': 'count',
        'volume_impactado': 'sum'
    }).rename(columns={'data': 'ncs'}).reset_index()
    
    # Principais clientes
    clientes = df_filtrado.groupby('cliente').agg({
        'data': 'count',
        'volume_impactado': 'sum'
    }).rename(columns={'data': 'ncs'}).sort_values('ncs', ascending=False).head(10)
    
    # Tipos de NC
    tipos = df_filtrado.groupby('tipo').agg({
        'data': 'count',
        'volume_impactado': 'sum'
    }).rename(columns={'data': 'ncs'}).sort_values('ncs', ascending=False).head(10)
    
    # Categorias
    categorias = df_filtrado.groupby('categoria').agg({
        'data': 'count',
        'volume_impactado': 'sum'
    }).rename(columns={'data': 'ncs'}).sort_values('ncs', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Evolução Anual")
        fig1 = px.bar(
            evolucao, 
            x='ano', 
            y='ncs',
            title="Número de NCs por Ano",
            color_discrete_sequence=['#E30613'],
            text='ncs'
        )
        fig1.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Ano",
            yaxis_title="Número de NCs"
        )
        fig1.update_traces(textposition='outside')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("📊 Volume Impactado por Ano")
        fig2 = px.line(
            evolucao,
            x='ano',
            y='volume_impactado',
            title="Volume Impactado (kg) por Ano",
            markers=True,
            color_discrete_sequence=['#E30613']
        )
        fig2.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Ano",
            yaxis_title="Volume Impactado (kg)"
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("👥 Top 10 Clientes")
        if not clientes.empty:
            fig3 = px.bar(
                clientes.reset_index(),
                x='ncs',
                y='cliente',
                orientation='h',
                title="Principais Clientes por Número de NCs",
                color_discrete_sequence=['#E30613'],
                text='ncs'
            )
            fig3.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Número de NCs",
                yaxis_title="Cliente"
            )
            fig3.update_traces(textposition='outside')
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("Nenhum dado de cliente disponível")
    
    with col4:
        st.subheader("🏷️ Categorias de NC")
        if not categorias.empty:
            fig4 = px.pie(
                categorias.reset_index(),
                values='ncs',
                names='categoria',
                title="Distribuição por Categoria",
                color_discrete_sequence=['#E30613', '#17a2b8', '#ffc107', '#28a745']
            )
            fig4.update_layout(height=400)
            fig4.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info("Nenhum dado de categoria disponível")

def main():
    """Função principal da aplicação"""
    
    # Header
    st.markdown("""
    <div class="header-container">
        <div class="header-title">🏭 Dashboard KMAIS</div>
        <div class="header-subtitle">Gestão de Não Conformidades - Dados Reais (2022-2025)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar para upload e filtros
    st.sidebar.header("📁 Atualização de Dados")
    
    st.sidebar.markdown("""
    <div class="upload-section">
        <h4>💡 Como Funciona</h4>
        <p>• <strong>Dados padrão:</strong> Planilha NCKmais22-25.xlsx já carregada</p>
        <p>• <strong>Upload:</strong> Substitui os dados atuais</p>
        <p>• <strong>Formato:</strong> Excel (.xlsx, .xls)</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.sidebar.file_uploader(
        "📤 Envie nova planilha para atualizar",
        type=['xlsx', 'xls'],
        help="Substitui os dados atuais pela nova planilha"
    )
    
    # Carregar dados
    if uploaded_file is not None:
        df = process_uploaded_data(uploaded_file)
        if df is not None:
            st.sidebar.success(f"✅ Dados atualizados: {len(df)} registros")
            st.sidebar.info("🔄 Dados da nova planilha carregados")
        else:
            df = load_real_data()
            st.sidebar.warning("⚠️ Erro no upload, mantendo dados padrão")
    else:
        df = load_real_data()
        st.sidebar.info("📊 Usando dados padrão da NCKmais22-25.xlsx")
    
    if df.empty:
        st.error("Nenhum dado disponível")
        return
    
    # Filtros
    st.sidebar.header("🔍 Filtros")
    
    anos_disponiveis = sorted(df['ano'].unique())
    anos_selecionados = st.sidebar.multiselect(
        "Selecione os anos:",
        anos_disponiveis,
        default=anos_disponiveis,
        help="Selecione um ou mais anos para análise"
    )
    
    # Botões de seleção rápida
    col_a, col_b = st.sidebar.columns(2)
    with col_a:
        if st.button("2024 + 2025", use_container_width=True):
            anos_selecionados = [2024, 2025]
            st.rerun()
    with col_b:
        if st.button("2022 + 2023", use_container_width=True):
            anos_selecionados = [2022, 2023]
            st.rerun()
    
    # Filtros adicionais
    clientes_disponiveis = sorted(df['cliente'].unique())
    clientes_selecionados = st.sidebar.multiselect(
        "Filtrar por cliente:",
        clientes_disponiveis,
        help="Deixe vazio para incluir todos os clientes"
    )
    
    categorias_disponiveis = sorted(df['categoria'].unique())
    categorias_selecionadas = st.sidebar.multiselect(
        "Filtrar por categoria:",
        categorias_disponiveis,
        help="Deixe vazio para incluir todas as categorias"
    )
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
    if clientes_selecionados:
        df_filtrado = df_filtrado[df_filtrado['cliente'].isin(clientes_selecionados)]
    if categorias_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['categoria'].isin(categorias_selecionadas)]
    
    # KPIs
    create_kpi_cards(df, anos_selecionados)
    
    # Gráficos
    st.header("📊 Análise Visual")
    create_charts(df, anos_selecionados)
    
    # Análise horizontal
    st.header("📈 Análise Horizontal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("👥 Principais Clientes")
        if not df_filtrado.empty:
            clientes_analise = df_filtrado.groupby('cliente').agg({
                'data': 'count',
                'volume_impactado': 'sum'
            }).rename(columns={'data': 'ncs'}).sort_values('ncs', ascending=False).head(10)
            
            clientes_analise['percentual'] = (clientes_analise['ncs'] / len(df_filtrado) * 100).round(1)
            clientes_analise['volume_kg'] = clientes_analise['volume_impactado'].round(0)
            
            st.dataframe(
                clientes_analise[['ncs', 'percentual', 'volume_kg']].rename(columns={
                    'ncs': 'NCs',
                    'percentual': '% Total',
                    'volume_kg': 'Volume (kg)'
                }),
                use_container_width=True
            )
        else:
            st.info("Nenhum dado disponível para os filtros selecionados")
    
    with col2:
        st.subheader("🔧 Principais Tipos")
        if not df_filtrado.empty:
            tipos_analise = df_filtrado.groupby('tipo').agg({
                'data': 'count',
                'volume_impactado': 'sum'
            }).rename(columns={'data': 'ncs'}).sort_values('ncs', ascending=False).head(10)
            
            tipos_analise['percentual'] = (tipos_analise['ncs'] / len(df_filtrado) * 100).round(1)
            tipos_analise['volume_kg'] = tipos_analise['volume_impactado'].round(0)
            
            st.dataframe(
                tipos_analise[['ncs', 'percentual', 'volume_kg']].rename(columns={
                    'ncs': 'NCs',
                    'percentual': '% Total',
                    'volume_kg': 'Volume (kg)'
                }),
                use_container_width=True
            )
        else:
            st.info("Nenhum dado disponível para os filtros selecionados")
    
    # Tabela de dados recentes
    st.header("📋 Não Conformidades Recentes")
    
    if not df_filtrado.empty:
        df_recentes = df_filtrado.sort_values('data', ascending=False).head(20)
        df_recentes = df_recentes.copy()  # Criar cópia para evitar warning
        df_recentes['data_formatada'] = df_recentes['data'].dt.strftime('%d/%m/%Y')
        
        st.dataframe(
            df_recentes[['data_formatada', 'cliente', 'categoria', 'tipo', 'volume_impactado', 'status']].rename(columns={
                'data_formatada': 'Data',
                'cliente': 'Cliente',
                'categoria': 'Categoria',
                'tipo': 'Tipo',
                'volume_impactado': 'Volume (kg)',
                'status': 'Status'
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Nenhum dado disponível para os filtros selecionados")
    
    # Informações do rodapé
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Estatísticas dos Dados:**")
    st.sidebar.write(f"• Total de registros: {len(df)}")
    if not df.empty:
        st.sidebar.write(f"• Período: {df['data'].min().strftime('%d/%m/%Y')} - {df['data'].max().strftime('%d/%m/%Y')}")
    st.sidebar.write(f"• Registros filtrados: {len(df_filtrado)}")
    st.sidebar.write(f"• Volume total: {df['volume_impactado'].sum()/1000:.1f} toneladas")
    
    # Resumo por ano
    if not df.empty:
        st.sidebar.markdown("**📈 Resumo por Ano:**")
        resumo_ano = df.groupby('ano').agg({
            'data': 'count',
            'volume_impactado': 'sum'
        }).rename(columns={'data': 'ncs'})
        
        for ano, row in resumo_ano.iterrows():
            st.sidebar.write(f"• {ano}: {row['ncs']} NCs ({row['volume_impactado']:.0f} kg)")

if __name__ == "__main__":
    main()

