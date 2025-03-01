import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.patches as mpatches


sns.set_theme(style="dark", palette="deep", font_scale=1.2)
sns.axes_style("darkgrid")

def set_background_color():
    """Mengubah warna latar belakang menjadi cyan."""
    st.markdown(
       """
        <style>
        .stAppHeader {
            background-color: #ffffff !important;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .stAppHeader::after {
            content: "Dashboard Penyewaan Sepeda";
            font-size:40px;
            font-weight: bold;
            color: #333333;
        }
        .block-container {
            background-color: #F2F4F7 !important;
            color: black !important;
        }

        /* Pastikan sidebar juga terang */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important; /* Abu-abu terang */
        }

          /* Ubah latar belakang MultiSelect */
        [data-testid="stMultiSelect"] {
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
            border-radius: 5px !important;
            padding: 5px !important;
        }

        /* Ubah warna teks pada dropdown yang muncul */
        [data-testid="stMultiSelect"] div {
            color: black !important;
        }

        /* Ubah warna opsi yang dipilih */
        [data-testid="stMultiSelect"] span {
            background-color: cyan !important;
            color: black !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def load_data():
    """Memuat dataset bike-sharing.csv."""
    df = pd.read_csv("bike-sharing.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df
    
def plot_busy_hours(df):
    """Menampilkan jam tersibuk dalam penyewaan sepeda."""
    hour_df = df.groupby('hr', observed=False).agg({'cnt': 'sum'}).reset_index()
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=hour_df['hr'], y=hour_df['cnt'], color='lightblue', ax=ax)
    sns.lineplot(x=hour_df['hr'], y=hour_df['cnt'], color='blue', marker='o', linestyle='dashed', ax=ax)
    ax.set_facecolor("white")
    ax.set_title("Waktu Tersibuk dalam Penyewaan Sepeda", color='black')
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.tick_params(colors='black')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    st.pyplot(fig)

def plot_seasonal_rentals(df):
    """Menampilkan hubungan bulan dan musim dengan jumlah penyewaan."""
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#00DFA2" if i in [3, 4, 5] else  # Spring
              "yellow" if i in [6, 7, 8] else  # Summer
              "#FF0060" if i in [9, 10, 11] else  # Fall
              "#0079FF" for i in range(12)]  # Winter
    
    sns.barplot(x="mnth", y="cnt", hue="mnth", data=df, estimator=np.mean, errorbar=None, palette=colors, ax=ax)
    ax.set_facecolor("white")
    ax.set_title("Hubungan Bulan dan Musim Dengan Penyewaan", fontsize=14, color='black')
    ax.set_xlabel("", fontsize=12, color='black')
    ax.set_ylabel("", fontsize=12, color='black')
    ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"], color='black')
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    
    # Tambahkan keterangan warna musim
    legend_labels = [mpatches.Patch(color="#00DFA2", label="Spring"),
                     mpatches.Patch(color="yellow", label="Summer"),
                     mpatches.Patch(color="#FF0060", label="Fall"),
                     mpatches.Patch(color="#0079FF", label="Winter")]
    ax.legend(handles=legend_labels, title="Musim", loc="upper left")
  
    
    st.pyplot(fig)
    
def plot_temp_effect(df):
    """Menampilkan pengaruh suhu terhadap jumlah penyewaan sepeda."""
    df["temp_category"] = pd.cut(df["temp"], bins=5, labels=["Sangat Dingin", "Dingin", "Sejuk", "Hangat", "Panas"	])
    avg_rent_by_temp = df.groupby("temp_category", observed=True)["cnt"].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_facecolor("white")
    sns.lineplot(x="temp_category", y="cnt", data=avg_rent_by_temp, marker='o', color='#5AB6E9', linewidth=2.5, markersize=8, ax=ax)
    
    ax.set_title("Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda", fontsize=16, color='black')
    ax.set_xlabel("", fontsize=14, color='black')
    ax.set_ylabel("", fontsize=14, color='black')
    ax.grid(True, linestyle="--", alpha=0.7)
    
    st.pyplot(fig)
    
def plot_weather_effect(df):
    """Menampilkan jumlah penyewaan berdasarkan kondisi cuaca dalam bentuk donut chat."""
    weather_labels = ["Cerah", "Mendung", "Hujan", "Badai"]
    weather_colors = ["#09B6CC", "#1374E9", "#E62093", "#F9AD00"]
    avg_rent_per_weather = df.groupby("weathersit", observed=False)["cnt"].mean()
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(avg_rent_per_weather, labels=weather_labels, autopct='%1.1f%%', colors=weather_colors, wedgeprops={'edgecolor': 'white'}, startangle=90, pctdistance=0.78)
    
    # Buat lingkaran tengah untuk efek donu
    centre_circle = plt.Circle((0,0),0.58,fc='#ffffff')
    fig.gca().add_artist(centre_circle)
    
    ax.set_title("Jumlah Penyewaan Berdasarkan Kondisi Cuaca", fontsize=14, color='black')
    
    st.pyplot(fig)

def show_summary_statistics(df):

    total_rentals = df["cnt"].sum()
    avg_rentals = df["cnt"].mean()
    max_rentals = df["cnt"].max()

    avg_rentals_formatted = "{:.3f}".format(avg_rentals)

    # Buat 3 kolom untuk card-style
    col1, col2, col3 = st.columns(3)

    style= "<div style='background-color: #ffffff; color: black; border-radius: 5px; margin-bottom: 20px;'>"

    with col1:
        st.markdown(
            f"""
            {style}
                <h4 style="text-align: center; margin-bottom: 5px;">Total Penyewaan</h4>
                <h3 style="text-align: center; color: #09B6CC; margin-top: 5px;">{total_rentals:,}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            {style}
                <h4 style="text-align: center; margin-bottom: 5px;">Rerata Penyewaan</h4>
                <h3 style="text-align: center; color: #1374E9; margin-top: 5px;">{avg_rentals_formatted}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            {style}
                <h4 style="text-align: center; margin-bottom: 5px;">Sewa Tertinggi</h4>
                <h3 style="text-align: center; color: #E62093; margin-top: 5px;">{max_rentals}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    st.set_page_config(
    page_title="Dashboard Penyewaan Sepeda",
    layout="wide",
    initial_sidebar_state="expanded"
    )

    df = load_data()

    content, right_sidebar = st.columns([4, 2])
    set_background_color()
    
    with content:
        show_summary_statistics(df)
        plot_busy_hours(df)
        plot_seasonal_rentals(df)
        

    with right_sidebar:
        selected_plots = st.multiselect(
            label="Pilih chart yang ingin ditampilkan",
            options=('Pengaruh Suhu', 'Penyewaan Berdasarkan Cuaca'),
            help="Pilih chart yang ingin ditampilkan."
        )

        if "Pengaruh Suhu" in selected_plots:
            plot_temp_effect(df)

        if "Penyewaan Berdasarkan Cuaca" in selected_plots:
            plot_weather_effect(df)

if __name__ == "__main__":
    main()
