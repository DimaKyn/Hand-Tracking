import HandTrackingControlClassTypeOne as htcc1
import HandTrackingControlClassTypeTwo as htcc2


def main():
    while True:
        control_class = htcc1.HandControl()
        control_class.Hand_Control()

        control_class = htcc2.HandControl()
        control_class.Hand_Control()


if __name__ == "__main__":
    main()
