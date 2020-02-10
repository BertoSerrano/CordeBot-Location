import os
import numpy as np

# file_path = "/home/berto/Documents/CordeBot/CordeBot-Location/src/results.txt"
file_path = "/home/berto/Documents/CordeBot/CordeBot-Location/src/results__inside_lab.txt"

x_column = []
y_column = []
z_column = []


with open(file_path, "r") as f:
    for line in f:
        if ":" in line and "quality" not in line:
            line = line.replace(",\n", "")
            if "x" in line:
                line = line.replace('    "x_position": ', "")
                x_column.append(float(line.replace(" ", "")))
            if "y" in line:
                line = line.replace('    "y_position": ', "")
                y_column.append(float(line.replace(" ", "")))
            if "z" in line:
                line = line.replace('    "z_position": ', "")
                z_column.append(float(line.replace(" ", "")))

x_column = np.asarray(x_column)
y_column = np.asarray(y_column)
z_column = np.asarray(z_column)

print("Variance of X values: ", np.var(x_column, ddof=1))
print("Variance of Y values: ", np.var(y_column, ddof=1))
print("Variance of Z values: ", np.var(z_column, ddof=1))

print("Typical deviation of X values: ", np.std(x_column, ddof=1))
print("Typical deviation of Y values: ", np.std(y_column, ddof=1))
print("Typical deviation of Z values: ", np.std(z_column, ddof=1))

print("Mean of X values: ", np.mean(x_column))
print("Mean of Y values: ", np.mean(y_column))
print("Mean of Z values: ", np.mean(z_column))
