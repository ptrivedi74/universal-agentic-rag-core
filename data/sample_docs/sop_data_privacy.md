# Enterprise Data Privacy & Security SOP

## 1. Data Classification
All enterprise data must be classified under one of the following categories:
* **Public:** Non-sensitive operational data.
* **Internal:** Internal communications and business workflows.
* **Restricted / PII:** Customer information, health records, and credentials.

## 2. Retention & Sanitization Policy
* Personnel records and customer data must not be stored in unencrypted plain-text files.
* Before passing enterprise documents to third-party Large Language Model (LLM) APIs, all personally identifiable information (PII)—including emails, national IDs, and phone numbers—must undergo automated redaction.