# Analisi Diffusione COVID-19 - Epicode W12D8
import pandas as pd
import matplotlib.pyplot as plt

# Caricamento del dataset
df = pd.read_csv("covid.csv")

# Dimensioni e prime info
print(f"Righe: {df.shape[0]}")
print(f"Colonne: {df.shape[1]}")
print("Colonne principali:", df.columns[:10].tolist())
print("Esempio di record:")
print(df.head(1).T)

# Punto 2a - Casi totali per continente
df_clean = df.dropna(subset=["continent"])
latest = df_clean.sort_values("date").groupby("location").last()
continent_cases = latest.groupby("continent")["total_cases"].sum().sort_values(ascending=False)
print("Totale casi per continente:")
print(continent_cases)

# Punto 2b - Percentuale casi per continente
world_total_cases = continent_cases.sum()
continent_percentage = (continent_cases / world_total_cases) * 100
print("Percentuale casi per continente:")
print(continent_percentage)

# Punto 3 - Evoluzione casi totali Italia nel 2022
italy_2022 = df[(df["location"] == "Italy") & (df["date"].str.startswith("2022"))]
italy_2022["date"] = pd.to_datetime(italy_2022["date"])
italy_2022 = italy_2022.set_index("date").resample("W")["total_cases"].last().dropna()

plt.figure(figsize=(10, 5))
italy_2022.plot(title="Evoluzione casi totali in Italia nel 2022")
plt.ylabel("Casi totali")
plt.xlabel("Data")
plt.grid(True)
plt.tight_layout()
plt.savefig("italy_cases_2022.png")
plt.show()

# Punto 3b - Nuovi casi nel 2022
italy_new_cases = df[(df["location"] == "Italy") & (df["date"].str.startswith("2022"))]
italy_new_cases["date"] = pd.to_datetime(italy_new_cases["date"])
weekly_new_cases = italy_new_cases.set_index("date").resample("W")["new_cases"].sum().dropna()

plt.figure(figsize=(10, 5))
weekly_new_cases.plot(title="Nuovi casi settimanali in Italia (2022)")
plt.ylabel("Nuovi casi")
plt.xlabel("Data")
plt.grid(True)
plt.tight_layout()
plt.savefig("italy_new_cases_2022.png")
plt.show()

# Punto 4 - Pazienti in terapia intensiva
countries = ["Italy", "Germany", "France"]
icu = df[df["location"].isin(countries) & (df["date"] >= "2022-01-01")]
icu["date"] = pd.to_datetime(icu["date"])
icu_grouped = icu.groupby(["date", "location"])["icu_patients"].mean().unstack()

icu_grouped.plot(figsize=(12, 6), title="Pazienti in terapia intensiva (2022-2023)")
plt.ylabel("Pazienti")
plt.xlabel("Data")
plt.grid(True)
plt.tight_layout()
plt.savefig("icu_patients.png")
plt.show()

# Punto 5 - Pazienti ospedalizzati nel 2021
hosp = df[df["location"].isin(["Italy", "Germany", "France", "Spain"]) & df["date"].str.startswith("2021")]
hosp["date"] = pd.to_datetime(hosp["date"])
hosp_grouped = hosp.groupby(["date", "location"])["hosp_patients"].mean().unstack()

hosp_grouped.plot(figsize=(12, 6), title="Pazienti ospedalizzati nel 2021")
plt.ylabel("Pazienti")
plt.xlabel("Data")
plt.grid(True)
plt.tight_layout()
plt.savefig("hosp_patients_2021.png")
plt.show()
