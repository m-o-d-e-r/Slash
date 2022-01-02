from .views import AboutViews

class AboutRoute:
    @staticmethod
    def main(responce=None):
        return AboutViews.main_display()

    @staticmethod
    def error_404(error):
        return AboutViews.error_404_display(error)

    @staticmethod
    def error_500(error):
        return AboutViews.error_500_display(error)
