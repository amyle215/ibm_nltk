import sys
from PyQt5.QtWidgets import QApplication
from view import View
from controller import Controller
from model import Model


def main():
    """Main function."""
    # Create an instance of QApplication
    mt_app = QApplication(sys.argv)
    # Show the calculator's GUI
    view = View()
    view.show()
    # Create instances of the model and the controller
    model = Model()
    Controller(model=model, view=view)
    # Execute the calculator's main loop
    sys.exit(mt_app.exec_())


if __name__ == '__main__':
    main()
