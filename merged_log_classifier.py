
import pandas as pd
import os

def run_merged_classification():
    log_dir = "C:\\Users\\Study Blya\\Desktop\\Dissertation2\\Logs"

    # Load raw logs
    r1 = pd.read_csv(os.path.join(log_dir, "robot_1_log.csv"))
    r2 = pd.read_csv(os.path.join(log_dir, "robot_2_log.csv"))
    r3 = pd.read_csv(os.path.join(log_dir, "robot_3_log.csv"))

    # Drop timestamp (optional)
    r1 = r1.drop(columns=["Timestamp"])
    r2 = r2.drop(columns=["Timestamp"])
    r3 = r3.drop(columns=["Timestamp"])

    # Merge all logs on 'Piece ID'
    merged = r1.merge(r2, on="Piece ID").merge(r3, on="Piece ID")

    def classify(row):
        statuses = [row["Final Status_x"], row["Final Status_y"], row["Final Status"]]
        if "Scrap" in statuses:
            return "Scrap"
        elif "Rework" in statuses:
            return "Rework"
        else:
            return "Qualified"

    merged["Final Status"] = merged.apply(classify, axis=1)

    # Save merged log
    merged_path = os.path.join(log_dir, "merged_log.csv")
    merged.to_csv(merged_path, index=False)
    print(f"Merged log saved to: {merged_path}")

    # Print summary
    summary = merged["Final Status"].value_counts().reset_index()
    summary.columns = ["Status", "Count"]
    print("\n--- Classification Summary ---")
    print(summary)

    # Save summary
    summary.to_csv(os.path.join(log_dir, "merged_summary.csv"), index=False)

# Uncomment to test standalone
# if __name__ == "__main__":
#     run_merged_classification()
