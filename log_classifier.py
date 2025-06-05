import pandas as pd
import os
from robot_classifiers import classify_robot_1, classify_robot_2, classify_robot_3

def run_log_analysis():
    log_dir = "C:\\Users\\Study\\Desktop\\Dissertation2\\Logs"
    summary = []

    for filename in os.listdir(log_dir):
        if filename.startswith("robot_") and filename.endswith("_log.csv"):
            file_path = os.path.join(log_dir, filename)
            df = pd.read_csv(file_path)

            columns = df.columns.tolist()
            results = []
            qualified = 0
            rework = 0
            scrap = 0

            for _, row in df.iterrows():
                if "Length" in columns:
                    result, _ = classify_robot_1(row)
                elif "Surface Smoothness" in columns:
                    result, _ = classify_robot_2(row)
                elif "Hardness" in columns:
                    result, _ = classify_robot_3(row)
                else:
                    result = "Unknown"

                results.append(result)

                if result == "Qualified":
                    qualified += 1
                elif result == "Rework":
                    rework += 1
                elif result == "Scrap":
                    scrap += 1

            # Assign the classification results to the correct rows
            df["Final Status"] = results
            df.to_csv(file_path, index=False)

            robot_id = filename.split("_")[1]
            summary.append({
                "Robot ID": robot_id,
                "Qualified": qualified,
                "Rework": rework,
                "Scrap": scrap,
                "Total": qualified + rework + scrap
            })

    summary_df = pd.DataFrame(summary)
    print(summary_df)

    summary_path = os.path.join(log_dir, "summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Summary saved to: {summary_path}")

    from merged_log_classifier import run_merged_classification
    run_merged_classification()

    from final_report import analyze_robot_logs
    analyze_robot_logs()


    from bayesian_log_generator import generate_fault_log
    generate_fault_log()
    

    from predict_missing_faults import run_fault_prediction
    run_fault_prediction()
    
    # Optional Russian version
    # from final_report_ru import analyze_robot_logs as analyze_robot_logs_ru
    # analyze_robot_logs_ru()

    # Generate Bayesian training data



# Uncomment to run standalone
# if __name__ == "__main__":
#     run_log_analysis()
