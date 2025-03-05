class Article:
    def __init__(self, template, title, category="uncategorized"):
        self.template = template
        self.title = title
        self.category = "uncategorized" if category == None else category

    def __repr__(self):
        return f'Article(title="{self.title}")'