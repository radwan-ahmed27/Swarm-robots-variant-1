import pandas as pd
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder

def run_fault_prediction():
    log_path = r"C:\Users\Study\Desktop\Dissertation2\Logs\Bayesian Database\fault_causes_log.csv"
    df = pd.read_csv(log_path)

    # Train on all labeled rows
    train_df = df[df["Final Status"].notna()].copy()

    if train_df.empty:
        print("❌ No labeled data available to train the classifier.")
        return

    # Determine starting day and month for prediction
    last_day = int(train_df["Day"].max())
    last_month = int(train_df["Month"].max())
    next_day = last_day + 1

    # Generate prediction data for the next 30 days (100 pieces per day × 3 machines)
    future_rows = []
    for day in range(next_day, next_day + 30):
        month = (day - 1) // 30 + 1
        for piece in range(1, 101):
            piece_id = f"P{str(piece).zfill(4)}"
            for machine_id in [1, 2, 3]:
                future_rows.append({
                    "Piece ID": piece_id,
                    "Machine ID": machine_id,
                    "Day": day,
                    "Month": month
                })

    predict_df = pd.DataFrame(future_rows)

    # Prepare training data
    le_status = LabelEncoder()
    y = le_status.fit_transform(train_df["Final Status"])
    X_train = pd.get_dummies(train_df[["Machine ID", "Day", "Month"]])

    # Prepare prediction features
    X_pred = pd.get_dummies(predict_df[["Machine ID", "Day", "Month"]])
    X_pred = X_pred.reindex(columns=X_train.columns, fill_value=0)
    X_pred = X_pred.fillna(0)

    # Train and predict
    model = MultinomialNB()
    model.fit(X_train, y)
    y_pred = model.predict(X_pred)
    predict_df["Predicted Status"] = le_status.inverse_transform(y_pred)

    # Save result
    out_dir = os.path.dirname(log_path)
    output_file = os.path.join(out_dir, f"classifier_results_day_{next_day}_to_day_{next_day + 29}.csv")
    predict_df.to_csv(output_file, index=False)

    print(f"✅ Prediction complete.\nSaved to: {output_file}")

if __name__ == "__main__":
    run_fault_prediction()
