import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import os

os.makedirs("data", exist_ok=True)
os.makedirs("results", exist_ok=True)

# -------------------------
# Generate panel dataset
# -------------------------

np.random.seed(42)

n_individuals = 200
n_periods = 10

data = []

for i in range(n_individuals):

    treatment = 1 if i < 100 else 0

    for t in range(n_periods):

        post = 1 if t >= 5 else 0

        outcome = (
            5
            + 0.5 * treatment
            + 0.3 * post
            + 2 * treatment * post
            + np.random.normal(0,1)
        )

        data.append([i,t,treatment,post,outcome])

df = pd.DataFrame(
    data,
    columns=["id","time","treatment","post","outcome"]
)

df["did"] = df["treatment"] * df["post"]

df.to_csv("data/panel_dataset.csv",index=False)

# -------------------------
# Difference-in-Differences
# -------------------------

model = smf.ols(
    "outcome ~ treatment + post + did",
    data=df
).fit()

print(model.summary())

with open("results/did_regression.txt","w") as f:
    f.write(model.summary().as_text())

# -------------------------
# Plot policy effect
# -------------------------

avg = df.groupby(["time","treatment"])["outcome"].mean().reset_index()

for key,grp in avg.groupby("treatment"):

    label = "Treatment" if key==1 else "Control"

    plt.plot(grp["time"],grp["outcome"],label=label)

plt.axvline(5,linestyle="--")

plt.title("Difference-in-Differences Policy Effect")

plt.xlabel("Time")

plt.ylabel("Average Outcome")

plt.legend()

plt.savefig("results/policy_effect_plot.png")

plt.show()