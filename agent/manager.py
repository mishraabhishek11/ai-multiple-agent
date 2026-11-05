# Remove from openai import OpenAI
# Remove from dotenv import # 
# Remove load_dotenv
# Remove import os
# Added llm below
from llm import call_llm
# Added validation below
from validation import (
    validate_task
)

# Added Logger
from logger import logger

from workers.research_agent import research
from workers.coding_agent import write_code
from workers.reviewer_agent import review
from agent.state import create_state


# Remove load_dotenv()


# Remove client = OpenAI(
#  base_url=os.getenv("BASE_URL"),
#   api_key=os.getenv("API_KEY")
# ) 


# Remove MAX_REVISIONS = 3
# Added below line
from config import (
    MAX_REVISIONS
)



def choose_worker(state):

    prompt = f"""
You are the Manager Agent.

Your job is to decide which worker
should act NEXT.

Original Task:
{state["task"]}

Research:
{state["research"]}

Code:
{state["code"]}

Review:
{state["review"]}

History:
{state["history"]}

Revision Count:
{state["revision_count"]}

Maximum Revisions:
{MAX_REVISIONS}

Available workers:

research
coding
review
finish

Decision rules:

- If Research is empty, choose research.

- If Research exists and Code is empty, choose coding.

- If a Review exists with status
  "needs_revision" and the Revision count is below the maximum, choose coding.

- If Code exists and there is no Review, choose review.

- If the previous review requested
  revision and new code has been generated,  choose review again.

- If the latest Review status is
  "approved", choose finish.

- If the maximum revision count has
  been reached, choose finish.

Return ONLY one word:

research
coding
review
finish
"""
    # Modified to call_llm
    response = call_llm(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.strip().lower()
    


def run_manager(task):
    # Added validate_task here
    task = validate_task(task)
    state = create_state(
        task
    )
    # Added logger here
    logger.info(
    f"Starting manager for task: {task}"
    )


    while True:

        worker = choose_worker(
            state
        )
        # Logger added here
        logger.info(
    f"Manager selected: {worker}"
        )

        print(
            f"\nManager selected: {worker}"
        )

        if worker == "research":

            state["research"] = research(
                state["task"]
            )

            state["history"].append(
                "research"
            )

        elif worker == "coding":

            if (
            state["review"]
            and state["revision_count"]
            >= MAX_REVISIONS
            ):

                print(
                "Maximum revisions reached."
                )
                # Added Logger
                logger.warning(
        f"Maximum steps reached: {MAX_REVISIONS}"
                )


                break

            feedback = ""

            if state["review"]:

                feedback = state[
                "review"
                ].get(
                "feedback",
                ""
                )

            state["revision_count"] += 1

            state["code"] = write_code(
            state["task"],
            state["research"],
            feedback
            )

            state["review"] = ""

            state["history"].append(
            "coding"
            )

        elif worker == "review":

            state["review"] = review(
                state["task"],
                state["code"]
            )

            state["history"].append(
                "review"
            )

        elif worker == "finish":
            # Added Logger here
            logger.info(
            "Manager finished the workflow."
            )

            break

        else:

            raise ValueError(
                f"Unknown worker: {worker}"
            )

    return state
