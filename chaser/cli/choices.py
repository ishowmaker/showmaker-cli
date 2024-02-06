import typer


def choices_select(choices):
    """
    Prompt the user to select a choice from a list of choices.
    :param choices:
    :return:
    """
    while True:
        user_input = typer.prompt("Enter the number of your choice (q to quit):")
        if user_input.lower() == "q":
            break

        try:
            index = int(user_input)
            if 1 <= index <= len(choices):
                return choices[index - 1]
            else:
                typer.echo("Invalid choice. Please try again.")
        except ValueError:
            typer.echo("Invalid input. Please try again.")
