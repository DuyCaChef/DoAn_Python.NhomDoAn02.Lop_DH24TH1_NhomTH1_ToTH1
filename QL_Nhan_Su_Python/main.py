from gui.login_window import LoginWindow
from gui.form_employee import App


def run_app():
    """Start the application: show login window, then open main app on success."""

    def on_login_success():
        # This will be called after login window is destroyed
        app = App()
        app.mainloop()

    login = LoginWindow(on_login_success=on_login_success)
    login.mainloop()


if __name__ == '__main__':
    run_app()

    