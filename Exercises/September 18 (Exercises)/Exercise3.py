while True:
    x = int(input("Enter your marks: "))
    if x>79: ## If statement with merit first since code checks the condition of the input being above 80 first
        print("\nIt's a Merit!\n")
    elif x>39: ## Else if input is not 80 or above, print pass unless it is below 40
        print("\nIt's a Pass!\n")
    else: ## Numbers 39 and lesser are marked as fail
        print("\nIt's a Fail.\n")