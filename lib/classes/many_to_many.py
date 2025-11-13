class Article:
    all = []

    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        # Use hasattr to make title immutable
        if not hasattr(self, '_title'):
            if isinstance(title, str) and 5 <= len(title) <= 50:
                self._title = title
            else:
                self._title = None  # Invalid title, but we'll set it anyway for non-exception mode
                if isinstance(title, str) and 5 <= len(title) <= 50:
                    self._title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # Title is immutable - only set if it doesn't exist yet
        if hasattr(self, '_title'):
            pass  # Do nothing, title is immutable
        else:
            if isinstance(value, str) and 5 <= len(value) <= 50:
                self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if isinstance(value, Author):
            self._author = value

    @property
    def magazine(self):
        return self._magazine

    @magazine.setter
    def magazine(self, value):
        if isinstance(value, Magazine):
            self._magazine = value
        
class Author:
    def __init__(self, name):
        # Use hasattr to make name immutable
        if not hasattr(self, '_name'):
            if isinstance(name, str) and len(name) > 0:
                self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Name is immutable - only set if it doesn't exist yet
        if hasattr(self, '_name'):
            pass  # Do nothing, name is immutable
        else:
            if isinstance(value, str) and len(value) > 0:
                self._name = value

    def articles(self):
        """Returns a list of all articles the author has written"""
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        """Returns a unique list of magazines the author has contributed to"""
        magazine_list = []
        for article in self.articles():
            if article.magazine not in magazine_list:
                magazine_list.append(article.magazine)
        return magazine_list

    def add_article(self, magazine, title):
        """Creates and returns a new Article instance"""
        article = Article(self, magazine, title)
        return article

    def topic_areas(self):
        """Returns a unique list of category strings, or None if no articles"""
        if len(self.articles()) == 0:
            return None
        categories = []
        for magazine in self.magazines():
            if magazine.category not in categories:
                categories.append(magazine.category)
        return categories

class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Name is mutable but must be validated
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        elif not hasattr(self, '_name'):
            # If setting for the first time and invalid, still need to set something
            self._name = value if isinstance(value, str) else ""

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        # Category is mutable but must be validated
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        elif not hasattr(self, '_category'):
            # If setting for the first time and invalid, still need to set something
            self._category = value if isinstance(value, str) else ""

    def articles(self):
        """Returns a list of all articles published in this magazine"""
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        """Returns a unique list of authors who have written for this magazine"""
        author_list = []
        for article in self.articles():
            if article.author not in author_list:
                author_list.append(article.author)
        return author_list

    def article_titles(self):
        """Returns a list of article title strings, or None if no articles"""
        articles = self.articles()
        if len(articles) == 0:
            return None
        return [article.title for article in articles]

    def contributing_authors(self):
        """Returns authors who have written more than 2 articles, or None"""
        articles = self.articles()
        if len(articles) == 0:
            return None

        # Count articles per author
        author_counts = {}
        for article in articles:
            if article.author in author_counts:
                author_counts[article.author] += 1
            else:
                author_counts[article.author] = 1

        # Filter authors with more than 2 articles
        prolific_authors = [author for author, count in author_counts.items() if count > 2]

        if len(prolific_authors) == 0:
            return None
        return prolific_authors

    @classmethod
    def top_publisher(cls):
        """Returns the Magazine instance with the most articles, or None"""
        if len(Article.all) == 0:
            return None

        if len(cls.all) == 0:
            return None

        # Find magazine with most articles
        max_magazine = None
        max_count = 0

        for magazine in cls.all:
            article_count = len(magazine.articles())
            if article_count > max_count:
                max_count = article_count
                max_magazine = magazine

        return max_magazine