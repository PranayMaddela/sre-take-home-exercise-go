# Fetch SRE Take-Home Exercise

This project implements a service health checker for HTTP endpoints using a YAML configuration, designed to evaluate endpoint availability and log results every 15 seconds. It meets the requirements of the Fetch Rewards Site Reliability Engineering (SRE) take-home assignment.

## ✅ Features

- Accepts a YAML configuration via command-line argument.
- Parses each endpoint's method, headers, and body as defined in the config.
- Checks availability based on:
  - HTTP status code between `200` and `299`
  - Response time ≤ 500 milliseconds
- Cumulatively tracks availability for each domain (ignores port numbers).
- Logs availability reports **every 15 seconds**, regardless of endpoint count or latency.

---

## 📂 YAML Configuration Format

Example `sample.yaml`:

```yaml
- name: sample body up
  method: POST
  url: https://example.com/body
  headers:
    content-type: application/json
  body: '{"foo":"bar"}'

- name: sample index up
  url: https://example.com/

- name: sample body down
  method: POST
  url: https://example.com/body
  body: "{}"

- name: sample error down
  url: https://example.com/error
```

---

## 🚀 How to Run

### 1. Install Dependencies

```bash
pip install requests pyyaml
```

### 2. Run the Script

```bash
python main.py sample.yaml
```

> The script will continuously log availability results every 15 seconds.

---

## 🛠 Improvements Made to Original Code

| Issue Identified | Fix Implemented |
|------------------|------------------|
| Method not defaulting | Added default `GET` when method is missing |
| Port numbers in domain | Used `urlparse().hostname` to clean domain |
| Cumulative tracking missing | Used dictionary to track domain stats over time |
| Response time not considered | Measured response duration and filtered by 500ms |
| No error handling or timeout | Set request timeout to 0.5 seconds |
| Full endpoint marshaled as body | Used only the `body` string as request payload |

---

## 🧪 Output Example

```text
Availability Report:
example.com has 75% availability
```

---

## 📎 Notes

- The script is designed to run indefinitely (until interrupted via `Ctrl+C`).
- Availability is calculated as a whole number (e.g., 67%), per assignment instructions.

---

## 📤 Submission

- All code and documentation are submitted through a public Git repository.
- No external AI tools were used in writing or debugging the code.