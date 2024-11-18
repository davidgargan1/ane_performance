import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from src.data_processing import process_data, produce_total_df, produce_region_df
from src.plotting import total_attendances_graph, regional_performance_graph, trusts_performance_graph

df = process_data()
df = df.reset_index()

df_total = produce_total_df(df)
total_attendances_graph(df_total)

df_regions = produce_region_df(df)
regional_performance_graph(df_regions)

trusts_performance_graph(df)