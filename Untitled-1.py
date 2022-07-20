# %%
import pandas as pd
import numpy as np
import streamlit as st


# %%
st.title("Промокоды1")

upload_file = "offers_responds_06_01_07_01.txt"

df = pd.read_csv(upload_file, sep='|')
#df = pd.read_csv('/Users/arturfattahov/Downloads/Telegram Desktop/offers_responds_06_01_07_01.txt', sep='|')
df = df.dropna()

df.columns = [c.lower().replace(' ','') for c in df.columns]

df['responds_id'] = df['responds_id'].str.strip()
df = df.query('responds_id != ""')

df["category_id"] = df["category_id"].astype(int)
df["client_phone"] = df["client_phone"].astype(int)
df["responds_id"] = df["responds_id"].astype(int)
df['offer_created_at']= pd.to_datetime(df['offer_created_at'], format='%Y-%m-%d %H:%M:%S')
df['respond_created_at']= pd.to_datetime(df['respond_created_at'], format='%Y-%m-%d %H:%M:%S')

# %%
df = df.sort_values(by=['state', 'offer_id', 'respond_created_at'])
df['sequence']=df.groupby('offer_id').cumcount() + 1

# %%
st.title("Промокоды2")


# %%
df = df.query('sequence == 1')

# %%
st.title("Промокоды3")

# %%
df['diff_time'] = df['respond_created_at'] - df['offer_created_at']

# %%
st.title("Промокоды4")

# %%
df['diff_time'] = df['diff_time'].astype('timedelta64[m]')
df['diff_time'] = df['diff_time'] / 60
df['diff_time'] = df['diff_time'].round(2)

# %%
st.title("Промокоды5")

# %%
def time_distribution(diff_time):
    if diff_time < 0.5:
        return 'Менее 30 минут'
    elif 0.5 <= diff_time < 1:
        return 'От 30 минут до 1 часа'
    elif 1 <= diff_time < 2:
        return 'От 1 до 2 часов'
    elif 2 <= diff_time < 5:
        return 'От 2 до 5 часов'
    elif 5 <= diff_time < 10:
        return 'От 5 до 10 часов'
    elif 10 <= diff_time < 15:
        return 'От 10 до 15 часов'
    elif 15 <= diff_time < 24:
        return 'От 15 до 24 часов'
    elif 24 <= diff_time < 36:
        return 'От 24 до 36 часов'
    elif 36 <= diff_time < 48:
        return 'От 36 до 48 часов'
    elif 48 <= diff_time < 72:
        return 'От 48 до 72 часов'
    else:
        return 'Более 72 часов'
df['time_period'] = df['diff_time'].apply(time_distribution)

# %%
st.title("Промокоды6")

# %%
df = df.drop(['client_phone', 'offer_created_at', 'responds_id', 'offer_id','executor_phone', 'respond_created_at', 'sequence', 'diff_time'], axis=1)

# %%
st.title("Промокоды7")

# %%
import numpy as np
df['count'] = 1

pivot_df = df.pivot_table(index=["state", 'category_id', 'time_period'], values='count', aggfunc='count')
pivot_df
pivot_df = pivot_df.reset_index()

# %%
st.title("Промокоды8")

# %%
df = df.sort_values(by=['state', 'category_id'])

# %%
st.title("Промокоды9")

# %%
df_l = pivot_df.pivot_table(index=['state', 'category_id'], columns='time_period')

# %%
st.title("Промокоды10")

# %%
df_l = df_l.reset_index()

# %%
st.title("Промокоды11")

# %%
df_l.columns = ['state', 'category_id', 'Более 72 часов', 'Менее 30 минут', 'От 1 до 2 часов',
               'От 10 до 15 часов', 'От 15 до 24 часов', 'От 2 до 5 часов', 'От 24 до 36 часов',
               'От 30 минут до 1 часа', 'От 36 до 48 часов', 'От 48 до 72 часов', 'От 5 до 10 часов']

# %%
st.title("Промокоды12")

# %%
new_df = df_l.reindex(columns=['state', 'category_id', 'Менее 30 минут', 'От 30 минут до 1 часа',
                               'От 1 до 2 часов', 'От 2 до 5 часов', 'От 5 до 10 часов', 'От 10 до 15 часов',
                               'От 15 до 24 часов', 'От 24 до 36 часов', 'От 36 до 48 часов',
                               'От 48 до 72 часов', 'Более 72 часов'])

# %%
new_df = new_df.fillna(0)

# %%
for col in new_df.columns:
    if str(new_df[col].dtype) == 'float64':
        new_df[col] = new_df[col].astype(int)

# %%
st.title("Промокоды13")

# %%
new_df['total_task'] = new_df[['Менее 30 минут', 'От 30 минут до 1 часа',
       'От 1 до 2 часов', 'От 2 до 5 часов', 'От 5 до 10 часов',
       'От 10 до 15 часов', 'От 15 до 24 часов', 'От 24 до 36 часов',
       'От 36 до 48 часов', 'От 48 до 72 часов', 'Более 72 часов']].sum(axis=1)

# %%
col_multi, col_em = st.columns([2, 3])
selected_sn = col_multi.selectbox(
    "Выберите штат",
    options=new_df['state'].unique().tolist(),
    index=0,
)

col_em.write("")
col_em.write("")
col_em.write(
    f"{selected_sn} содержит {new_df.query('state == @selected_sn').sum()[13]} задач с откликом"
)
st.write(new_df.query('state == @selected_sn'))


