class Category:
    def __init__(self, name):
        if len(name) > 30:
            raise ValueError("Category name should not exceed 30 characters")

        self.name = name
        self.ledger = list()
    
    
    def __str__(self):
        title_line = self.name.center(30, "*")

        transactions_str = str()
        total = float()
        for transaction in self.ledger:
            description = transaction["description"][:23] if len(transaction["description"]) >= 23 else transaction["description"]
            amount = transaction["amount"]
            transactions_str = transactions_str + "\n{:23s}{:7.2f}".format(description, amount)
            total = total + transaction["amount"]
        
        category_total = "\nTotal: {:.2f}".format(total)
        
        return title_line + transactions_str + category_total


    def deposit(self, amount, description = ""):
        if not isinstance(amount, (int, float)):
            raise TypeError("The 'amount' argument should be numeric")
        if not isinstance(description, str):
            raise TypeError("The 'description' argument should be a string")
        if amount <= 0:
            raise ValueError("Invalid deposit amount")
        
        self.ledger.append({"amount": amount, "description":description})
    
    def get_balance(self):
        return sum(transaction["amount"] for transaction in self.ledger) if len(self.ledger) > 0 else 0
    
    def check_funds(self, amount):
        if not isinstance(amount, (int, float)):
            raise TypeError("The 'amount' argument should be numeric")
        
        return True if amount <= self.get_balance() else False
    
    def withdraw(self, amount, description = ""):
        if not isinstance(amount, (int, float)):
            raise TypeError("The 'amount' argument should be numeric")
        if not isinstance(description, str):
            raise TypeError("The 'description' argument should be a string")
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")
        
        if self.check_funds(amount) is False: return False
        
        amount = amount * -1
        self.ledger.append({"amount": amount, "description": description})

        return True
    
    def transfer(self, amount, destination_category):
        if not isinstance(amount, (int, float)):
            raise TypeError("The 'amount' argument should be of type int or float")
        if not isinstance(destination_category, Category):
            raise TypeError("The 'destination_category' argument should be of type Category")
        if amount <= 0:
            raise ValueError("Invalid transfer amount")
        
        if self.check_funds(amount) is False: return False

        self.withdraw(amount, f"Transfer to {destination_category.name}")
        destination_category.deposit(amount, f"Transfer from {self.name}")

        return True


def create_spend_chart(categories):
    if not isinstance(categories, list):
        raise TypeError("The argument 'categories' should be of type list")


    # Compute the expenses per category and the total expenditure
    category_expenses = dict()
    total_expenditure = float()
    for category in categories:
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                withdrawal_amount = transaction["amount"] * -1
                category_expenses[category.name] = category_expenses.get(category.name, 0) + withdrawal_amount
                total_expenditure = total_expenditure + withdrawal_amount

    percentage_expenses = dict()
    for (category_name, expenditure) in category_expenses.items():
        percentage_expenses[category_name] = (expenditure / total_expenditure) * 100


    # Format the bar chart
    title_line = "Percentage spent by category\n"

    chart_grid = str()
    for n in range(10, -1, -1):
        chart_grid = chart_grid + "{:3d}| ".format(n*10)
        for category in categories:
            if int(percentage_expenses[category.name] / 10) >= n:
                chart_grid = chart_grid + "o  "
            else:
                chart_grid = chart_grid + "   "
        chart_grid = chart_grid + "\n"

    chart_base = "    -" + ("---" * len(categories))
    
    chart_labels = [list(category.name) for category in categories]
    label_lens = [len(label) for label in chart_labels]
    max_label_len = max(label_lens)
    label_grid = str()
    for x in range(max_label_len):
        label_grid = label_grid + "\n     "
        for y in range(len(chart_labels)):
            if x < label_lens[y]:
                label_grid = label_grid + chart_labels[y][x] + "  "
            else:
                label_grid = label_grid + "   "


    spend_chart = title_line + chart_grid + chart_base + label_grid
    
    return spend_chart
