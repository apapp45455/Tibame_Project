import pandas as pd
import numpy as np
import scipy.sparse as sparse
from sklearn import metrics
from sklearn.preprocessing import MinMaxScaler
import implicit
import json

sales_df = pd.read_csv('./sales4.csv')
product_df = pd.read_csv('./product.csv')
retail_df = pd.merge(sales_df, product_df, on='product_id', how='outer')

# grouped_df = retail_df[['customer_id', 'product_id', 'quantity','product_name']].groupby(['customer_id', 'product_id']).sum().reset_index()
grouped_df = retail_df[['customer_id', 'product_id', 'quantity', 'product_name']].groupby(['customer_id', 'product_id','product_name'], as_index=False)['quantity'].sum()

# 編碼
unique_customers = grouped_df.customer_id.unique()
customer_ids = dict(zip(unique_customers, np.arange(unique_customers.shape[0], dtype=np.int32)))
unique_items = grouped_df.product_id.unique()
item_ids = dict(zip(unique_items, np.arange(unique_items.shape[0], dtype=np.int32)))

grouped_df['Customer'] = grouped_df.customer_id.apply(lambda i: customer_ids[i])
grouped_df['Item'] = grouped_df.product_id.apply(lambda i: item_ids[i])

#製作稀疏矩陣
sparse_item_customer = sparse.csr_matrix((grouped_df['quantity'].astype(float), (grouped_df['Item'], grouped_df['Customer'])))
sparse_customer_item = sparse.csr_matrix((grouped_df['quantity'].astype(float), (grouped_df['Customer'], grouped_df['Item'])))

# 訓練
alpha = 40
data = (sparse_item_customer * alpha).astype('double')
model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.1, iterations=20)
model.fit(data)


def recommend(Customer, sparse_customer_item, customer_vecs, item_vecs, num_items=5):
    
    customer_interactions = sparse_customer_item[Customer,:].toarray()
    customer_interactions = customer_interactions.reshape(-1) + 1
    customer_interactions[customer_interactions > 1] = 0
    
    rec_vector = (customer_vecs[Customer,:].dot(item_vecs.T)).toarray()
    
    min_max = MinMaxScaler()
    rec_vector_scaled = min_max.fit_transform(rec_vector.reshape(-1,1))[:,0]
    recommend_vector = customer_interactions * rec_vector_scaled

    Item_idx = np.argsort(recommend_vector)[::-1][:num_items]
    
    product_list = []

    for idx in Item_idx:
        product = grouped_df.product_name.loc[grouped_df.Item == idx].iloc[0]
        product_list.append(product)

    recommendations = product_list

    return recommendations

item_vecs = sparse.csr_matrix(model.user_factors)
customer_vecs = sparse.csr_matrix(model.item_factors)

# recommendations = recommend(Customer, sparse_customer_item, customer_vecs, item_vecs)
customer_list = sorted(retail_df.customer_id.unique().tolist())
all_recommend = []

for Customer, customer_id in enumerate(customer_list):
    recommendations = recommend(Customer, sparse_customer_item, customer_vecs, item_vecs)
    customer_dict = {}
    customer = {}
    customer[customer_id] = recommendations
    customer_dict['customer_id'] = str(customer_id)
    customer_dict['recommendations'] = customer
    all_recommend.append(customer_dict)

# print(all_recommend)
with open('recommendation_total.json', 'w') as f:
    json.dump(all_recommend, f)

