# core/reporting.py
import json
import os
from datetime import datetime
from jinja2 import Template

class Reporter:
    """
    Génération de rapports JSON et HTML pour les runs des scrapers.
    """

    def __init__(self, output_dir="reports"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.json_path = os.path.join(self.output_dir, f"report_{timestamp}.json")
        self.html_path = os.path.join(self.output_dir, f"report_{timestamp}.html")
        self.data = {
            "timestamp": datetime.now().isoformat(),
            "queries": {}
        }

    def add_query_results(self, query: str, merged_results: list, stats_per_source: dict):
        self.data["queries"][query] = {
            "results": merged_results,
            "stats": stats_per_source
        }

    def save_json(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def save_html(self):
        template_str = """
        <html>
        <head>
            <meta charset="utf-8">
            <title>Scraping Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                h2 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
                th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
                th { background-color: #f5f5f5; }
                .status-OK { color: green; font-weight: bold; }
                .status-SKIPPED { color: orange; font-weight: bold; }
                .status-ERROR { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>Scraping Report - {{ timestamp }}</h1>
            {% for query, info in queries.items() %}
                <h2>{{ query }}</h2>
                <h3>Stats:</h3>
                <table>
                    <tr>
                        <th>Source</th>
                        <th>Count</th>
                        <th>Status</th>
                    </tr>
                    {% for source, stat in info.stats.items() %}
                        <tr>
                            <td>{{ source }}</td>
                            <td>{{ stat.count }}</td>
                            <td class="status-{{ stat.status }}">{{ stat.status }}</td>
                        </tr>
                    {% endfor %}
                </table>
                <h3>Results:</h3>
                <table>
                    <tr><th>Title</th><th>URL</th><th>Snippet</th></tr>
                    {% for item in info.results %}
                        <tr>
                            <td>{{ item.title }}</td>
                            <td><a href="{{ item.url }}" target="_blank">{{ item.url }}</a></td>
                            <td>{{ item.snippet }}</td>
                        </tr>
                    {% endfor %}
                </table>
            {% endfor %}
        </body>
        </html>
        """
        template = Template(template_str)
        html_content = template.render(timestamp=self.data["timestamp"], queries=self.data["queries"])

        with open(self.html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def save_all(self):
        self.save_json()
        self.save_html()
        return self.json_path, self.html_path


def generate_report(output_dir="reports"):
    return Reporter(output_dir)
