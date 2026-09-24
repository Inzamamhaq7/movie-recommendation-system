def choose_option(title, options):

    print(f"\n{title}")

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:

        try:
            choice = int(input("Enter choice: "))

            if 1 <= choice <= len(options):
                return options[choice - 1]

            print("Please choose a valid option.")

        except ValueError:
            print("Please enter a number.")