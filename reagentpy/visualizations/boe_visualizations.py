from typing import Optional
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from reagentpy.ReagentClient import ReagentClient
from reagentpy.clients.repo import RepoClient
from reagentpy.clients.composite_scores import CompositeClient


class BOEVisClient(ReagentClient):
    def __init__(self):
        super().__init__()
        self.colormap = plt.get_cmap("RdYlGn")


    def email_domain_pie_chart(self, repo: str):

        data = RepoClient().email_domains(repo, 100).df()

        # Prepare data for the pie chart
        labels = list(data["domain"])
        sizes = list(data["instances"])

        # Plotting the pie chart
        plt.figure(figsize=(14, 11))
        plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.axis("equal")  # Equal aspect ratio ensures that pie chart is drawn as a circle.

        # Show the pie chart
        plt.show()


    def get_colormap(self, percent: float):
        colormap = self.colormap
        # normalized_values = (percent / 100)
        if percent >= 90:
            # dark green
            normalized_values = (percent / 100)
        elif percent >= 75:
            # light green - yellow
            normalized_values = (percent / 150)
        elif percent >= 50:
            # yellow - orange
            normalized_values = (percent / 170)
        else:
            # red
            normalized_values = (percent / 200)
        return colormap(normalized_values)


    def total_chart(self, repo: str, adversarial: Optional[bool] =True):

        if adversarial:
            data = CompositeClient().adversarial_total(repo).dict()
            title = "Foreign Adversarial Score out of 100%"
            # print(data)
            score = data[0]["foreign_adversarial_influence_score"]
        else:
            data = CompositeClient().nonadversarial_total(repo).dict()
            title = "Metadata Risk Score out of 100%"
            score = data[0]["metadata_risk_score"]
            # print(data)
            # print(score)
        if len(data) != 1:
            raise ValueError("Expected a single dictionary of values, but got multiple.")

        _, ax = plt.subplots(figsize=(10, 1.5))

        # colormap
        bar_colors = self.get_colormap(score)

        # Create the foreground bar (actual score)
        ax.barh(y=0, width=score, color=bar_colors, align="center")

        ax.set_xlim(0, 100)
        ax.set_yticks([])
        ax.set_title(title)

        if score == 100:
            ax.text(score, 0, "%", ha="left", va="center")
        else:
            ax.text(score, 0, f"{score:.2f}%", ha="left", va="center")

        plt.tight_layout()
        plt.show()
        

    def create_percent_chart(self, repo: str, adversarial: Optional[bool] =False):

        if adversarial:
            data = CompositeClient().adversarial_components(repo).dict()
        else:
            data = CompositeClient().nonadversarial_components(repo).dict()

        if len(data) != 1:
            raise ValueError("Expected a single dictionary of values, but got multiple.")
        values = data[0]

        # Create and display charts for each metric
        for raw_title in values:

            if raw_title.find("weight") != -1:
                continue

            score = values[raw_title]

            title = f"{raw_title.replace('_', ' ').title()} out of 100%"

            _, ax = plt.subplots(figsize=(10, 1.5))

            # colormap
            bar_colors = self.get_colormap(score)

            # Create the foreground bar (actual score)
            ax.barh(y=0, width=score, color=bar_colors, align="center")

            ax.set_xlim(0, 100)
            ax.set_yticks([])
            ax.set_title(title)

            if score == 100:
                ax.text(score, 0, "%", ha="left", va="center")
            else:
                ax.text(score, 0, f"{score:.2f}%", ha="left", va="center")

            plt.tight_layout()
            plt.show()

    
    def plot_percent_timezone_color(self, repo: str):
        """Shows distribution across all timezones, coloring bars based on count"""

        data = CompositeClient().nonadversarial_timezones(repo)
        timezone_commit_data = data.dict()

        timezone_dict = {}
        for d in timezone_commit_data:
            normalized_timezone = str(d["timezone"])
            timezone_dict[normalized_timezone] = d["percent_of_total_commits"]

        timezones = list(timezone_dict.keys())
        commit_count = list(timezone_dict.values())

        # Select a colormap for cold-to-hot mapping
        # colormap = self.colormap
        # normalized_values = (commit_count - np.min(commit_count)) / (
        #     np.max(commit_count) - np.min(commit_count)
        # )
        # bar_colors = colormap(normalized_values)

        # Plotting
        plt.figure(figsize=(10, 6))
        plt.bar(timezones, commit_count, width=0.5, zorder=3) #color=bar_colors, width=0.5, zorder=3)

        plt.xticks(range(len(timezones)))
        plt.xlabel("Time Zone (UTC Offset)")
        plt.ylabel("Percent of Total Commits")
        plt.title("Commit Distribution Across Time Zones")

        plt.grid(axis="y", zorder=0)
        plt.gca().set_axisbelow(True)
        plt.tight_layout()
        plt.show()

    
    def show_percents_logarithmic_bar_chart(self, repo: str):
        """Show a bar chart of commits with log scale"""

        data = CompositeClient().nonadversarial_timezones(repo)
        values = data.dict()

        # Create DataFrame
        df = pd.DataFrame(values)

        # Sort by timezones
        df = df.sort_values(by="timezone", ascending=True)

        # Convert timezone from seconds to "UTC±" format
        df["timezone"] = df["timezone"].apply(lambda x: f"UTC{x:+.0f}")

        # Convert 'timezone' back to numerical offset for sorting
        df["timezone_numeric"] = df["timezone"].apply(
            lambda x: float(x[3:]) if x[3:] != "" else 0
        )

        # colormap
        # colormap = self.colormap
        # normalized_values = (df["percent_of_total_commits"])
        # bar_colors = colormap(normalized_values)

        # Plot chart
        plt.figure(figsize=(10, 6))
        plt.bar(x=df["timezone"], height=df["percent_of_total_commits"], zorder=3) #color=bar_colors, zorder=3)

        # Setting y-axis to logarithmic scale
        plt.yscale("log")

        # Setting labels and title
        plt.xlabel("Timezone (UTC±)", fontsize=16)
        plt.ylabel("Commit Count (log scale)", fontsize=16)
        plt.title("Commit Counts by Timezone Around the World (Log Scale)", fontsize=18)
        plt.xticks(rotation=45)  # Rotate the x-axis labels to avoid overlapping
        plt.grid(
            axis="y", linestyle="--", which="both"
        )  # Grid lines for both major and minor ticks

        plt.tight_layout()  # Adjust the layout
        plt.show()


    def plot_adversarial_percent_timezone_color(self, repo: str):
        """Shows distribution across all timezones, coloring bars based on count"""

        # Prepare data for the pie chart
        data = CompositeClient().adversarial_timezones(repo)
        timezone_commit_data = data.dict()
        timezone_commit_data.sort(key=lambda x: x["major_city"] != "Non-Adversarial")

        labels = [tz["country"] + ": " + tz["major_city"] if tz["major_city"] != "Non-Adversarial" else "Non-Adversarial" for tz in list(timezone_commit_data)]
        sizes = [tz["percent_of_total_commits"] for tz in list(timezone_commit_data)]

        # Create a list of colors for the pie slices
        colors = ['green' if label == 'Non-Adversarial' else 'red' if i % 2 == 0 else 'darkred' for i, label in enumerate(labels)]

        # Plotting the pie chart
        plt.figure(figsize=(10, 7))
        plt.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", rotatelabels =True, startangle=180, textprops = dict(va="center", rotation_mode = 'anchor'))
        plt.axis("equal")  # Equal aspect ratio ensures that pie chart is drawn as a circle.

        # Show the pie chart
        plt.show()

    
    def show_adversarial_percents_logarithmic_bar_chart(self, repo: str):
        """Show a bar chart of commits with log scale"""

        data = CompositeClient().adversarial_timezones(repo)
        values = data.dict()

        timezone_dict = {}
        for d in values:
            if d["major_city"] == "Non-Adversarial":
                normalized_timezone = d["major_city"]
            else:
                normalized_timezone = str(d["timezone"]) + " - " + str(d["major_city"])
            timezone_dict[normalized_timezone] = d["percent_of_total_commits"]

        timezones = list(timezone_dict.keys())
        commit_count = list(timezone_dict.values())

        # colormap
        bar_colors = self.get_colormap(commit_count)

        # Plot chart
        plt.figure(figsize=(10, 6))
        plt.bar(timezones, commit_count, color=bar_colors, zorder=3)

        # Setting y-axis to logarithmic scale
        plt.yscale("log")

        # Setting labels and title
        plt.xlabel("Timezone Offset and Corresponding City", fontsize=16)
        plt.ylabel("Commit Percent (log scale)", fontsize=16)
        plt.title("Commit Percentages by Timezone and Major City (Log Scale)", fontsize=18)
        plt.xticks(rotation=45)  # Rotate the x-axis labels to avoid overlapping
        plt.grid(
            axis="y", linestyle="--", which="both"
        )  # Grid lines for both major and minor ticks

        plt.tight_layout()  # Adjust the layout
        plt.show()
