from apscheduler.schedulers.background import (
    BackgroundScheduler
)


def start_cleanup_scheduler(
    app
):

    scheduler = (
        BackgroundScheduler(
            daemon=True
        )
    )

    def cleanup():

        with app.app_context():

            app.session_manager\
                .cleanup_expired()

    scheduler.add_job(
        cleanup,
        "interval",
        minutes=5,
        id="session-cleanup",
        replace_existing=True
    )

    scheduler.start()

    return scheduler