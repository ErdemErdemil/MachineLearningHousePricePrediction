#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#VERİ ÇEKME


# In[1]:


#pip install beautifulsoup4


# In[2]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# In[3]:


url_listesi = []
ilan_numarasi_listesi = []
guncelleme_tarihi_listesi = []
kategori_listesi = []
net_metrekare_listesi = []
oda_sayisi_listesi = []
bulundugu_kat_listesi = []
isitma_tipi_listesi = []
krediye_uygunluk_listesi = []
yapi_durumu_listesi = []
site_icerisinde_listesi = []
banyo_sayisi_listesi = []
fiyat_listesi = []
wc_sayisi_listesi = []


for sayfa_numarasi in range(1, 23):  
    url = "https://www.emlakjet.com/satilik-konut/antalya-kepez/" + str(sayfa_numarasi) + "/"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    ev_urls = soup.find_all('div', class_='_3qUI9q')

    for ev_url in ev_urls:
        ev_url = "https://www.emlakjet.com/" + ev_url.a.get("href")
        url_listesi.append(ev_url)

        ev_response = requests.get(ev_url)
        soup_ev = BeautifulSoup(ev_response.content, 'html.parser')

        ilan_bilgileri_div = soup_ev.find('div', {'id': 'bilgiler'})
        if ilan_bilgileri_div:

            ilan_numarasi = ilan_bilgileri_div.find('div', string='İlan Numarası')
            ilan_numarasi_listesi.append(
                ilan_numarasi.find_next('div', class_='_1bVOdb').text.strip() if ilan_numarasi else 'Bilinmiyor')

            guncelleme_tarihi = ilan_bilgileri_div.find('div', string='İlan Güncelleme Tarihi')
            guncelleme_tarihi_listesi.append(
                guncelleme_tarihi.find_next('div', class_='_1bVOdb').text.strip() if guncelleme_tarihi else 'Bilinmiyor')

            kategori = ilan_bilgileri_div.find('div', string='Kategorisi')
            kategori_listesi.append(kategori.find_next('div', class_='_1bVOdb').text.strip() if kategori else 'Bilinmiyor')

            net_metrekare = ilan_bilgileri_div.find('div', string='Net Metrekare')
            net_metrekare_listesi.append(
                pd.to_numeric(net_metrekare.find_next('div', class_='_1bVOdb').text.strip().replace('M2', ''), errors='coerce')
                if net_metrekare else np.nan)

            oda_sayisi = ilan_bilgileri_div.find('div', string='Oda Sayısı')
            oda_sayisi_listesi.append(
                oda_sayisi.find_next('div', class_='_1bVOdb').text.strip() if oda_sayisi else np.nan)

            bulundugu_kat = ilan_bilgileri_div.find('div', string='Bulunduğu Kat')
            bulundugu_kat_listesi.append(
                bulundugu_kat.find_next('div', class_='_1bVOdb').text.strip() if bulundugu_kat else np.nan)

            isitma_tipi = ilan_bilgileri_div.find('div', string='Isıtma Tipi')
            isitma_tipi_listesi.append(
                isitma_tipi.find_next('div', class_='_1bVOdb').text.strip() if isitma_tipi else 'Bilinmiyor')

            krediye_uygunluk = ilan_bilgileri_div.find('div', string='Krediye Uygunluk')
            krediye_uygunluk_listesi.append(
                krediye_uygunluk.find_next('div', class_='_1bVOdb').text.strip() if krediye_uygunluk else 'Bilinmiyor')

            yapi_durumu = ilan_bilgileri_div.find('div', string='Yapı Durumu')
            yapi_durumu_listesi.append(
                yapi_durumu.find_next('div', class_='_1bVOdb').text.strip() if yapi_durumu else 'Bilinmiyor')

            site_icerisinde = ilan_bilgileri_div.find('div', string='Site İçerisinde')
            site_icerisinde_listesi.append(
                site_icerisinde.find_next('div', class_='_1bVOdb').text.strip() if site_icerisinde else 'Bilinmiyor')

            banyo_sayisi = ilan_bilgileri_div.find('div', string='Banyo Sayısı')
            banyo_sayisi_listesi.append(
                banyo_sayisi.find_next('div', class_='_1bVOdb').text.strip() if banyo_sayisi else np.nan)
            
            wc_sayisi = ilan_bilgileri_div.find('div', string='WC Sayısı')
            wc_sayisi_listesi.append(
                wc_sayisi.find_next('div', class_='_1bVOdb').text.strip() if wc_sayisi else np.nan)

            fiyat = soup_ev.find('div', class_='_2TxNQv')
            if fiyat:
                fiyat_miktar = fiyat.text.strip().replace('TL', '').replace('.', '').replace(',', '')

                if ',' in fiyat_miktar:
                    fiyat_listesi.append(float(fiyat_miktar.replace(',', '')))
                elif fiyat_miktar.isdigit():
                    fiyat_listesi.append(int(fiyat_miktar))
                else:
                    fiyat_listesi.append(np.nan)


# In[4]:


df = pd.DataFrame({
    'Emlak URL': url_listesi,
    'İlan Numarası': ilan_numarasi_listesi,
    'İlan Güncelleme Tarihi': guncelleme_tarihi_listesi,
    'Kategori': kategori_listesi,
    'Net Metrekare': net_metrekare_listesi,
    'Oda Sayısı': oda_sayisi_listesi,
    'Bulunduğu Kat': bulundugu_kat_listesi,
    'Isıtma Tipi': isitma_tipi_listesi,
    'Krediye Uygunluk': krediye_uygunluk_listesi,
    'Yapı Durumu': yapi_durumu_listesi,
    'Site İçerisinde': site_icerisinde_listesi,
    'Banyo Sayısı': banyo_sayisi_listesi,
    'Fiyat': fiyat_listesi,
    'Tuvalet Sayısı' : wc_sayisi_listesi
})


# In[5]:


df.to_excel("X_Emlak_Verileri.xlsx", index=False)


# In[6]:


#ÖN İŞLEME


# In[7]:


import pandas as pd
from sklearn.preprocessing import LabelEncoder


# In[8]:


excel_file_path = r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx"
df = pd.read_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx")


# In[9]:


df.columns = df.columns.str.replace(' ', '_')


# In[10]:


df.columns = df.columns.str.lower()


# In[11]:


df.columns = df.columns.str.replace('ı', 'i')
df.columns = df.columns.str.replace('ğ', 'g')
df.columns = df.columns.str.replace('ü', 'u')
df.columns = df.columns.str.replace('ö', 'o')
df.columns = df.columns.str.replace('ç', 'c')
df.columns = df.columns.str.replace('ş', 's')


# In[12]:


df['oda_sayisi'] = df['oda_sayisi'].replace({"1 Oda": "1+0", "Stüdyo": "1+0"})
df['oda_sayisi'] = df['oda_sayisi'].replace({"2.5+1": "3+0"})
df['oda_sayisi'] = df['oda_sayisi'].replace({" ":"2+0" })


# In[13]:


df.to_excel("X_Emlak_Verileri.xlsx", index=False)


# In[14]:


excel_filepath = r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx"
df = pd.read_excel(excel_file_path)

def oda_sayisi_donusumu(oda_sayisi):

    if pd.isna(oda_sayisi):
        return oda_sayisi

    elif not isinstance(oda_sayisi, str):
        return None

    else:
        try:

            sayilar = [float(sayi) for sayi in oda_sayisi.split('+')]
            return sum(sayilar)
        except ValueError:

            return None

df['oda_sayisi'] = df['oda_sayisi'].apply(oda_sayisi_donusumu)

df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[15]:


excel_file_path = r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx"
df = pd.read_excel(excel_file_path)

non_numeric_columns = df.select_dtypes(exclude='number').columns

for column in non_numeric_columns:
    df[column].replace('Bilinmiyor', None, inplace=True)
    if df[column].dtype != 'O':  
        df[column].fillna(df[column].mean(), inplace=True)
        df[column] = df[column].astype(int) 
    else:
        df[column].fillna(df[column].mode()[0], inplace=True)

df['oda_sayisi'].replace('Yok', None, inplace=True)

df['oda_sayisi'] = pd.to_numeric(df['oda_sayisi'], errors='coerce')

df['oda_sayisi'].fillna(df['oda_sayisi'].mean(), inplace=True)
df['fiyat'].fillna(df['fiyat'].mean(), inplace=True)


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[16]:


excel_file_path = r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx"
df = pd.read_excel(excel_file_path)

df.drop("emlak_url", axis= 1 ,inplace = True )
df.drop("i̇lan_numarasi", axis= 1 ,inplace = True )
df.drop("i̇lan_guncelleme_tarihi", axis = 1 , inplace = True)
df.drop("kategori", axis= 1 ,inplace = True )
df.drop("tuvalet_sayisi", axis= 1 ,inplace = True )


# In[17]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[18]:


df['fiyat'] = df['fiyat'].replace({"2912621,97637795":"2912621" })


# In[19]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[20]:


df.loc[df.bulundugu_kat == "Yüksek Giriş" , "bulundugu_kat"] = "1.Kat"
df.loc[df.bulundugu_kat == "Düz Giriş (Zemin)" , "bulundugu_kat"] = "1.Kat"
df.loc[df.bulundugu_kat == "Bahçe Katı" , "bulundugu_kat"] = "1.Kat"
df.loc[df.bulundugu_kat == "Bahçe Dublex" , "bulundugu_kat"] = "1.Kat"
df.loc[df.bulundugu_kat == "Bodrum Kat" , "bulundugu_kat"] = "1.Kat"


# In[21]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[22]:


df['oda_sayisi'] = df['oda_sayisi'].replace({"3,30030487804878":"3" })
df.loc[df.bulundugu_kat == "Villa Tipi" , "bulundugu_kat"] = "1.Kat"
df.loc[df.bulundugu_kat == "Çatı Dubleks" , "bulundugu_kat"] = "3.Kat"
df.loc[df.bulundugu_kat == "Kot 1 (-1).Kat" , "bulundugu_kat"] = "1.Kat"
df.loc[df.bulundugu_kat == "Çatı Katı" , "bulundugu_kat"] = "3.Kat"


# In[23]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[24]:


df['oda_sayisi'] = df['oda_sayisi'].round()


# In[25]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[26]:


df.loc[df.isitma_tipi == "Kombi Doğalgaz" ,       "isitma_tipi"] = "Doğalgaz"
df.loc[df.isitma_tipi == "Merkezi (Pay Ölçer)" ,  "isitma_tipi"] = "Doğalgaz"
df.loc[df.isitma_tipi == "Yerden Isıtma" ,        "isitma_tipi"] = "Doğalgaz"
df.loc[df.isitma_tipi == "Merkezi Doğalgaz" ,     "isitma_tipi"] = "Doğalgaz"
df.loc[df.isitma_tipi == "Doğalgaz Sobalı" ,      "isitma_tipi"] = "Doğalgaz"
df.loc[df.isitma_tipi == "Güneş Enerjisi" ,       "isitma_tipi"] = "Diğer"
df.loc[df.isitma_tipi == "Sobalı" ,               "isitma_tipi"] = "Diğer"
df.loc[df.isitma_tipi == "Kat Kaloriferi" ,       "isitma_tipi"] = "Diğer"
df.loc[df.isitma_tipi == "Merkezi Kömür" ,        "isitma_tipi"] = "Diğer"


# In[27]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[28]:


df['fiyat'] = df['fiyat'].round()


# In[29]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[30]:


df.loc[df.banyo_sayisi == "Yok" , "banyo_sayisi"] = "0"


# In[31]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[32]:


df.loc[df.yapi_durumu == "Yapım Aşamasında" , "yapi_durumu"] = "Sıfır"


# In[33]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[51]:


df.loc[df.bulundugu_kat == "1.Kat" ,       "bulundugu_kat"] = "1"
df.loc[df.bulundugu_kat == "2.Kat" ,       "bulundugu_kat"] = "2"
df.loc[df.bulundugu_kat == "3.Kat" ,       "bulundugu_kat"] = "3"
df.loc[df.bulundugu_kat == "4.Kat" ,       "bulundugu_kat"] = "4"
df.loc[df.bulundugu_kat == "5.Kat" ,       "bulundugu_kat"] = "5"
df.loc[df.bulundugu_kat == "6.Kat" ,       "bulundugu_kat"] = "6"
df.loc[df.bulundugu_kat == "7.Kat" ,       "bulundugu_kat"] = "7"
df.loc[df.bulundugu_kat == "8.Kat" ,       "bulundugu_kat"] = "9"
df.loc[df.bulundugu_kat == "9.Kat" ,       "bulundugu_kat"] = "9"
df.loc[df.bulundugu_kat == "10.Kat" ,       "bulundugu_kat"] = "10"
df.loc[df.bulundugu_kat == "11.Kat" ,       "bulundugu_kat"] = "11"
df.loc[df.bulundugu_kat == "12.Kat" ,       "bulundugu_kat"] = "12"
df.loc[df.bulundugu_kat == "13.Kat" ,       "bulundugu_kat"] = "13"


# In[52]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri.xlsx", index=False)


# In[53]:


df


# In[54]:


#ENCODING


# In[55]:


le = LabelEncoder()


# In[56]:


le.fit_transform(df["isitma_tipi"])


# In[57]:


df["isitma_tipi"] = le.fit_transform(df["isitma_tipi"])


# In[58]:


le.fit_transform(df["krediye_uygunluk"])


# In[59]:


df["krediye_uygunluk"] = le.fit_transform(df["krediye_uygunluk"])


# In[60]:


le.fit_transform(df["yapi_durumu"])


# In[61]:


df["yapi_durumu"] = le.fit_transform(df["yapi_durumu"])


# In[62]:


le.fit_transform(df["site_i̇cerisinde"])


# In[63]:


df["site_i̇cerisinde"] = le.fit_transform(df["site_i̇cerisinde"])


# In[64]:


le.fit_transform(df["bulundugu_kat"])


# In[65]:


df["bulundugu_kat"] = le.fit_transform(df["bulundugu_kat"])


# In[66]:


df.to_excel(r"C:\Users\erdem\X\X_Emlak_Verileri_Onislenmis.xlsx", index=False)


# In[67]:


#ALGORİTMALAR


# In[73]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler

excel_file_path = r"C:\Users\erdem\X\X_Emlak_Verileri_Onislenmis.xlsx"
df = pd.read_excel(excel_file_path)

X = df.drop("fiyat", axis=1)
y = df["fiyat"]

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42)

models = [
    ("Random Forest", RandomForestRegressor(random_state=42)),
    ("Gradient Boosting", GradientBoostingRegressor(random_state=42)),
    ("Linear Regression", LinearRegression()),
    ("Ridge", Ridge()),
    ("Lasso", Lasso()),
    ("SVR", SVR()),
    ("KNN", KNeighborsRegressor())
]

best_model_name = None
best_model_r2 = -float('inf')
best_model_mse = float('inf')

for model_name, model in models:

    model.fit(X_train, y_train)
    

    y_pred = model.predict(X_test)
    

    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    

    print(f"{model_name} Modeli:")
    print(f"R-squared (R²) Score: {r2}")
    print(f"Mean Squared Error (MSE): {mse}")
    print("="*50)

    if r2 > best_model_r2 and mse < best_model_mse:
        best_model_r2 = r2
        best_model_name = model_name
        best_model_mse = mse
        
print(f"En iyi model: {best_model_name} (R-squared Score: {best_model_r2}, MSE: {best_model_mse})")


# In[74]:


#VERİ EĞİTİMİ


# In[76]:


import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib

excel_filepath = r"C:\Users\erdem\X\X_Emlak_Verileri_Onislenmis.xlsx"
df = pd.read_excel(excel_filepath)

df.dropna(inplace=True)

X = df.drop("fiyat", axis=1)
y = df["fiyat"]
y = y.fillna(y.mean())

model = GradientBoostingRegressor()  
model.fit(X, y)

trained_columns = X.columns.tolist()

model_filename = "x_test_model.pkl"
joblib.dump(model, model_filename)
joblib.dump(trained_columns, 'x_trained_columns.pkl')


# In[78]:


df.columns


# In[ ]:


#SERVİSLEME


# In[82]:


import streamlit as st
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
import joblib

model = joblib.load("x_test_model.pkl")

trained_columns = joblib.load("x_trained_columns.pkl")

st.sidebar.header("Emlak Tahmini Uygulaması")
features = {}
for column in trained_columns:
    features[column] = st.sidebar.number_input(f"Enter {column}", value=0)

input_data = pd.DataFrame([features])
prediction = model.predict(input_data)[0]

st.write(f"**Tahmini Fiyat:** {prediction:.2f} TL")


# In[ ]:




