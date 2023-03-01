class Dashboard_Menu:
    def __init__(self, *args):
        self.args = args
        self.logo_image = ("CLASS", "oxd-brand-banner")
        self.dashboard_menu = ("CLASS", "oxd-sidepanel-body")
        self.dashboard_item = ("XPATH", f"//a[normalize-space()='{args[0]}']")
        self.dashboard_item_count = ("CLASS", "oxd-main-menu-item-wrapper")
