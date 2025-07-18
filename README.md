# 📦 Terraform Drift Detection Script

This Python script automates the process of detecting infrastructure drift using Terraform. It runs `terraform init`, `terraform plan`, and parses the resulting plan to determine if any configuration drift exists.

---

## 📋 Features

* Initializes the Terraform working directory
* Creates and parses a Terraform plan
* Detects if drift exists (i.e., if changes would be applied)
* Prints a full plan if drift is found
* Exits with:

  * `0` if **no drift**
  * `1` if **drift detected** or errors occur

---

## 🚀 Usage

### 1. ✅ Prerequisites

* Python 3.7+
* Terraform installed (`terraform` must be in your `PATH`)
* Terraform configuration present in the directory defined by `$TF_DATA_DIR`

### 2. 📂 Environment Variable

You must set the `TF_DATA_DIR` environment variable before running the script. It should point to your Terraform configuration directory:

```bash
export TF_DATA_DIR="/path/to/your/terraform/config"
```

### 3. ▶️ Run the Script

```bash
python3 terraform_drift_check.py
```

> Replace `terraform_drift_check.py` with your actual filename.

---

## 🧠 What It Does

1. **Initialize Terraform**:

   ```bash
   terraform -chdir=$TF_DATA_DIR init
   ```

2. **Create a Terraform Plan**:

   ```bash
   terraform -chdir=$TF_DATA_DIR plan -out plan.txt
   ```

3. **Convert Plan to JSON**:

   ```bash
   terraform -chdir=$TF_DATA_DIR show --json plan.txt > plan.json
   ```

4. **Parse `plan.json`** and check:

   * Was the plan complete?
   * Did it detect changes (drift)?

5. **Prints full plan if drift is found** and exits with `1`.

---

## 📁 Output Files

* `plan.txt`: The raw Terraform plan
* `plan.json`: JSON version of the plan for parsing

---

## ❌ Exit Codes

* `0`: No drift
* `1`: Drift detected or an error occurred

---

## 🛠 Logging

Logs are printed to the console with timestamps and severity:

```
2025-07-14 12:34:56 [INFO] Initializing Terraform...
```

---

## 📄 License

MIT 
