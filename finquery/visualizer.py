import matplotlib.pyplot as plt
import os


class DataVisualizer:
    def create_bar_chart(self, data_dict, chart_title, filename="chart.png"):
        print(f"--- Drawing chart: '{chart_title}' ---")


        if not data_dict:
            print("--- [Visualizer] No numeric data to plot. Skipping chart. ---")
            return False

        labels = list(data_dict.keys())
        values = []

        for v in data_dict.values():
            try:
                v_clean = float(str(v).replace(",", ""))
                values.append(v_clean)
            except:
                print(f"[Visualizer] Skipping non-numeric value: {v}")


        if not values:
            print("--- [Visualizer] No valid numeric values found. Skipping chart. ---")
            return False

        try:
            plt.figure(figsize=(8,5))
            plt.bar(labels, values, color="skyblue")
            plt.title(chart_title)
            plt.xlabel("Period")
            plt.ylabel("Value")
            plt.savefig(filename)
            plt.close()
            print(f"--- Chart saved successfully as '{filename}' ---")
            return True
        except Exception as e:
            print(f"An error occurred while drawing chart: {e}")
            return False
