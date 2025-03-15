import pandas as pd
import matplotlib.pyplot as plt

# Define question mappings with additional questions
question_map = {
    "Q1": ["Q3.1_1", "Q3.1_2", "Q2.1_1", "Q2.1_2"],
    "Q2": ["Q3.3_1", "Q3.3_2", "Q2.3_1", "Q2.3_2"],
    "Q3": ["Q3.5_1", "Q3.5_2", "Q2.5_1", "Q2.5_2"],
    "Q4": ["Q3.7_1", "Q3.7_2"],
    "Q5": ["Q3.9_1", "Q3.9_2", "Q3.14_1", "Q3.14_2"],
    "Q6": ["Q3.11_1", "Q3.11_2"],
    "Q7": ["Q2.7_1", "Q2.7_2"],
    "Q8": ["Q2.9_1", "Q2.9_2"],
    "Q9": ["Q2.16_1", "Q2.16_2"]
}

# Load CSV
file_path = "survey.csv"  # Replace with actual file path
df = pd.read_csv(file_path)

# Compute averages
avg_data = {"Question": [], "AutoPentester": [], "PentestGPT": []}

for q, cols in question_map.items():
    auto_values, gpt_values = [], []
    
    for i in range(0, len(cols), 2):
        auto_col, gpt_col = cols[i], cols[i + 1]
        if auto_col in df.columns and gpt_col in df.columns:
            auto_values.append(pd.to_numeric(df[auto_col], errors='coerce'))
            gpt_values.append(pd.to_numeric(df[gpt_col], errors='coerce'))
    
    if auto_values and gpt_values:
        avg_data["Question"].append(q)
        avg_data["AutoPentester"].append(pd.concat(auto_values).mean())
        avg_data["PentestGPT"].append(pd.concat(gpt_values).mean())

# Print computed averages
a = sum(avg_data["AutoPentester"]) / len(avg_data["AutoPentester"])
b = sum(avg_data["PentestGPT"]) / len(avg_data["PentestGPT"])
print('AutoPentester:', a)
print('PentestGPT:', b)
print((a - b) * 100 / b)

# Convert to DataFrame
avg_df = pd.DataFrame(avg_data)

# Plot
plt.figure(figsize=(6.5, 3.5))
x = range(len(avg_df["Question"]))
plt.bar(x, avg_df["AutoPentester"], width=0.3, label="AutoPentester", align="center", alpha=0.9)
plt.bar([i + 0.3 for i in x], avg_df["PentestGPT"], width=0.3, label="PentestGPT", align="center", alpha=0.9)

plt.xticks([i + 0.2 for i in x], avg_df["Question"])
plt.xlabel("Question")
plt.ylabel("Average Score")
plt.ylim(0, 5.5)
plt.title("Survey Results")
plt.legend()
plt.grid(True, axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

plt.tight_layout(rect=[0, 0.002, 1, 1])
plt.savefig('survey.pdf', format='pdf', bbox_inches="tight")
plt.show()