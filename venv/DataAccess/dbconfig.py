from DataAccess.db import DBContext


class DbConfig:
    __ctx = DBContext()

    def __init__(self):
        pass

    def get_search_term(self):
        """Fetch a list of keyword from Database

                Returns:
                    a list of keyword
        """

        search_terms = 'search_terms'
        return self.__ctx.find_all(search_terms)
