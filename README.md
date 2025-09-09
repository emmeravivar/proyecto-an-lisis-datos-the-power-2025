Proyecto: EDA de E-commerce (Olist) + Power BI

Objetivo
- Explorar y analizar datos de e-commerce (Olist), unir una segunda fuente socioeconómica por estado y entregar un dashboard operativo en Power BI con un README reproducible.

Estructura
- data/raw/: datos en bruto (Olist + states.csv; se incluyen también hdi.csv, airports.csv, icu-beds.csv como extras no obligatorios).
- data/interim/: artefactos intermedios (order_items_join_orders.parquet, states_clean.csv|parquet).
- data/processed/: salidas finales (olist_final_dataset.csv y .xlsx con 50,000 filas). Al ejecutar 03–05 se crean subcarpetas eda/, stats/ y dash/.
- notebooks/: 01→05 pipeline completa.
- utils/: utilidades (etl_utils.py con days_diff y pct).
- dashboard/: PBIX del informe (Dahsboard_ok_ok - nuevo.pbix).

Requisitos y estado
- Dos datasets en bruto de fuentes distintas: CUMPLIDO. Olist + states.csv.
- Dataset final transformado: CUMPLIDO. olist_final_dataset.csv/.xlsx con exactamente 50,000 filas y 34 columnas (≥20).
- Análisis exhaustivo del dataset final: CUMPLIDO al ejecutar 03 (EDA) y 04 (estadística), que exportan a data/processed/eda/ y data/processed/stats/.
- Dashboard operativo (Power BI): CUMPLIDO. PBIX incluido; 05 (opcional) genera agregados en data/processed/dash/.
- Informe del análisis: CUMPLIDO en este README y desarrollado en los notebooks 03/04.
- Organización clara de carpetas: CUMPLIDO.

Cómo reproducir
1) Entorno
- Python 3.10+ recomendado.
- Instalar dependencias: pip install -r requirements.txt (en macOS, puedes usar requirements_mac.txt).

2) Orden de ejecución
- 01_carga_dataset.ipynb
  - Carga Olist (orders, items), verifica integridad y guarda data/interim/order_items_join_orders.parquet.
  - Limpia y exporta la segunda fuente a data/interim/states_clean.(csv|parquet) con las columnas: uf, region, population, poverty, demographic_density, gdp_per_capita.
- 02_limpieza_transformacion.ipynb
  - Une productos y sellers, crea variables derivadas (delivery_time_days, delay_vs_estimated_days, is_late, shipping_days_limit, purchase_year/month/day/weekday/hour, total_price, order_status_simple, order_line_uid).
  - Enriquecimiento por estado: join left seller_state ← uf con states_clean.
  - Exporta el dataset final limitando a exactamente 50,000 filas (muestra determinística):
    - data/processed/olist_final_dataset.csv
    - data/processed/olist_final_dataset.xlsx
- 03_eda_descriptivo.ipynb (opcional)
  - EDA del final; exporta a data/processed/eda/.
- 04_analisis_estadistico.ipynb (opcional)
  - Análisis estadístico; exporta a data/processed/stats/.
- 05_dashboard_powerbi_preparacion.ipynb (opcional)
  - Agregados para el dashboard: monthly_summary.csv, seller_summary.csv, product_summary.csv, status_summary.csv y state_demography_sellers.csv → data/processed/dash/.

3) Power BI
- Abre dashboard/Dahsboard_ok_ok - nuevo.pbix.
- Conecta la tabla principal a data/processed/olist_final_dataset.csv (o .xlsx).
- (Opcional) Conecta data/processed/dash/* si utilizas las tablas agregadas de 05.

Dataset final (resumen)
- Rutas: data/processed/olist_final_dataset.csv y .xlsx
- Tamaño: 50,000 filas (muestra determinística), 34 columnas.
- Campos clave:
  - Métricas/tiempos: total_price, delivery_time_days, delay_vs_estimated_days, is_late, shipping_days_limit.
  - Temporales: purchase_year, purchase_month, purchase_day, purchase_weekday, purchase_hour.
  - Logística/estado: order_status_simple, order_line_uid, seller_state, region, population, poverty, demographic_density, gdp_per_capita.

Medidas DAX sugeridas (Power BI)
- Total Revenue = SUM(Fact[total_price])
- Orders = DISTINCTCOUNT(Fact[order_id])
- Delivered Orders = CALCULATE([Orders], Fact[order_status_simple] = "delivered")
- On-Time Rate = 1 - AVERAGE(Fact[is_late])
- Late Rate = AVERAGE(Fact[is_late])
- Active Sellers = DISTINCTCOUNT(Fact[seller_id])
- Revenue per Seller = DIVIDE([Total Revenue], [Active Sellers])
- (Opcional con dimensión estado o dash) Sellers per 100k, Revenue per 100k usando population.

Notas de implementación
- La unión de la segunda fuente se hace en 02 usando data/interim/states_clean.(csv|parquet); el join conserva las filas y añade variables exógenas.
- 05 también consume states_clean para construir state_demography_sellers.csv; se corrigieron lecturas y renombres para evitar errores.
- utils/etl_utils.py aporta functions days_diff y pct usadas en 02.

Informe del análisis (resumen)
- Tendencias y estacionalidad: evolución mensual de pedidos e ingresos; base para KPIs temporales.
- Logística/on-time: tasa de puntualidad (is_late), tiempos de entrega y retrasos respecto a estimado.
- Contribuidores: top vendedores y productos por revenue (total_price).
- Contexto socioeconómico: segmentación por region/uf con población, pobreza, densidad y gdp_per_capita.

Limitaciones/consideraciones
- Los finales contienen una muestra de 50,000 filas (para requisito de tamaño); los resultados de 03/04/05 reflejarán esa cobertura.
- Si el entorno no tiene motor parquet, los notebooks hacen fallback a CSV para states_clean.

