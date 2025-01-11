#here will be a class for reporting
#class will be used to generate reports in html
import math
import os

from sklearn.metrics import confusion_matrix, roc_auc_score


class Reporting:
    def __init__(self, aid, path):
        self.path = path
        self.aid = aid

    def generate_report(self):
        if not os.path.exists(f"{self.path}/report"):
            os.makedirs(f"{self.path}/report")

        title = "Model Comparison Report"

        # Create and write to the HTML file
        with open(f"{self.path}/report/report.html", "w") as f:
            # Write basic HTML structure and styling
            f.write("""
            <!DOCTYPE html>
            <html lang='en'>
            <head>
                <meta charset='UTF-8'>
                <meta name='viewport' content='width=device-width, initial-scale=1.0'>
                <title>Model Comparison Report</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f8f9fa;
                        margin: 0;
                        padding: 0;
                    }
                    header {
                        background-color: #343a40;
                        color: #fff;
                        padding: 20px;
                        text-align: center;
                    }
                    header h1 {
                        margin: 0;
                    }
                    section {
                        padding: 20px;
                        margin: 20px auto;
                        background: #fff;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        max-width: 1200px;
                    }
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-bottom: 20px;
                    }
                    table th, table td {
                        border: 1px solid #ddd;
                        padding: 8px;
                        text-align: left;
                    }
                    table th {
                        background-color: #343a40;
                        color: white;
                    }
                    img {
                        max-width: 100%;
                        height: auto;
                        margin: 10px 0;
                        border-radius: 4px;
                        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
                    }
                    .image-row {
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        gap: 20px;
                        margin-bottom: 20px;
                    }
                    .image-row img {
                        flex: 1;
                        max-height: 400px;
                    }
                    .scrollable-container {
                        width: 100%;
                        height: 600px;
                        overflow: auto;
                        border: 1px solid #ccc;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <header>
                    <h1>Model Comparison Report</h1>
                </header>
            """)

            # Data analysis section
            f.write(f"""
            <section>
                <h2>Data Analysis</h2>
                <p><strong>Number of rows:</strong> {len(self.aid.X)}</p>
                <p><strong>Number of columns:</strong> {len(self.aid.X.columns)}</p>
            </section>
            """)

            # Preprocessing details section
            f.write("<section><h2>Preprocessing Details</h2><table>")
            for line in open(f"{self.path}/results/preprocessing_details.csv", 'r'):
                f.write("<tr>" + "".join(f"<td>{value.strip()}</td>" for value in line.split(",")) + "</tr>")
            f.write("</table></section>")

            # Feature distributions
            f.write("<section><h2>Feature Distributions</h2><div>")
            plots_path = os.path.join(self.path, 'distribution_plots')
            for plot_file in os.listdir(plots_path):
                if plot_file.endswith('.png'):
                    plot_path = f'../distribution_plots/{plot_file}'
                    f.write(f"<img src='{plot_path}' width='250' height='200'>")
            f.write("</div></section>")

            # Correlation matrix and correlation with target
            f.write(f"""
            <section>
                <h2>Correlation Analysis</h2>
                <h3>Correlation Matrix</h3>
                <img src='../correlation_plots/correlation_matrix.png' style="width: 600px; height: auto;">
                <h3>Correlation with {self.aid.y.name}</h3>
            """)
            for plot_file in os.listdir(os.path.join(self.path, 'correlation_plots')):
                if plot_file.endswith('.png') and plot_file != 'correlation_matrix.png':
                    plot_path = f'../correlation_plots/{plot_file}'
                    f.write(f"<img src='{plot_path}' width='250' height='200'>")
            f.write("</section>")

            # DataFrame head
            f.write("<section><h2>Data Frame Preview</h2><table><tr>")
            for col in self.aid.df_before.columns:
                f.write(f"<th>{col}</th>")
            f.write("</tr>")
            for row in self.aid.df_before.head().values:
                f.write("<tr>")
                for i, value in enumerate(row):
                    if math.isnan(value):
                        f.write("<td>NaN</td>")
                    else:
                        if self.aid.df_before.iloc[:, i].nunique() == 2:
                            f.write(f"<td>{int(value)}</td>")
                        else:
                            f.write(f"<td>{value}</td>")
                f.write("</tr>")
            f.write("</table></section>")

            # Models and metrics
            f.write(f"""
            <section>
                <h2>Models</h2>
                <p><strong>Models used:</strong> {', '.join(self.aid.models)}</p>
                <p><strong>Metric used:</strong> {self.aid.metric}</p>
                <h2>Model Ranking</h2>
                <table>
                    <tr>
                        <th>Model</th>
                        <th>Accuracy</th>
                        <th>Precision</th>
                        <th>Recall</th>
                        <th>F1</th>
                    </tr>
            """)
            for model in self.aid.best_metrics[['model', 'accuracy', 'precision', 'recall', 'f1']].values:
                f.write("<tr>" + "".join(f"<td>{value}</td>" for value in model) + "</tr>")
            f.write("</table></section>")
            f.write("""<section>
                    <h2>Explanation of Medical Metrics</h2>
                    <ul>
                        <li><strong>Sensitivity (Recall):</strong> Sensitivity measures how well the model identifies patients who truly have the disease. A higher sensitivity reduces the risk of false negatives, which is crucial in early detection of serious conditions.</li>
                        <li><strong>Specificity:</strong> Specificity measures how well the model identifies healthy patients. A higher specificity reduces the risk of false positives, preventing unnecessary treatments.</li>
                        <li><strong>Positive Predictive Value (PPV):</strong> PPV indicates the likelihood that a positive prediction is correct. A high PPV ensures that patients who are diagnosed as sick truly have the condition.</li>
                        <li><strong>Negative Predictive Value (NPV):</strong> NPV indicates the likelihood that a negative prediction is correct. A high NPV ensures that healthy patients are not incorrectly diagnosed.</li>
                        <li><strong>False Positive Rate (FPR):</strong> FPR measures the proportion of healthy patients incorrectly identified as having the disease. A high FPR can lead to unnecessary tests and treatments.</li>
                        <li><strong>False Negative Rate (FNR):</strong> FNR measures the proportion of sick patients who are incorrectly diagnosed as healthy. A high FNR can delay diagnosis and treatment, which may worsen patient outcomes.</li>
                        <li><strong>ROC-AUC Score:</strong> The ROC-AUC score evaluates the model's ability to distinguish between positive and negative cases across different thresholds. A higher ROC-AUC indicates better discriminatory performance of the model, especially in imbalanced datasets.</li>
                    </ul>
                </section>""")

            # Inside the section for each model
            for model in self.aid.best_models:
                # Calculate statistics for medical relevance
                y_pred = model.predict(self.aid.X_test)
                cm = confusion_matrix(self.aid.y_test, y_pred)
                tn, fp, fn, tp = cm.ravel()
                sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0  # Recall
                specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
                ppv = tp / (tp + fp) if (tp + fp) > 0 else 0  # Precision
                npv = tn / (tn + fn) if (tn + fn) > 0 else 0
                fpr = fp / (fp + tn) if (fp + tn) > 0 else 0
                fnr = fn / (fn + tp) if (fn + tp) > 0 else 0
                y_proba = model.predict_proba(self.aid.X_test)[:, 1]  # Compute probabilities for positive class
                roc_auc = roc_auc_score(self.aid.y_test, y_proba)

                # Write model statistics section
                f.write(f"""
                <section>
                    <h2>{model.__class__.__name__}</h2>
                    <h3>Model Performance Metrics</h3>
                    <!-- Medical Metrics Explanation -->
                    <ul>
                        <li><strong>Sensitivity (Recall):</strong> {sensitivity:.2f}</li>
                        <li><strong>Specificity:</strong> {specificity:.2f}</li>
                        <li><strong>Positive Predictive Value (PPV):</strong> {ppv:.2f}</li>
                        <li><strong>Negative Predictive Value (NPV):</strong> {npv:.2f}</li>
                        <li><strong>False Positive Rate (FPR):</strong> {fpr:.2f}</li>
                        <li><strong>False Negative Rate (FNR):</strong> {fnr:.2f}</li>
                        <li><strong>ROC-AUC Score:</strong> {roc_auc:.2f}</li>
                    </ul>
                    <div class="image-row">
                        <div>
                            <h3>Confusion Matrix</h3>
                            <img src='../confusion_matrix/{model.__class__.__name__}_confusion_matrix.png'>
                        </div>
                        <div>
                            <h3>Feature Importance</h3>
                """)
                if os.path.exists(
                        f"{self.path}/shap_feature_importance/{model.__class__.__name__}_custom_feature_importance.png"):
                    f.write(
                        f"<img src='../shap_feature_importance/{model.__class__.__name__}_custom_feature_importance.png'>")
                f.write("</div></div>")

                if model.__class__.__name__ == "DecisionTreeClassifier":
                    f.write("""
                    <h3>Tree Visualization</h3>
                    <div class="scrollable-container">
                        <img src="../plots/tree.svg" alt="Decision Tree Visualization">
                    </div>
                    """)
                f.write("</section>")

            # Close HTML
            f.write("</body></html>")
        return None

if __name__ == "__main__":
    from project.do_poprawy_code.medaid import medaid
    import pickle
    with open('medaid1/medaid.pkl', 'rb') as file:
        medaid = pickle.load(file)
    print(medaid.path)
    report = Reporting(medaid, medaid.path)
    report.generate_report()