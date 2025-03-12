#!/usr/bin/env python3
"""test_accuracy.py

A consolidated Python script that:
1. Measures digit-level and text-based (Levenshtein) accuracy.
2. Computes numeric confusion matrices, text character confusion.
3. Calculates absolute error and percentage error for numeric fields.
4. Optionally plots the distribution of absolute errors.

All functions have docstrings explaining their purpose.
Example usage is in the `main()` function at the bottom.

Author: Your Name
"""

import string

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def levenshtein_distance(s1: str, s2: str) -> int:
    """Compute the Levenshtein edit distance between two strings s1 and s2.
    The distance is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to transform s1 into s2.

    :param s1: First string.
    :param s2: Second string.
    :return: Integer representing the Levenshtein distance.
    """
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)

    rows = len(s1) + 1
    cols = len(s2) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost,  # substitution
            )
    return dp[-1][-1]


def digit_level_accuracy(true_val, pred_val):
    """Compare two numeric values (or strings) digit by digit,
    counting how many match exactly.

    :param true_val: Ground-truth numeric value or string.
    :param pred_val: Predicted numeric value or string.
    :return: (matched_digits, total_digits_in_truth)
    """
    t_str = str(true_val)
    p_str = str(pred_val)

    matched = 0
    total = len(t_str)

    min_len = min(len(t_str), len(p_str))
    for i in range(min_len):
        if t_str[i] == p_str[i]:
            matched += 1

    return matched, total


def evaluate_accuracy(
    df_true: pd.DataFrame, df_pred: pd.DataFrame, numeric_cols, text_cols
) -> dict:
    """Measure overall digit-level accuracy for numeric columns
    and average Levenshtein distance for text columns.

    :param df_true: Ground-truth DataFrame.
    :param df_pred: Predicted (AI) DataFrame.
    :param numeric_cols: List of numeric column names.
    :param text_cols: List of text column names.
    :return: Dictionary with keys:
        {
            "digit_level_accuracy": float,
            "avg_levenshtein_dist": float
        }
    """
    # 1) Numeric accuracy
    total_matched_digits = 0
    total_groundtruth_digits = 0
    for col in numeric_cols:
        for i in range(len(df_true)):
            matched, total = digit_level_accuracy(
                df_true[col].iloc[i], df_pred[col].iloc[i]
            )
            total_matched_digits += matched
            total_groundtruth_digits += total

    numeric_accuracy = 0.0
    if total_groundtruth_digits > 0:
        numeric_accuracy = total_matched_digits / total_groundtruth_digits

    # 2) Text columns -> Levenshtein distance
    total_lev_dist = 0
    count_entries = 0
    for col in text_cols:
        for i in range(len(df_true)):
            true_str = str(df_true[col].iloc[i])
            pred_str = str(df_pred[col].iloc[i])
            dist = levenshtein_distance(true_str, pred_str)
            total_lev_dist += dist
            count_entries += 1

    avg_lev_dist = 0.0
    if count_entries > 0:
        avg_lev_dist = total_lev_dist / count_entries

    return {
        "digit_level_accuracy": numeric_accuracy,
        "avg_levenshtein_dist": avg_lev_dist,
    }


def compare_digits_with_confusion(true_val, pred_val, confusion_matrix):
    """Compare two numeric values (or strings) digit by digit,
    updating the confusion_matrix for digits 0-9.

    :param true_val: Ground-truth value.
    :param pred_val: Predicted value.
    :param confusion_matrix: A 10x10 array (rows=GT digit, cols=pred digit).
    :return: (matched_digits, total_digits_in_truth)
    """
    t_str = str(true_val)
    p_str = str(pred_val)

    matched = 0
    total = len(t_str)

    min_len = min(len(t_str), len(p_str))
    for i in range(min_len):
        gt_digit = t_str[i]
        pd_digit = p_str[i]

        if gt_digit.isdigit() and pd_digit.isdigit():
            gt_idx = int(gt_digit)
            pd_idx = int(pd_digit)
            confusion_matrix[gt_idx, pd_idx] += 1

            if gt_digit == pd_digit:
                matched += 1

    return matched, total


def evaluate_numeric_with_confusion(
    df_true: pd.DataFrame, df_pred: pd.DataFrame, numeric_cols
) -> dict:
    """Builds a confusion matrix for digits (0-9) across specified numeric columns.
    Computes an overall digit-level accuracy, and also provides per-column stats.

    :param df_true: Ground-truth DataFrame.
    :param df_pred: Predicted (AI) DataFrame.
    :param numeric_cols: List of numeric column names.
    :return: Dict:
        {
          "digit_level_accuracy": float,
          "confusion_matrix": a 10x10 numpy array,
          "per_column": {
              col_name: {
                  "digit_level_accuracy": float,
                  "confusion_matrix": 10x10 array
              },
              ...
          }
        }
    """
    master_confusion = np.zeros((10, 10), dtype=int)

    overall_matched = 0
    overall_total = 0

    per_column_stats = {}

    for col in numeric_cols:
        col_conf = np.zeros((10, 10), dtype=int)
        col_matched = 0
        col_total = 0

        for i in range(len(df_true)):
            true_val = df_true[col].iloc[i]
            pred_val = df_pred[col].iloc[i]

            m, t = compare_digits_with_confusion(true_val, pred_val, col_conf)
            compare_digits_with_confusion(true_val, pred_val, master_confusion)

            col_matched += m
            col_total += t

        col_acc = col_matched / col_total if col_total > 0 else 0.0
        per_column_stats[col] = {
            "digit_level_accuracy": col_acc,
            "confusion_matrix": col_conf,
        }

        overall_matched += col_matched
        overall_total += col_total

    overall_acc = overall_matched / overall_total if overall_total > 0 else 0.0

    return {
        "digit_level_accuracy": overall_acc,
        "confusion_matrix": master_confusion,
        "per_column": per_column_stats,
    }


def analyze_digit_confusion(confusion_matrix: np.ndarray):
    """Print info about digit confusion: top confusions, etc.

    :param confusion_matrix: 10x10 array (rows=GT digit, cols=predicted digit).
    """
    print("Digit Confusion Matrix (rows=GT, cols=Prediction):")
    print(confusion_matrix)
    print()

    row_sums = confusion_matrix.sum(axis=1)
    for digit in range(10):
        total_count = row_sums[digit]
        if total_count == 0:
            continue
        row = confusion_matrix[digit]
        sorted_preds = sorted(range(10), key=lambda x: row[x], reverse=True)

        top_pred = sorted_preds[0]
        top_count = row[top_pred]

        if len(sorted_preds) > 1:
            second_pred = sorted_preds[1]
            second_count = row[second_pred]
        else:
            second_pred = None
            second_count = 0

        print(f"Ground Truth Digit: {digit}")
        print(f"  Most predicted as: {top_pred} ({top_count} times)")
        if digit != top_pred:
            print(f"  --> This indicates confusion of {digit} -> {top_pred}")
        if second_pred is not None:
            print(f"  Second predicted as: {second_pred} ({second_count} times)")
        print()


def compare_chars_with_confusion(
    true_str: str, pred_str: str, confusion_matrix: np.ndarray, char_list: str
) -> None:
    """Compare two strings character by character, updating confusion_matrix
    (size = len(char_list) x len(char_list)).

    :param true_str: Ground-truth text string.
    :param pred_str: Predicted text string.
    :param confusion_matrix: 2D array with dimensions = len(char_list).
    :param char_list: A string or list of characters (e.g. ascii_lowercase).
    """
    t_str = true_str.lower()
    p_str = pred_str.lower()

    min_len = min(len(t_str), len(p_str))
    for i in range(min_len):
        gt_char = t_str[i]
        pd_char = p_str[i]
        if gt_char in char_list and pd_char in char_list:
            gt_idx = char_list.index(gt_char)
            pd_idx = char_list.index(pd_char)
            confusion_matrix[gt_idx, pd_idx] += 1


def evaluate_text_with_char_confusion(
    df_true: pd.DataFrame, df_pred: pd.DataFrame, text_cols, char_list: str
) -> dict:
    """For each text column, build a character-level confusion matrix.
    Also track exact string match rate per column.

    :param df_true: Ground-truth DataFrame.
    :param df_pred: Predicted (AI) DataFrame.
    :param text_cols: List of text column names.
    :param char_list: String or list of characters to track.
    :return: Dict containing:
        {
          "per_column": {
              col: {
                  "char_confusion_matrix": ...,
                  "exact_match_rate": ...
              }, ...
          },
          "master_char_confusion": 2D array aggregated across all text cols
        }
    """
    size = len(char_list)
    master_confusion = np.zeros((size, size), dtype=int)

    per_col_results = {}

    for col in text_cols:
        col_conf = np.zeros((size, size), dtype=int)

        exact_matches = 0
        total_rows = len(df_true)

        for i in range(total_rows):
            true_str = str(df_true[col].iloc[i])
            pred_str = str(df_pred[col].iloc[i])

            compare_chars_with_confusion(true_str, pred_str, col_conf, char_list)
            compare_chars_with_confusion(
                true_str, pred_str, master_confusion, char_list
            )

            # Check exact match ignoring case/whitespace around edges
            if true_str.strip().lower() == pred_str.strip().lower():
                exact_matches += 1

        exact_rate = exact_matches / total_rows if total_rows > 0 else 0.0

        per_col_results[col] = {
            "char_confusion_matrix": col_conf,
            "exact_match_rate": exact_rate,
        }

    return {"per_column": per_col_results, "master_char_confusion": master_confusion}


def analyze_char_confusion(confusion_matrix: np.ndarray, char_list: str) -> None:
    """Print or interpret a character confusion matrix (rows=GT char, cols=Pred).

    :param confusion_matrix: A 2D array of shape (len(char_list), len(char_list)).
    :param char_list: String or list of characters used in the confusion matrix.
    """
    row_sums = confusion_matrix.sum(axis=1)

    print(
        "Character Confusion Matrix (rows=GT, cols=Prediction). Shape:",
        confusion_matrix.shape,
    )
    print()

    for i, row_total in enumerate(row_sums):
        if row_total == 0:
            continue
        gt_char = char_list[i]
        row = confusion_matrix[i]

        # sort predicted chars by frequency
        sorted_preds = sorted(range(len(char_list)), key=lambda x: row[x], reverse=True)
        top_pred_idx = sorted_preds[0]
        top_count = row[top_pred_idx]

        # second-most predicted
        second_pred_idx = sorted_preds[1] if len(sorted_preds) > 1 else None
        second_count = row[second_pred_idx] if second_pred_idx is not None else 0

        top_pred_char = char_list[top_pred_idx]

        print(f"Ground Truth '{gt_char}' (count in GT = {row_total})")
        print(f"  Most commonly predicted as: '{top_pred_char}' (count={top_count})")

        if top_pred_char != gt_char:
            print(f"    --> Confusion: '{gt_char}' -> '{top_pred_char}'")

        if second_pred_idx is not None:
            second_pred_char = char_list[second_pred_idx]
            if top_pred_char == gt_char:
                print(
                    f"  Second most predicted (possible confusion): '{second_pred_char}' (count={second_count})"
                )
            else:
                print(
                    f"  Second predicted: '{second_pred_char}' (count={second_count})"
                )
        print()


def evaluate_numeric_errors(
    df_true: pd.DataFrame, df_pred: pd.DataFrame, numeric_cols, debug=False
) -> dict:
    """Computes Mean Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE)
    for the specified numeric_cols, both overall and per-column.
    Also returns absolute errors by column for optional plotting.

    :param df_true: Ground-truth DataFrame.
    :param df_pred: AI-predicted DataFrame.
    :param numeric_cols: List of numeric column names.
    :param debug: If True, prints debug info when parsing fails.
    :return: Dict:
      {
        "overall_mae": float,
        "overall_mape": float,
        "per_column": {
            col_name: { "mae": float, "mape": float }
        },
        "abs_errors_by_col": { col_name: [list_of_abs_errors] }
      }
    """
    overall_abs_errors = []
    overall_pct_errors = []

    per_column_stats = {}
    abs_errors_by_col = {col: [] for col in numeric_cols}

    parse_fail_count = {col: 0 for col in numeric_cols}
    parse_success_count = {col: 0 for col in numeric_cols}

    for col in numeric_cols:
        col_abs_errors = []
        col_pct_errors = []

        for i in range(len(df_true)):
            true_val = df_true[col].iloc[i]
            pred_val = df_pred[col].iloc[i]

            # Attempt parse
            try:
                true_num = float(str(true_val).replace(",", "").strip())
            except:
                if debug:
                    print(
                        f"[DEBUG] Row {i}, col '{col}' -> Failed parse for true_val = {true_val!r}"
                    )
                parse_fail_count[col] += 1
                continue

            try:
                pred_num = float(str(pred_val).replace(",", "").strip())
            except:
                if debug:
                    print(
                        f"[DEBUG] Row {i}, col '{col}' -> Failed parse for pred_val = {pred_val!r}"
                    )
                parse_fail_count[col] += 1
                continue

            if (
                np.isnan(true_num)
                or np.isnan(pred_num)
                or np.isinf(true_num)
                or np.isinf(pred_num)
            ):
                if debug:
                    print(
                        f"[DEBUG] Row {i}, col '{col}' -> NaN or inf found, skipping."
                    )
                continue

            parse_success_count[col] += 1

            # Absolute error
            abs_err = abs(pred_num - true_num)
            col_abs_errors.append(abs_err)
            abs_errors_by_col[col].append(abs_err)
            overall_abs_errors.append(abs_err)

            # Percentage error if true_num != 0
            if true_num != 0:
                pct_err = abs_err / abs(true_num)
                col_pct_errors.append(pct_err)
                overall_pct_errors.append(pct_err)

        # MAE, MAPE for this column
        if len(col_abs_errors) > 0:
            col_mae = float(np.mean(col_abs_errors))
        else:
            col_mae = float("nan")

        if len(col_pct_errors) > 0:
            col_mape = float(np.mean(col_pct_errors))
        else:
            col_mape = float("nan")

        per_column_stats[col] = {"mae": col_mae, "mape": col_mape}

    # Overall
    if len(overall_abs_errors) > 0:
        overall_mae = float(np.mean(overall_abs_errors))
    else:
        overall_mae = float("nan")

    if len(overall_pct_errors) > 0:
        overall_mape = float(np.mean(overall_pct_errors))
    else:
        overall_mape = float("nan")

    if debug:
        print("\n[DEBUG] Parsing Summary:")
        for col in numeric_cols:
            print(
                f"  {col}: parse_success={parse_success_count[col]}, parse_fail={parse_fail_count[col]}"
            )
        print()

    return {
        "overall_mae": overall_mae,
        "overall_mape": overall_mape,
        "per_column": per_column_stats,
        "abs_errors_by_col": abs_errors_by_col,
    }


def plot_error_distribution(abs_errors_by_col: dict) -> None:
    """Plot histograms of absolute errors for each numeric column.

    :param abs_errors_by_col: Dict { col_name: [list_of_abs_errors, ...], ... }
    """
    num_cols = len(abs_errors_by_col)
    if num_cols == 0:
        print("No numeric columns to plot.")
        return

    fig, axes = plt.subplots(1, num_cols, figsize=(5 * num_cols, 4))
    if num_cols == 1:
        axes = [axes]

    for ax, (col, errors) in zip(axes, abs_errors_by_col.items()):
        ax.hist(errors, bins=20, color="blue", alpha=0.7)
        ax.set_title(f"Absolute Error: {col}")
        ax.set_xlabel("Error")
        ax.set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()


def main():
    """Example main function to demonstrate usage of the above functions.

    Adjust numeric_cols, text_cols, and file paths as needed.
    All paths are relative by default.
    """
    df_human_path = "1940human.csv"
    df_ai_path = "1940raw.csv"

    numeric_columns = ["YEAR", "CONGRESSIONAL_DISTRICT", "VOTES"]
    text_columns = ["STATE", "RACE_TYPE", "CANDIDATE_NAME", "CANDIDATE_PARTY"]

    df_human = pd.read_csv(df_human_path)
    df_ai = pd.read_csv(df_ai_path)

    # 1) Overall accuracy (digit-level + Levenshtein)
    base_results = evaluate_accuracy(df_human, df_ai, numeric_columns, text_columns)
    print("== Overall Accuracy ==")
    print("Digit-Level Accuracy:", base_results["digit_level_accuracy"])
    print("Average Levenshtein Distance:", base_results["avg_levenshtein_dist"])
    print("-------------------------------------")

    # 2) Numeric confusion
    num_conf_res = evaluate_numeric_with_confusion(df_human, df_ai, numeric_columns)
    print("== Numeric Confusion ==")
    print("Digit-Level Accuracy (via confusion):", num_conf_res["digit_level_accuracy"])
    analyze_digit_confusion(num_conf_res["confusion_matrix"])
    print("-------------------------------------")

    # 3) Text character confusion
    char_list = string.ascii_lowercase
    txt_conf_res = evaluate_text_with_char_confusion(
        df_human, df_ai, text_columns, char_list
    )
    print("== Text Confusion ==")
    analyze_char_confusion(txt_conf_res["master_char_confusion"], char_list)
    for col, info in txt_conf_res["per_column"].items():
        print(f"Column: {col}, Exact Match Rate: {info['exact_match_rate']:.2f}")
    print("-------------------------------------")

    # 4) Error metrics (MAE / MAPE) + distribution
    err_res = evaluate_numeric_errors(df_human, df_ai, numeric_columns, debug=False)
    print("== Numeric Error Metrics ==")
    print("Overall MAE:", err_res["overall_mae"])
    print("Overall MAPE:", err_res["overall_mape"])
    for col, stats in err_res["per_column"].items():
        print(f"  {col}: MAE={stats['mae']:.2f}, MAPE={stats['mape']:.2f}")
    # Plot distribution:
    plot_error_distribution(err_res["abs_errors_by_col"])
    print("-------------------------------------")


if __name__ == "__main__":
    main()
