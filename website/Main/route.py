from views import MainViews

class MainRoute:
    @staticmethod
    def main(responce=None):
        return MainViews.main_display()

    @staticmethod
    def error_404(error):
        return MainViews.error_404_display(error)

    @staticmethod
    def error_500(error):
        return MainViews.error_500_display(error)
