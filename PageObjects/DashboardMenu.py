class Dashboard_Menu:
    def __init__(self, *args):
        self.args = args
        self.logo_image = ("CLASS_NAME", "oxd-brand-banner")
        self.dashboard_item = ("XPATH", f"//a[normalize-space()='{args[0]}']")
        self.dashboard_item_count = ("CLASS_NAME", "oxd-main-menu-item-wrapper")
