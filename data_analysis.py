import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix

sns.set(rc={"figure.figsize":(14,14)})
plt.style.use("fivethirtyeight")

import warnings
warnings.filterwarnings(action="always")

df = pd.read_csv("signal_data.csv")
print(df.sample(7))
print(df.columns)  # ['g_x', ' g_y', ' TARGET']
df.columns = [x.replace(' ', '') for x in df.columns]
print(df.columns)
print(df['TARGET'].unique())

class_ = ["halt", "forward", "retreat", "left", "right"]
sns.scatterplot(x="g_x", y="g_y", hue="TARGET", data=df, palette="deep")
plt.show()

X = df.iloc[:, :-1]
y = df.iloc[:, -1]

for depth in range(1, 5):
    tree = DecisionTreeClassifier(max_depth=depth)
    tree.fit(X,y)
    y_pred = tree.predict(X)

    cm = confusion_matrix(y_pred, y)
    print(f"depth at : {depth} \n Confusion matrix: \n {cm} \n\n")
