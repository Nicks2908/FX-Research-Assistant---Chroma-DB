



def qa_prompt(
        question,
        context,
        history
):

    return f"""
Conversation History:
{history}

Context:
{context}

Question:
{question}
"""


def analyst_prompt(
        question,
        context,
        history
):

    return f"""
You are a Senior Forex Strategist.

Analyze the report.

Provide:

1. Executive Summary

2. Bullish Factors

3. Bearish Factors

4. Trading Opportunities

5. Risk Assessment

6. Conclusion

Conversation History:
{history}

Context:
{context}

Question:
{question}
"""

def executive_summary_prompt(
        context
):

    return f"""
Create an executive summary.

Include:

- Market Overview
- Currency Outlook
- Risks
- Opportunities

Context:

{context}
"""

def risk_prompt(
        context
):

    return f"""
Identify:

1. Macro Risks

2. Political Risks

3. Monetary Policy Risks

4. Liquidity Risks

Context:

{context}
"""

def trade_prompt(
        context
):

    return f"""
Extract all trade recommendations.

Return:

| Pair |
| Direction |
| Entry |
| Target |
| Stop Loss |
| Risk Reward |

Context:

{context}
"""

def compare_prompt(
        context
):

    return f"""
Compare all uploaded reports.

Provide:

1. Agreements

2. Disagreements

3. Consensus Outlook

Context:

{context}
"""


def outlook_prompt(
        context
):

    return f"""
Generate Weekly Forex Outlook.

Include:

USD
EUR
GBP
JPY
AUD
INR

Context:

{context}
"""