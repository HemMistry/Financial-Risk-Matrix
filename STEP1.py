
import pandas as pd

try:
    # 🔹 File is in the same folder as the script
    df = pd.read_csv("accepted_2007_to_2018Q4.csv", low_memory=False, nrows=100000)
    print("✅ CSV loaded successfully")

    # 🔹 Sample 5000 rows
    df_small = df.sample(n=5000, random_state=42)
    print("✅ Sampled 5000 rows")

    # 🔹 Save Excel file in same folder
    df_small.to_excel("lendingclub_sample.xlsx", index=False)
    print("✅ Excel file saved as: lendingclub_sample.xlsx")

except FileNotFoundError:
    print("❌ File not found. Make sure the CSV is in this folder.")
except Exception as e:
    print(f"❌ Error: {e}")
