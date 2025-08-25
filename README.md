# Dashboard KMAIS - Não Conformidades

Dashboard interativo para análise de não conformidades da KMAIS, desenvolvido com Streamlit.

## 🚀 Funcionalidades

- **Upload de Planilhas Excel**: Atualize os dados facilmente enviando uma nova planilha
- **Filtros Interativos**: Filtre por ano, cliente e categoria
- **Análise Visual**: Gráficos interativos com Plotly
- **Responsivo**: Funciona em desktop, tablet e mobile
- **KPIs Dinâmicos**: Indicadores que se atualizam conforme os filtros
- **Análise Horizontal**: Comparação entre períodos e categorias

## 📊 Estrutura dos Dados

A planilha Excel deve conter as seguintes colunas:

| Coluna | Descrição | Exemplo |
|--------|-----------|---------|
| Data | Data da não conformidade | 2024-06-15 |
| Cliente | Nome do cliente | Lassonde |
| Categoria | Categoria da NC | Produto |
| Tipo | Tipo específico da NC | Tambor fermentado |
| Volume Impactado | Volume em kg | 410 |
| Status | Status atual | J097 |

## 🛠️ Instalação Local

1. **Clone ou baixe o projeto**
```bash
git clone <repository-url>
cd dashboard_streamlit
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
streamlit run app.py
```

4. **Acesse no navegador**
```
http://localhost:8501
```

## 🌐 Deploy no Streamlit Cloud

1. **Faça upload dos arquivos para um repositório GitHub**

2. **Acesse [share.streamlit.io](https://share.streamlit.io)**

3. **Conecte seu repositório GitHub**

4. **Configure o deploy:**
   - Repository: `seu-usuario/dashboard-kmais`
   - Branch: `main`
   - Main file path: `app.py`

5. **Clique em "Deploy"**

## 📱 Responsividade

O dashboard foi desenvolvido com design responsivo:

- **Desktop**: Layout completo com 5 colunas de KPIs
- **Tablet**: Layout adaptado com 2-3 colunas
- **Mobile**: Layout em coluna única, otimizado para toque

## 🔄 Atualizando Dados

### Método 1: Upload na Interface
1. Acesse o dashboard
2. Use o sidebar "Upload de Dados"
3. Envie sua planilha Excel atualizada

### Método 2: Substituição no Repositório
1. Substitua o arquivo de dados no repositório
2. O Streamlit Cloud atualizará automaticamente

## 📈 Análises Disponíveis

- **Evolução Anual**: Número de NCs por ano
- **Volume Impactado**: Análise do impacto em kg/toneladas
- **Top Clientes**: Ranking de clientes com mais NCs
- **Categorias**: Distribuição por tipo de problema
- **Análise Horizontal**: Comparação entre períodos
- **Tendências**: Cálculo automático de variações

## 🎨 Personalização

### Cores da Marca KMAIS
- Vermelho principal: `#E30613`
- Vermelho secundário: `#C41E3A`
- Azul complementar: `#17a2b8`

### Modificando Gráficos
Os gráficos podem ser personalizados editando as funções em `app.py`:
- `create_charts()`: Gráficos principais
- `create_kpi_cards()`: Cards de KPIs

## 🐛 Solução de Problemas

### Erro no Upload
- Verifique se o arquivo é .xlsx ou .xls
- Confirme se as colunas estão nomeadas corretamente
- Verifique se há dados válidos nas linhas

### Gráficos não Carregam
- Verifique a conexão com internet
- Limpe o cache do navegador
- Recarregue a página

### Performance Lenta
- Reduza o número de registros na planilha
- Use filtros para limitar os dados exibidos

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação acima
2. Consulte os logs de erro no Streamlit
3. Entre em contato com o desenvolvedor

## 🔄 Versões

- **v1.0**: Versão inicial com funcionalidades básicas
- **v1.1**: Adicionado upload de planilhas
- **v1.2**: Melhorada responsividade mobile
- **v1.3**: Adicionados filtros avançados

