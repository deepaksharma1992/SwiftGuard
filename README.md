# SwiftGuard – Multi-Agent SWIFT Transaction Processing System

SwiftGuard is a multi-agent AI system designed to automate validation, fraud detection, analysis, and reporting of SWIFT financial transactions using structured agentic workflows.

This project demonstrates practical implementation of advanced agent design patterns applied to real-world financial message processing.

---

## Project Overview

International banks process thousands of SWIFT messages daily. These transactions must be:

- Validated for format and compliance
- Screened for fraud
- Analyzed through multi-step reasoning
- Structured into actionable reports

SwiftGuard implements a complete end-to-end processing pipeline using four distinct agent design patterns.

---

## System Architecture

The system processes transactions in the following sequence:

1. **Evaluator–Optimizer Pattern**  
   Validates SWIFT messages using an LLM-based EvaluatorAgent and corrects malformed messages using an LLM-based OptimizerAgent.

2. **Parallelization Pattern**  
   Executes multiple fraud detection agents concurrently and aggregates risk results.

3. **Prompt Chaining Pattern**  
   Performs multi-stage fraud reasoning using progressive agents:
   - Initial Screener
   - Technical Analyst
   - Risk Assessor
   - Compliance Officer
   - Final Reviewer

4. **Orchestrator–Worker Pattern**  
   Delegates structured tasks to worker agents and generates final report artifacts.

---

## Agent Patterns Implemented

### 1. Evaluator–Optimizer Pattern

- `EvaluatorAgent` (LLM-based validation)
- `SwiftCorrectionAgent` (LLM-based repair)
- Iterative correction loop
- Manual review fallback for complex failures

All validation and correction is agent-driven (no hardcoded fixes).

---

### 2. Parallel Fraud Detection

Fraud agents executed concurrently:

- FraudAmountDetectionAgent
- FraudPatternDetectionAgent
- GeographicRiskAgent

Features:
- ThreadPoolExecutor-based concurrency
- Risk aggregation agent
- Fraud status classification

---

### 3. Prompt Chaining Workflow

Each agent builds upon the previous output:

1. Initial Screening
2. Technical Analysis
3. Risk Assessment
4. Compliance Review
5. Final Decision

Structured JSON responses ensure traceability and explainability.

---

### 4. Orchestrator–Worker Pattern

- Orchestrator creates structured task plans
- Generic workers execute tasks
- Two filtered report sets generated:
  - Clean transactions
  - High-value transactions

---

## Generated Reports

After execution, the system generates persistent report files:
- report_clean_messages.json
- report_high_value_messages.json



Each report contains:
- Timestamp
- Filter type
- Message count
- Orchestrator analysis
- Worker execution results

These reports serve as durable system artifacts beyond console output.

---


## Technology Stack

- Python 3.11+
- OpenAI API
- ThreadPoolExecutor
- Pydantic
- dotenv
- JSON structured outputs
