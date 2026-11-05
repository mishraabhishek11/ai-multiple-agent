from llm import call_llm
import json
def review(
    task,
    code
):

    prompt = f"""
You are a Reviewer Agent.

Review the following Python solution.

Task:
{task}

Solution:
{code}

Check:

1. Correctness
2. Python syntax
3. Logic
4. Missing issues
5. Possible improvements

Return ONLY valid JSON.

Use exactly this format:

{{
    "status": "approved",
    "feedback": "The solution is correct."
}}

OR:

{{
    "status": "needs_revision",
    "feedback": "Explain what needs to be changed."
}}

Use "approved" only when the solution
is acceptable.

Use "needs_revision" when the solution
requires a correction.
"""

    response = call_llm(
                messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.strip()
    

    return json.loads(result)

