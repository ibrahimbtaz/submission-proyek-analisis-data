import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

def create_revenue_category_df(df):
    revenue_df = df.groupby('product_category_name_english')['price'].sum().reset_index()
    revenue_sorted = revenue_df.sort_values(by='price', ascending=False)
    return revenue_sorted

def create_delivery_delay_df(df):
    df_unique = df.drop_duplicates(subset='order_id').copy()
    df_unique['is_late'] = df_unique['order_delivered_customer_date'] > df_unique['order_estimated_delivery_date']
    
    total_orders = len(df_unique)
    late_orders = df_unique['is_late'].sum()
    
    return total_orders, late_orders

all_data = pd.read_csv("dashboard/main_data.csv")

datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]
for col in datetime_columns:
    all_data[col] = pd.to_datetime(all_data[col])

all_data.sort_values(by="order_purchase_timestamp", inplace=True)
all_data.reset_index(drop=True, inplace=True)

min_date = all_data["order_purchase_timestamp"].min()
max_date = all_data["order_purchase_timestamp"].max()

with st.sidebar:
    # st.image("")
    st.title("🛒 E-Commerce Filter")
    
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

if len(date_range) == 2:
    start_date, end_date = date_range
elif len(date_range) == 1:
    start_date = date_range[0]
    end_date = date_range[0]
else:
    start_date = min_date
    end_date = max_date

main_df = all_data[(all_data["order_purchase_timestamp"] >= str(start_date)) & 
                   (all_data["order_purchase_timestamp"] <= str(end_date))]

revenue_sorted = create_revenue_category_df(main_df)
total_orders, late_orders = create_delivery_delay_df(main_df)

st.header('E-Commerce Public Dashboard 📊')

st.subheader("Kinerja Pendapatan Kategori Produk")

if not revenue_sorted.empty:
    fig1, ax1 = plt.subplots(nrows=1, ncols=2, figsize=(24, 6))
    colors_top = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    colors_bottom = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#ff6f69"]

    sns.barplot(x="price", y="product_category_name_english", data=revenue_sorted.head(5), palette=colors_top, ax=ax1[0])
    ax1[0].set_ylabel(None)
    ax1[0].set_xlabel("Total Revenue", fontsize=12)
    ax1[0].set_title("5 Pendapatan Tertinggi", loc="center", fontsize=15)
    ax1[0].tick_params(axis ='y', labelsize=12)

    sns.barplot(x="price", y="product_category_name_english", data=revenue_sorted.tail(5).sort_values(by="price", ascending=True), palette=colors_bottom, ax=ax1[1])
    ax1[1].set_ylabel(None)
    ax1[1].set_xlabel("Total Revenue", fontsize=12)
    ax1[1].invert_xaxis()
    ax1[1].yaxis.set_label_position("right")
    ax1[1].yaxis.tick_right()
    ax1[1].set_title("5 Pendapatan Terendah", loc="center", fontsize=15)
    ax1[1].tick_params(axis='y', labelsize=12)

    st.pyplot(fig1)
else:
    st.warning("Tidak ada data transaksi pada rentang tanggal yang dipilih.")


st.subheader("Persentase Keterlambatan Pengiriman")

if total_orders > 0:
    labels = ['Tepat Waktu / Lebih Cepat', 'Terlambat']
    sizes = [total_orders - late_orders, late_orders]
    colors = ['#72BCD4', '#ff6f69']
    explode = (0, 0.1) 

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.2f%%',
            shadow=False, startangle=90, textprops={'fontsize': 12})
    ax2.axis('equal') 

    st.pyplot(fig2)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Pesanan", value=total_orders)
    with col2:
        st.metric("Pesanan Terlambat", value=late_orders)
else:
    st.warning("Tidak ada data pesanan pada rentang tanggal yang dipilih.")

st.caption('Copyright (c) Muhammad Surya Ibrahim 2026')
