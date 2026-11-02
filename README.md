# FINC 3390 Financial Modeling — Fall 2026

A reusable Python workspace for financial-data analysis, visualization, and course projects.

The goal is to understand the pipeline behind a financial chart: retrieve data, validate it, transform it into meaningful measures, visualize it, and explain the result. The repository separates reusable functions from assignment notebooks so the analysis stays readable and reproducible.

## Repository map

```text
finance_tools/          Reusable Python functions
notebooks/homework/     Clean assignment notebooks
notebooks/midterm/      Midterm review and practice
notebooks/experiments/  Safe place to test ideas
examples/               Small runnable examples
tests/                  Checks for financial calculations
docs/                   Concept notes and attribution guidance
```

## Setup

1. Open Anaconda Prompt or a terminal.
2. Create an environment:

   ```bash
   conda create -n finc3390 python=3.12 -y
   conda activate finc3390
   pip install -r requirements.txt
   ```

3. Open the repository in VS Code or JupyterLab.
4. Select the `finc3390` Python kernel.
5. Run the tests:

   ```bash
   python -m unittest discover -s tests -v
   ```

6. Try the example:

   ```bash
   python examples/market_comparison.py
   ```

## Public-repository rules

- Do not commit student IDs, passwords, API keys, private data, or proprietary employer material.
- Sanitize assignment notebooks before publishing them.
- Cite outside code and keep its license notice.
- Do not post answer keys or another student's work.
- Verify downloaded data before drawing conclusions.

This repository is educational. It is not investment advice and should not be used as a production trading system.
