import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_json("anime_data.json", encoding="utf-8")
st.title('Анализ аниме по данным MyAnimeList')

year_filter = st.sidebar.slider('Выберите год выпуска аниме', min_value=int(df['year'].min()), max_value=int(df['year'].max()), value=int(df['year'].max()))
filtered_year_df = df[df['year'] == year_filter]
st.subheader(f"Аниме, выпущенные в {year_filter}")
st.dataframe(filtered_year_df[['title', 'score', 'studio', 'genres']])

df['genres'] = df['genres'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
df_genres = df['genres'].str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
top_genres = df_genres.value_counts().head(10)

st.subheader('Топ-10 самых популярных жанров')
sns.set(style="whitegrid", palette="magma")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=top_genres.values, y=top_genres.index, palette='magma', ax=ax)
ax.set_xlabel('Количество', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Жанр', fontsize=14, fontweight='bold', color='black')
plt.tight_layout()
st.pyplot(fig)

studio_counts = df['studio'].value_counts().head(10)
st.subheader('Топ-10 студий по количеству аниме')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x=studio_counts.values, y=studio_counts.index, palette='coolwarm', ax=ax)
ax.set_xlabel('Количество', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Студия', fontsize=14, fontweight='bold', color='black')
plt.tight_layout()
st.pyplot(fig)

year_counts = df['year'].value_counts().sort_index()
st.subheader('Распределение аниме по годам')
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o', ax=ax)
ax.set_xlabel('Год', fontsize=14, fontweight='bold', color='black')
ax.set_ylabel('Количество', fontsize=14, fontweight='bold', color='black')
plt.tight_layout()
st.pyplot(fig)
