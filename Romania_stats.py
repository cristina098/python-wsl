# %%
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
# %%
fp = "ROU_adm/ROU_adm1.shp"
map_df = gpd.read_file(fp)
# check the GeoDataframe
#map_df.head()
# %%
#plt.rcParams['figure.figsize'] = [50, 70] #height, width
#map_df.plot()
# %%
judete = pd.read_csv("ROU_adm/ROU_judete.csv", sep=";")
#judete.head()
# %%
merged = map_df.merge(judete, how='left', left_on="NAME_1", right_on="province")
merged = merged[['province', 'geometry', 'population_2007', 'area_km2', 'municipalities', 'cities', 'comunes', 'villages']]
#merged.head()
# %%
variable = 'population_2007'
vmin, vmax = 100000, 2000000
fig, ax = plt.subplots(1, figsize=(30, 10))
ax.axis('off')
ax.set_title('Populatia Romaniei', fontdict={'fontsize': '25', 'fontweight' : '3'})

sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=0, vmax=vmax))# empty array for the data range
sm.set_array([]) 
fig.colorbar(sm)
#fig.colorbar(sm, orientation="horizontal", fraction=0.036, pad=0.1, aspect = 30)

merged.plot(column=variable, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
# %%

# %%
