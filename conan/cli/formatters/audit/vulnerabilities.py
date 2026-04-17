import json

from jinja2 import select_autoescape, Template

from conan.api.output import cli_out_write, Color


severity_order = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}


def text_vuln_formatter(result):

    pass


def json_vuln_formatter(result):
    pass


def _render_vulns(vulns, template):
    pass


vuln_html = """
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Conan Audit Vulnerabilities Report</title>
  <link rel="stylesheet" href="https://cdn.datatables.net/2.3.4/css/dataTables.dataTables.min.css">
  <style>
    body { margin: 0; padding: 0; font-family: Arial, sans-serif; background: #333; color: #ffffff; }
    .container { width: 95%; margin: 40px auto; padding: 20px; background: #222; box-shadow: 0 2px 5px rgba(0,0,0,0.1); border-radius: 8px; }
    h1 { text-align: center; margin-bottom: 20px; }
    table { width: 100%; border-collapse: collapse; margin-bottom: 20px; table-layout: fixed; padding-top: 10px;}
    col[data-dt-column="0"] { width: 10%; }
    col[data-dt-column="1"] { width: 10%; }
    col[data-dt-column="2"] { width: auto; }
    thead { background: #333; color: #fff; }
    thead th { padding: 12px; text-align: left; }
    tbody tr { border-bottom: 1px solid #ddd; }
    tbody tr:hover { background: #f0f0f0; }
    td { padding: 10px; vertical-align: top; white-space: normal; word-wrap: break-word; overflow-wrap: break-word; word-break: break-word;}
    .severity-badge { padding: 2px 4px; border-radius: 4px; color: #fff; font-weight: bold; display: inline-block; }
    .severity-Critical { background: #d9534f; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { box-shadow: 0 0 0 0 rgba(217,83,79,0.7); } 70% { box-shadow: 0 0 0 12px rgba(217,83,79,0); } 100% { box-shadow: 0 0 0 0 rgba(217,83,79,0); } }
    .severity-High { background: #f0ad4e; }
    .severity-Medium { background: #f7ecb5; color: #333; }
    .severity-Low { background: #5cb85c; }
    .footer { text-align: center; color: #666; margin-bottom: 10px; }
    a { color: #007bff; text-decoration: none; }
    a:hover { text-decoration: underline; }
    .jfrog-research-summary { padding: 10px; border-radius: 6px; margin-bottom: 10px; border: 1px solid #555; }
    .jfrog-research-details { margin-top: 10px; }
  </style>
  <script
    src="https://code.jquery.com/jquery-3.7.1.min.js"
    integrity="sha256-/JqT3SQfawRcv/BIHPThkBvs0OEvtFFmqPF/lYI/Cxo="
    crossorigin="anonymous"></script>
  <script src="https://cdn.datatables.net/2.3.4/js/dataTables.min.js"></script>
  <script>
    $(document).ready(function(){
      $('#vuln_table').DataTable({
        "columnDefs": [
          { "orderable": true, "targets": [0, 1] },
          { "orderable": false, "targets": [2] }
        ],
        "order": [[1, "desc"]],
        "autoWidth": false,
      });
    });
  </script>
</head>
<body>
  <div class="container">
    <h1>Conan Audit Vulnerabilities Report</h1>
    <table id="vuln_table" class="stripe">
      <colgroup>
        <col class="pkg-col">
        <col class="info-col">
        <col class="desc-col">
      </colgroup>
      <thead>
        <tr>
          <th>Package</th>
          <th>Info</th>
          <th>Description</th>
        </tr>
      </thead>
      <tbody>
      {% for vuln in vulns %}
        {% set parts = vuln.severity.split(' - ') %}
        {% set severity_id = parts[0] %}
        {% set severity_label = parts[1] if parts|length > 1 else parts[0] %}
        <tr>
          <td>
            {{ vuln.package }}
          </td>
          <td>
            <span style="display: none">{{ vuln.preferred_score }}</span>
            {% if vuln.severity not in ['N/A', ''] %}
              <span class="severity-badge severity-{{ severity_label }}">{{ severity_label }} {% if vuln.preferred_score %}({{ vuln.preferred_score }}){% endif %}</span>
            {% else %}
              {{ vuln.severity }}
            {% endif %}
            <br>
            <br>
            {% if vuln.withdrawn %}
                <span style="color: #00ced1; font-weight: bold;">[WITHDRAWN]</span><br>
            {% endif %}
            <b>{{ vuln.vuln_id }}</b>
            {% if vuln.score_v3 %}<br/>CVSS <i>v3</i>: {{ vuln.score_v3 }}{% endif %}
            {% if vuln.score_v4 %}<br/>CVSS <i>v4</i>: {{ vuln.score_v4 }}{% endif %}
          </td>
          <td>
            {% for research in vuln.advisories %}
                {% if research.shortDescription %}
                <div class="jfrog-research-summary">
                    <strong>Summary provided by JFrog Research <span style="color: green">({{ research.name }})</span></strong>
                    <div class="jfrog-research-details">
                        <b>Short description:</b> {{ research.shortDescription }}<br>
                        {% if research.severity %}
                            <b>Impact severity:</b> <span class="severity-badge severity-{{ research.severity }}">{{ research.severity }}</span><br>
                            {% if research.impactReasons %}
                                <b>Impact reasons:</b>
                                <ul>
                                {% for reason in research.impactReasons %}
                                    <li style="color: {{ 'inherit' if reason.isPositive else 'red' }};">{{ reason.name }}</li>
                                {% endfor %}
                                </ul>
                            {% endif %}
                        {% endif %}
                        {% if vuln.provider_url %}
                            {% set expected_url = vuln.provider_url.rstrip('/') + '/ui/catalog/vulnerabilities/details/' + research.name %}
                            <b>More info available in:</b> <a href="{{ expected_url }}" target="_blank">{{ expected_url }}</a><br>
                        {% endif %}
                    </div>
                </div>
                {% endif %}
            {% endfor %}
            <strong>Description:</strong>
            <br>
            {{ vuln.description }}
            {% if vuln.publishedAt %}
                <br>
                <br>
                <strong>Published at:</strong> {{ vuln.publishedAt }}
            {% endif %}
            {% if vuln.fixVersions %}
                <div class="fix-versions-section">
                    <br>
                    <strong>Fixed in version(s):</strong>
                    <br>
                    {% for version in vuln.fixVersions %}
                        <span class="severity-badge severity-Medium">{{ version }}</span>
                    {% endfor %}
                </div>
            {% endif %}
            {% if vuln.references %}
              <br><strong>References:</strong>
              <ul>
                {% for ref in vuln.references %}
                  <li><a href="{{ ref }}" target="_blank">{{ ref }}</a></li>
                {% endfor %}
              </ul>
            {% endif %}
            {% if vuln.aliases %}
              <br><strong>Aliases:</strong> {{ ', '.join(vuln.aliases) }}
            {% endif %}
          </td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    <div class="footer">
      <p>Vulnerability information provided by JFrog Advanced Security. Please check <a href="https://jfrog.com/advanced-security/" target="_blank">https://jfrog.com/advanced-security/</a> for more information.</p>
      <p>You can send questions and report issues about the returned vulnerabilities to <a href="mailto:conan-research@jfrog.com">conan-research@jfrog.com</a>.</p>
      <p>Conan version: {{ version }}</p>
    </div>
  </div>
</body>
</html>
"""


def html_vuln_formatter(result):
    pass
