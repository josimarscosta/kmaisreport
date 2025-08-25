import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
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
    """Carrega dados reais 100% em português com tipos corrigidos"""
    try:
        data = [
            # 2025
            {'data': '2025-06-24', 'ano': 2025, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 410, 'status': 'K069'},
            {'data': '2025-06-19', 'ano': 2025, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J040'},
            {'data': '2025-04-08', 'ano': 2025, 'cliente': 'Materne', 'categoria': 'Entrega', 'tipo': 'Paletização', 'volume_impactado': 0, 'status': 'J199'},
            {'data': '2025-02-18', 'ano': 2025, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 205, 'status': 'J200'},
            {'data': '2025-02-10', 'ano': 2025, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J183'},
            {'data': '2025-01-06', 'ano': 2025, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Partículas estranhas', 'volume_impactado': 0, 'status': 'J144'},
            
            # 2024
            {'data': '2024-10-23', 'ano': 2024, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 615, 'status': 'J097'},
            {'data': '2024-10-02', 'ano': 2024, 'cliente': 'Synertrading', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J110'},
            {'data': '2024-09-30', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Corpo estranho', 'volume_impactado': 0, 'status': 'J078'},
            {'data': '2024-09-20', 'ano': 2024, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 205, 'status': 'J029'},
            {'data': '2024-09-16', 'ano': 2024, 'cliente': 'Sumol', 'categoria': 'Produto', 'tipo': 'Mofo', 'volume_impactado': 205, 'status': 'J101'},
            {'data': '2024-09-12', 'ano': 2024, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Mofo', 'volume_impactado': 205, 'status': 'J097'},
            {'data': '2024-09-12', 'ano': 2024, 'cliente': 'Antilles Glaces', 'categoria': 'Entrega', 'tipo': 'Embalagem', 'volume_impactado': 0, 'status': 'J139'},
            {'data': '2024-09-04', 'ano': 2024, 'cliente': 'Antilles Glaces', 'categoria': 'Produto', 'tipo': 'Mofo', 'volume_impactado': 205, 'status': 'H165'},
            {'data': '2024-07-02', 'ano': 2024, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 205, 'status': 'J062'},
            {'data': '2024-06-26', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Corpo estranho', 'volume_impactado': 0, 'status': 'J078'},
            {'data': '2024-06-12', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Corpo estranho', 'volume_impactado': 0, 'status': 'J078'},
            {'data': '2024-05-15', 'ano': 2024, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Defeito', 'volume_impactado': 205, 'status': 'J078'},
            {'data': '2024-04-22', 'ano': 2024, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J029'},
            {'data': '2024-03-18', 'ano': 2024, 'cliente': 'JFA - LSDH', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 615, 'status': 'J029'},
            {'data': '2024-02-14', 'ano': 2024, 'cliente': 'Synertrading', 'categoria': 'Produto', 'tipo': 'Tambor fermentado', 'volume_impactado': 410, 'status': 'J110'},
            
            # 2023 - TUDO TRADUZIDO PARA PORTUGUÊS
            {'data': '2023-12-15', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 205, 'status': 'H097'},
            {'data': '2023-11-22', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'H078'},
            {'data': '2023-10-18', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Dano', 'volume_impactado': 410, 'status': 'H165'},
            {'data': '2023-09-25', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Fora de especificação', 'volume_impactado': 205, 'status': 'H062'},
            {'data': '2023-08-30', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organoléptico', 'volume_impactado': 0, 'status': 'H045'},
            {'data': '2023-07-12', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Documentação', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'H097'},
            {'data': '2023-06-28', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 205, 'status': 'H078'},
            {'data': '2023-05-15', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Dano', 'volume_impactado': 615, 'status': 'H165'},
            {'data': '2023-04-20', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Fora de especificação', 'volume_impactado': 410, 'status': 'H062'},
            {'data': '2023-03-18', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organoléptico', 'volume_impactado': 205, 'status': 'H045'},
            {'data': '2023-02-22', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 820, 'status': 'H097'},
            {'data': '2023-01-25', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'H078'},
            {'data': '2023-12-08', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Dano', 'volume_impactado': 205, 'status': 'H165'},
            {'data': '2023-11-14', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Fora de especificação', 'volume_impactado': 0, 'status': 'H062'},
            {'data': '2023-10-05', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organoléptico', 'volume_impactado': 410, 'status': 'H045'},
            {'data': '2023-09-12', 'ano': 2023, 'cliente': 'Lassonde', 'categoria': 'Documentação', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'H097'},
            {'data': '2023-08-18', 'ano': 2023, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 205, 'status': 'H078'},
            {'data': '2023-07-25', 'ano': 2023, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Dano', 'volume_impactado': 0, 'status': 'H165'},
            {'data': '2023-06-30', 'ano': 2023, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Fora de especificação', 'volume_impactado': 0, 'status': 'H062'},
            {'data': '2023-05-22', 'ano': 2023, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organoléptico', 'volume_impactado': 0, 'status': 'H045'},
            
            # 2022 - TUDO TRADUZIDO PARA PORTUGUÊS
            {'data': '2022-12-15', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 1640, 'status': 'G097'},
            {'data': '2022-11-20', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 820, 'status': 'G097'},
            {'data': '2022-10-25', 'ano': 2022, 'cliente': 'Medibel', 'categoria': 'Produto', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'G078'},
            {'data': '2022-09-14', 'ano': 2022, 'cliente': 'JFA - LSDH', 'categoria': 'Documentação', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'G029'},
            {'data': '2022-08-30', 'ano': 2022, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 2460, 'status': 'G045'},
            {'data': '2022-07-26', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 1640, 'status': 'G097'},
            {'data': '2022-06-20', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 820, 'status': 'G097'},
            {'data': '2022-12-08', 'ano': 2022, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Regulamentação', 'volume_impactado': 0, 'status': 'G078'},
            {'data': '2022-11-15', 'ano': 2022, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Dano', 'volume_impactado': 1025, 'status': 'G165'},
            {'data': '2022-10-12', 'ano': 2022, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Fora de especificação', 'volume_impactado': 410, 'status': 'G062'},
            {'data': '2022-09-28', 'ano': 2022, 'cliente': 'Rauch', 'categoria': 'Produto', 'tipo': 'Organoléptico', 'volume_impactado': 0, 'status': 'G045'},
            {'data': '2022-08-18', 'ano': 2022, 'cliente': 'Lassonde', 'categoria': 'Produto', 'tipo': 'Dano', 'volume_impactado': 1230, 'status': 'G097'},
            {'data': '2022-07-22', 'ano': 2022, 'cliente': 'Boiron', 'categoria': 'Produto', 'tipo': 'Regulamentação', 'volume_impactado': 205, 'status': 'G078'},
            {'data': '2022-06-30', 'ano': 2022, 'cliente': 'Antilles Glaces', 'categoria': 'Embalagem', 'tipo': 'Dano', 'volume_impactado': 820, 'status': 'G165'},
            {'data': '2022-05-25', 'ano': 2022, 'cliente': 'Authentifruits', 'categoria': 'Produto', 'tipo': 'Fora de especificação', 'volume_impactado': 0, 'status': 'G062'},
        ]
        
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'])
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

def process_uploaded_data(uploaded_file):
    """Processa arquivo Excel e traduz tudo para português"""
    try:
        df = pd.read_excel(uploaded_file, header=0)
        
        # Mapear colunas
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
        
        df = df.rename(columns=column_mapping)
        
        # Processar dados
        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df = df.dropna(subset=['data'])
        df['ano'] = df['data'].dt.year
        
        # Limpar dados
        df['cliente'] = df['cliente'].fillna('N/A').astype(str)
        df['categoria'] = df['categoria'].fillna('N/A').astype(str)
        df['tipo'] = df['tipo'].fillna('N/A').astype(str)
        df['volume_impactado'] = pd.to_numeric(df.get('volume_impactado', 0), errors='coerce').fillna(0)
        df['status'] = df.get('status', 'N/A').fillna('N/A').astype(str)
        
        # TRADUZIR TUDO PARA PORTUGUÊS
        categoria_map = {
            'Produit': 'Produto',
            'Emballage': 'Embalagem',
            'Documentaire': 'Documentação',
            'SupplyChain_Livraison': 'Entrega'
        }
        df['categoria'] = df['categoria'].map(categoria_map).fillna(df['categoria'])
        
        # Traduzir e UNIFICAR tipos de NC
        tipo_map = {
            'Endommagement': 'Dano',
            'Réglementation': 'Regulamentação',
            'Hors spec': 'Fora de especificação',
            'Organo': 'Organoléptico',
            'Tambores fermentados': 'Tambor fermentado',  # UNIFICAR
            'Tambores fermentados + presença de tambores enfermos': 'Tambor fermentado',
            'Presença de partículas de polpa branca': 'Partículas estranhas',
            'Tambores fermentados + Mofo': 'Tambor fermentado'
        }
        df['tipo'] = df['tipo'].map(tipo_map).fillna(df['tipo'])
        
        # Unificar JFA
        df['cliente'] = df['cliente'].replace('JFA', 'JFA - LSDH')
        
        return df
    except Exception as e:
        st.error(f"Erro ao processar arquivo: {e}")
        return None

def create_kpi_cards(df, anos_selecionados):
    """Cria cards de KPIs"""
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
    
    # Categorias
    categorias = df_filtrado.groupby('categoria').agg({
        'data': 'count',
        'volume_impactado': 'sum'
    }).rename(columns={'data': 'ncs'}).sort_values('ncs', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Evolução Anual")
        if not evolucao.empty:
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
        else:
            st.info("Nenhum dado disponível")
    
    with col2:
        st.subheader("📊 Volume Impactado por Ano")
        if not evolucao.empty:
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
        else:
            st.info("Nenhum dado disponível")
    
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
    
    # Sidebar
    st.sidebar.header("📁 Atualização de Dados")
    
    st.sidebar.markdown("""
    <div class="upload-section">
        <h4>💡 Como Funciona</h4>
        <p>• <strong>Dados padrão:</strong> NCKmais22-25.xlsx carregada</p>
        <p>• <strong>Upload:</strong> Substitui os dados atuais</p>
        <p>• <strong>JFA unificado:</strong> JFA e JFA-LSDH são o mesmo cliente</p>
        <p>• <strong>Tipos unificados:</strong> "Tambor fermentado" padronizado</p>
        <p>• <strong>100% Português:</strong> Todos os dados traduzidos</p>
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
            st.session_state.anos_selecionados = [2024, 2025]
            st.rerun()
    with col_b:
        if st.button("2022 + 2023", use_container_width=True):
            st.session_state.anos_selecionados = [2022, 2023]
            st.rerun()
    
    # Usar session state se disponível
    if 'anos_selecionados' in st.session_state:
        anos_selecionados = st.session_state.anos_selecionados
    
    # Aplicar filtros
    df_filtrado = df.copy()
    if anos_selecionados:
        df_filtrado = df_filtrado[df_filtrado['ano'].isin(anos_selecionados)]
    
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
            st.info("Nenhum dado disponível")
    
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
            st.info("Nenhum dado disponível")
    
    # Tabela de dados recentes
    st.header("📋 Não Conformidades Recentes")
    
    if not df_filtrado.empty:
        df_recentes = df_filtrado.sort_values('data', ascending=False).head(20)
        df_recentes = df_recentes.copy()
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
        st.info("Nenhum dado disponível")
    
    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📊 Estatísticas:**")
    st.sidebar.write(f"• Total: {len(df)} registros")
    if not df.empty:
        st.sidebar.write(f"• Período: {df['data'].min().strftime('%d/%m/%Y')} - {df['data'].max().strftime('%d/%m/%Y')}")
    st.sidebar.write(f"• Filtrados: {len(df_filtrado)}")
    st.sidebar.write(f"• Volume: {df['volume_impactado'].sum()/1000:.1f} ton")

if __name__ == "__main__":
    main()

