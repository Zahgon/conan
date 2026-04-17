class RestRoutes:
    ping = "ping"
    common_search = "conans/search"
    common_authenticate = "users/authenticate"
    common_check_credentials = "users/check_credentials"

    def __init__(self):
        self.base = 'conans'

    @property
    def recipe(self):
        pass

    @property
    def recipe_latest(self):
        pass

    @property
    def recipe_revision(self):
        pass

    @property
    def recipe_revision_files(self):
        pass

    @property
    def recipe_revisions(self):
        pass

    @property
    def recipe_revision_file(self):
        pass

    @property
    def packages_revision(self):
        pass

    @property
    def package_recipe_revision(self):
        """Route for a package specifying the recipe revision but not the package revision"""
        pass

    @property
    def package_revisions(self):
        pass

    @property
    def package_revision(self):
        pass

    @property
    def package_revision_files(self):
        pass

    @property
    def package_revision_latest(self):
        pass

    @property
    def package_revision_file(self):
        pass

    @property
    def common_search_packages(self):
        pass

    @property
    def common_search_packages_revision(self):
        pass
