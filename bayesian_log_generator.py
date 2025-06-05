import os
import pandas as pd
from robot_classifiers import classify_robot_1, classify_robot_2, classify_robot_3

def generate_fault_log():
    log_dir = r"C:\Users\Study\Desktop\Dissertation2\Logs"
    output_path = os.path.join(log_dir, "Bayesian Database")
    os.makedirs(output_path, exist_ok=True)

    fault_log_path = os.path.join(output_path, "fault_causes_log.csv")

    # Step 1: Determine next day index
    if os.path.exists(fault_log_path):
        existing_df = pd.read_csv(fault_log_path)
        if 'Day' in existing_df.columns:
            next_day = existing_df['Day'].max() + 1
        else:
            next_day = 1
    else:
        existing_df = None
        next_day = 1

    # Step 2: Analyze current robot logs
    fault_log = []

    for filename in os.listdir(log_dir):
        if filename.startswith("robot_") and filename.endswith("_log.csv"):
            machine_id = int(filename.split("_")[1])
            path = os.path.join(log_dir, filename)
            df = pd.read_csv(path)

            for _, row in df.iterrows():
                piece_id = row["Piece ID"]

                if machine_id == 1:
                    result, cause = classify_robot_1(row)
                elif machine_id == 2:
                    result, cause = classify_robot_2(row)
                elif machine_id == 3:
                    result, cause = classify_robot_3(row)
                else:
                    result, cause = "Unknown", "Unknown"

                month = (next_day - 1) // 30 + 1  # Month grouping by every 30 days
                fault_log.append([
                    piece_id,
                    machine_id,
                    result,
                    cause,
                    next_day,
                    month
                ])

    # Step 3: Append or create the fault cause log
    df_fault = pd.DataFrame(
        fault_log,
        columns=["Piece ID", "Machine ID", "Final Status", "Fault Cause", "Day", "Month"]
    )

    if existing_df is not None:
        final_df = pd.concat([existing_df, df_fault], ignore_index=True)
    else:
        final_df = df_fault

    final_df.to_csv(fault_log_path, index=False)
    print(f"Bayesian fault log updated: Day {next_day} added → {fault_log_path}")
