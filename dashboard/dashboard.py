import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data
all_data = pd.read_csv("dashboard/main_data.csv")

# Pastikan kolom tanggal bertipe datetime
datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
for col in datetime_columns:
    all_data[col] = pd.to_datetime(all_data[col])

# ==============================
# Judul Dashboard
# ==============================
st.title('E-Commerce Public Dashboard 🛒')

# ==============================
# Visualisasi 1: Kategori Produk
# ==============================
st.subheader("Kinerja Pendapatan Kategori Produk (2018)")

sales_2018 = all_data[all_data['order_purchase_timestamp'].dt.year == 2018]
revenue_per_category_2018 = sales_2018.groupby('product_category_name_english')['price'].sum().reset_index()
revenue_sorted = revenue_per_category_2018.sort_values(by='price', ascending=False)

fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
colors_top = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
colors_bottom = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#ff6f69"]

sns.barplot(x="price", y="product_category_name_english", data=revenue_sorted.head(5), palette=colors_top, ax=ax1[0])
ax1[0].set_ylabel(None)
ax1[0].set_xlabel("Total Revenue", fontsize=12)
ax1[0].set_title("Pendapatan Tertinggi (2018)", loc="center", fontsize=15)
ax1[0].tick_params(axis ='y', labelsize=12)

sns.barplot(x="price", y="product_category_name_english", data=revenue_sorted.tail(5).sort_values(by="price", ascending=True), palette=colors_bottom, ax=ax1[1])
ax1[1].set_ylabel(None)
ax1[1].set_xlabel("Total Revenue", fontsize=12)
ax1[1].invert_xaxis()
ax1[1].yaxis.set_label_position("right")
ax1[1].yaxis.tick_right()
ax1[1].set_title("Pendapatan Terendah (2018)", loc="center", fontsize=15)
ax1[1].tick_params(axis='y', labelsize=12)

st.pyplot(fig1)
st.write("**Insight:** Kategori *Health & Beauty* menjadi penyumbang pendapatan terbesar di tahun 2018.")

# ==============================
# Visualisasi 2: Keterlambatan Pengiriman
# ==============================
st.subheader("Persentase Keterlambatan Pengiriman (Q4 2017)")

q4_2017_data = all_data[(all_data['order_purchase_timestamp'] >= '2017-10-01') &
                        (all_data['order_purchase_timestamp'] <= '2017-12-31')].copy()
q4_2017_data = q4_2017_data.drop_duplicates(subset='order_id')
q4_2017_data['is_late'] = q4_2017_data['order_delivered_customer_date'] > q4_2017_data['order_estimated_delivery_date']

total_orders = len(q4_2017_data)
late_orders = q4_2017_data['is_late'].sum()

labels = ['Tepat Waktu / Lebih Cepat', 'Terlambat']
sizes = [total_orders - late_orders, late_orders]
colors = ['#72BCD4', '#ff6f69']
explode = (0, 0.1) 

fig2, ax2 = plt.subplots(figsize=(6, 4))
ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%',
        shadow=False, startangle=90, textprops={'fontsize': 12})
ax2.axis('equal') 

st.pyplot(fig2)
st.write("**Insight:** Terdapat keterlambatan pengiriman pesanan pada periode akhir tahun 2017, hal ini perlu menjadi bahan evaluasi untuk logistik.")

st.caption('Copyright (c) Muhammad Surya Ibrahim 2026')
