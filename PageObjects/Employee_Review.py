class EmployeeReview:
    def __init__(self, *args):
        self.args = args
        self.employee_review_page = ("XPATH", "//h5[normalize-space()='Employee Reviews']")