from manage import scheduler


def initialize_scheduler():
    if not scheduler.state:
        scheduler.start()
