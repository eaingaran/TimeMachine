from interactor import MasterInteractor as master


def start_time_machine():
    master.hello()
    print("Hello!")
    master.open_user_interface()


if __name__ == '__main__':
    start_time_machine()
