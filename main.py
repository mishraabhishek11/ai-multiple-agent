from agent.manager import run_manager


def main():

    print("=" * 50)
    print(" INTELLIGENT MULTI-AGENT SYSTEM")
    print("=" * 50)

    task = input(
        "\nEnter your task: "
    )
    try:
        state = run_manager( task ) 

    except ValueError as e:
        print(f"\nValidation error: {e}")

    return

    print("\n" + "=" * 50)
    print(" RESEARCH")
    print("=" * 50)
    print(state["research"])

    print("\n" + "=" * 50)
    print(" CODE")
    print("=" * 50)
    print(state["code"])

    print("\n" + "=" * 50)
    print(" REVIEW")
    print("=" * 50)
    print(state["review"])


if __name__ == "__main__":
    main()
