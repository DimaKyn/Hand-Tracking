import HandTrackingControlClassTypeOne as htcc1
import HandTrackingControlClassTypeTwo as htcc2






def main():
    while True:
        global CURR_OPERATION
        print("mode1")
        control_class1 = htcc1.HandControl()
        control_class1.Hand_Control()

        print("mode2")
        control_class2 = htcc2.HandControl()
        control_class2.Hand_Control()



if __name__ == "__main__":
    main()
