="""accuracy_functions.py

Helper file of Python functions for measuring OCR accuracy on numeric and text fields.
No environment management or IPython-specific code is included.
"""

import string

import matplotlib.pyplot as plt
import numpy as np


def digit_level_accuracy(true_val, pred_val):
    """Compare two numeric values digit by digit, counting matches."""
    t_str, p_str = str(true_val), str(pred_val)
    matched, total = 0, len(t_str)
    for i in range(min(len(t_str), len(p_str))):
        if t_str[i] == p_str[i]:
            matched += 1
    return matched, total


def levenshtein_distance(s1, s2):
    """Compute minimum edit distance (insert/delete/substitute) between two strings."""
    if not s1:
        return len(s2)
    if not s2:
        return len(s1)
    rows, cols = len(s1) + 1, len(s2) + 1
    dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j
    for i in range(1, rows):
        for j in range(1, cols):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[-1][-1]


def evaluate_accuracy(df_true, df_pred, numeric_cols, text_cols):
    """Returns digit-level accuracy for numeric_cols and average Levenshtein distance for text_cols."""
    total_matched, total_digits = 0, 0
    for col in numeric_cols:
        for i in range(len(df_true)):
            m, t = digit_level_accuracy(df_true[col].iloc[i], df_pred[col].iloc[i])
            total_matched += m
            total_digits += t
    digit_acc = (total_matched / total_digits) if total_digits else 0

    lev_dist_sum, text_count = 0, 0
    for col in text_cols:
        for i in range(len(df_true)):
            true_s = str(df_true[col].iloc[i])
            pred_s = str(df_pred[col].iloc[i])
            lev_dist_sum += levenshtein_distance(true_s, pred_s)
            text_count += 1
    avg_lev_dist = (lev_dist_sum / text_count) if text_count else 0

    return {"digit_level_accuracy": digit_acc, "avg_levenshtein_dist": avg_lev_dist}


def compare_digits_with_confusion(true_val, pred_val, conf_mat):
    """Update digit confusion matrix (10x10) for two numeric values."""
    t_str, p_str = str(true_val), str(pred_val)
    matched, total = 0, len(t_str)
    for i in range(min(len(t_str), len(p_str))):
        if t_str[i].isdigit() and p_str[i].isdigit():
            gt, pd = int(t_str[i]), int(p_str[i])
            conf_mat[gt, pd] += 1
            if gt == pd:
                matched += 1
    return matched, total


def evaluate_numeric_with_confusion(df_true, df_pred, numeric_cols):
    """Return digit-level accuracy and a 10x10 confusion matrix for numeric columns."""
    master_conf = np.zeros((10, 10), dtype=int)
    overall_matched, overall_total = 0, 0
    for col in numeric_cols:
        for i in range(len(df_true)):
            m, t = compare_digits_with_confusion(
                df_true[col].iloc[i], df_pred[col].iloc[i], master_conf
            )
            overall_matched += m
            overall_total += t
    digit_acc = overall_matched / overall_total if overall_total else 0
    return {"digit_level_accuracy": digit_acc, "confusion_matrix": master_conf}


def analyze_digit_confusion(confusion_matrix):
    """Print a summary of digit confusion from a 10x10 matrix."""
    print("Digit Confusion Matrix (rows=GT digit, cols=Pred digit):")
    print(confusion_matrix, "\n")
    row_sums = confusion_matrix.sum(axis=1)
    for d in range(10):
        if row_sums[d] == 0:
            continue
        row = confusion_matrix[d]
        best = sorted(range(10), key=lambda x: row[x], reverse=True)
        print(f"Ground Truth {d}, top predicted {best[0]} ({row[best[0]]} times)")


def compare_chars_with_confusion(true_s, pred_s, conf_mat, char_list):
    """Update char confusion matrix for each matching position."""
    t_s, p_s = true_s.lower(), pred_s.lower()
    for i in range(min(len(t_s), len(p_s))):
        gt, pd = t_s[i], p_s[i]
        if gt in char_list and pd in char_list:
            g_idx, p_idx = char_list.index(gt), char_list.index(pd)
            conf_mat[g_idx, p_idx] += 1


def evaluate_text_with_char_confusion(
    df_true, df_pred, text_cols, char_list=string.ascii_lowercase
):
    """Return character confusion and exact match rates for text columns."""
    size = len(char_list)
    master = np.zeros((size, size), dtype=int)
    per_col = {}
    for col in text_cols:
        col_conf = np.zeros((size, size), dtype=int)
        exact_matches, rows = 0, len(df_true)
        for i in range(rows):
            ts = str(df_true[col].iloc[i])
            ps = str(df_pred[col].iloc[i])
            compare_chars_with_confusion(ts, ps, col_conf, char_list)
            compare_chars_with_confusion(ts, ps, master, char_list)
            if ts.strip().lower() == ps.strip().lower():
                exact_matches += 1
        per_col[col] = {
            "char_confusion_matrix": col_conf,
            "exact_match_rate": exact_matches / rows if rows else 0,
        }
    return {"per_column": per_col, "master_char_confusion": master}


def analyze_char_confusion(conf_mat, char_list):
    """Print a summary of top confusions from a character confusion matrix."""
    print("Character Confusion Matrix shape:", conf_mat.shape)
    row_sums = conf_mat.sum(axis=1)
    for i, rsum in enumerate(row_sums):
        if rsum == 0:
            continue
        sorted_preds = sorted(
            range(len(char_list)), key=lambda x: conf_mat[i][x], reverse=True
        )
        print(f"GT '{char_list[i]}' -> top pred '{char_list[sorted_preds[0]]}'")


def evaluate_numeric_errors(df_true, df_pred, numeric_cols):
    """Compute MAE/MAPE for numeric cols, returning overall plus per-col stats."""
    overall_abs, overall_pct = [], []
    col_stats = {c: {"abs": [], "pct": []} for c in numeric_cols}
    for col in numeric_cols:
        for i in range(len(df_true)):
            try:
                tv = float(str(df_true[col].iloc[i]).replace(",", "").strip())
                pv = float(str(df_pred[col].iloc[i]).replace(",", "").strip())
                abs_err = abs(pv - tv)
                col_stats[col]["abs"].append(abs_err)
                overall_abs.append(abs_err)
                if tv != 0:
                    pct_err = abs_err / abs(tv)
                    col_stats[col]["pct"].append(pct_err)
                    overall_pct.append(pct_err)
            except:
                pass
    # Summaries
    results = {}
    mae_all = np.mean(overall_abs) if overall_abs else np.nan
    mape_all = np.mean(overall_pct) if overall_pct else np.nan
    per_col = {}
    for c in numeric_cols:
        ma = np.mean(col_stats[c]["abs"]) if col_stats[c]["abs"] else np.nan
        mp = np.mean(col_stats[c]["pct"]) if col_stats[c]["pct"] else np.nan
        per_col[c] = {"mae": ma, "mape": mp}
    return {
        "overall_mae": mae_all,
        "overall_mape": mape_all,
        "per_column": per_col,
        "abs_errors_by_col": {c: col_stats[c]["abs"] for c in numeric_cols},
    }


def plot_error_distribution(abs_errors_by_col):
    """Plot histograms of absolute errors for each numeric column."""
    ncols = len(abs_errors_by_col)
    if ncols == 0:
        return
    fig, axes = plt.subplots(1, ncols, figsize=(5 * ncols, 4))
    if ncols == 1:
        axes = [axes]
    for ax, (col, errs) in zip(axes, abs_errors_by_col.items()):
        ax.hist(errs, bins=20, color="blue", alpha=0.7)
        ax.set_title(f"Absolute Error: {col}")
        ax.set_xlabel("Error")
        ax.set_ylabel("Frequency")
    plt.tight_layout()
    plt.show()
