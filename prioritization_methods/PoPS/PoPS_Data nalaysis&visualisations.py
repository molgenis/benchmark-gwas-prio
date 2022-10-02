# %%
import pandas as pd
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np

# %% [markdown]
# ## height dataset from pops paper

# %%

df = pd.read_csv("D:\Public_PoPS_data\PoPS_FullResults.txt", sep = "\t")

# %%
df

# %%
# we only analyse the breaker fruits
df_height = df[df['trait'].str.contains('Height')]
df_height

# %%
h_paper = df_height.sort_values(by = 'pops_score', ascending = False)

# %%
h_paper

# %%
h_paper = h_paper.iloc[:500, :]
h_paper


# %%
#data.set_index('ensgid', inplace=True)

# %%
#data.head(5)

# %% [markdown]
# ## height dataset from combined features

# %%
h_combined = pd.read_csv("C:\\Users\\Gebruiker\\OneDrive\\Documents\\DSLS\\integrated_omics\\project\\POPS\\new_run_height\\output\\gene_output_height.preds", sep = '\t')
h_combined

# %%
h_combined = h_combined.sort_values(by = 'PoPS_Score', ascending = False)
h_combined

# %%
h_combined = h_combined.iloc[:500]
h_combined

# %% [markdown]
# ## compare result of pops paper with result of combined features

# %%
h_paper.ensgid.isin(h_combined.ENSGID).sum()

# %%
h_paper_h_combined = h_paper.ensgid[ h_paper.ensgid.isin(h_combined.ENSGID)].values

# %%
h_combined_data = h_combined[h_combined.ENSGID.isin(h_paper_h_combined )][["ENSGID", "PoPS_Score"]]
h_combined_data

# %%
h_combined_data = h_combined_data.sort_values(by = 'ENSGID', ascending = False)
h_combined_data

# %%
h_paper_data = h_paper[h_paper.ensgid.isin(h_paper_h_combined )][["ensgid", "pops_score"]]
h_paper_data

# %%
h_paper_data = h_paper_data.sort_values(by = 'ensgid', ascending = False)
h_paper_data

# %%
x = h_paper_data['pops_score']
y = h_combined_data["PoPS_Score"]

plt.scatter(x, y)
diag_line, = plt.plot(plt.xlim(), plt.ylim(), ls="--", c=".3")
print(np.corrcoef(x=x, y=y)[0, 1])

plt.show()

# %%
corr, _ = pearsonr(x, y)
corr

# %%
#h_combined_ids = h_combined.ENSGID.values
#h_combined_ids

# %%
overlapping_genes_data = data[data.index.isin(h_combined_ids)]
#print(overlapping_genes.index)
overlapping_genes = overlapping_genes_data.index
total_overlap = overlapping_genes.shape[0]
print(f"Number of overlapping genes: {total_overlap}")

# %% [markdown]
# ## height dataset combined three features

# %%
h_combined3 = pd.read_csv("C:\\Users\\Gebruiker\\OneDrive\\Documents\\DSLS\\integrated_omics\\project\\POPS\\height_combined_three_tissues\\gene_output_height.preds", sep = '\t')

# %%
h_combined3

# %%
h_combined3 = h_combined3.sort_values(by = 'PoPS_Score', ascending = False)
h_combined3

# %%
h_combined3 = h_combined3.iloc[:500]
h_combined3.head(5)

# %%
h_combined3_ids = h_combined.ENSGID.values
h_combined3_ids

# %%
#overlap of genes from combined data frame with three tissues with result of paper
overlapping_genes_data3 = data[data.index.isin(h_combined3_ids)]
#print(overlapping_genes.index)
overlapping_genes3 = overlapping_genes_data3.index
total_overlap = overlapping_genes3.shape[0]
print(f"Number of overlapping genes: {total_overlap}")

# %% [markdown]
# ## compare the results of selecting three features only, with selecting combined all features

# %%
combined3_combined = h_combined3.ENSGID[ h_combined3.ENSGID.isin(h_combined.ENSGID)].values

# %%
combined3_combined = h_combined3.ENSGID[ h_combined3.ENSGID.isin(h_combined.ENSGID)].values
h_combined3_data = h_combined3[h_combined3.ENSGID.isin(combined3_combined)][["ENSGID", "PoPS_Score"]]
h_combined3_data

# %%
h_combined3_data = h_combined3_data.sort_values(by = 'ENSGID', ascending = False)
h_combined3_data

# %%
h_combined_data = h_combined[h_combined.ENSGID.isin(combined3_combined)][["ENSGID", "PoPS_Score"]]
h_combined_data

# %%
h_combined_data = h_combined_data.sort_values(by = 'ENSGID', ascending = False)
h_combined_data

# %%
x = h_combined3_data['PoPS_Score']
y = h_combined_data["PoPS_Score"]

plt.scatter(x, y)
diag_line, = plt.plot(plt.xlim(), plt.ylim(), ls="--", c=".3")
print(np.corrcoef(x=x, y=y)[0, 1])

plt.show()

# %%
from scipy.stats import pearsonr
import matplotlib.pyplot as plt
import numpy as np
 
corr, _ = pearsonr(x, y)
corr

# %% [markdown]
# ## height dataset from one gene feature folder(human bone marrow)

# %%
h_hbn = pd.read_csv("C:\\Users\\Gebruiker\\OneDrive\\Documents\\DSLS\\integrated_omics\\project\\POPS\\step2\\out_hbn_height\\500_genes_priortised_height.txt", sep = '\t')
h_hbn

# %% [markdown]
# ## compare the result of one feature(hbn) with combined all features 

# %%
h_hbn_combined = h_hbn.ENSGID[ h_hbn.ENSGID.isin(h_combined.ENSGID)].values

# %%
h_hbn_data = h_hbn[h_hbn.ENSGID.isin(h_hbn_combined)][["ENSGID", "PoPS_Score"]]
h_hbn_data

# %%
h_hbn_data = h_hbn_data.sort_values(by = 'ENSGID', ascending = False)
h_hbn_data

# %%
h_combined_data = h_combined[h_combined.ENSGID.isin(h_hbn_combined)][["ENSGID", "PoPS_Score"]]
h_combined_data

# %%
h_combined_data = h_combined_data.sort_values(by = 'ENSGID', ascending = False)
h_combined_data

# %%
x = h_hbn_data['PoPS_Score']
y = h_combined_data["PoPS_Score"]

plt.scatter(x, y)
diag_line, = plt.plot(plt.xlim(), plt.ylim(), ls="--", c=".3")
print(np.corrcoef(x=x, y=y)[0, 1])

plt.show()

# %%
corr, _ = pearsonr(x, y)
corr


