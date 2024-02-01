
    #YOLO format validation   ----Not all test case covered for this validation function!!!!---
def yoloCheck(splited):
        if type(splited)!=list:
            return False
        # Each line in yolo contains five numbers, first int, later four float
        if len(splited)!=5:
            return False
        if not splited[0].isdigit():
            return False
        for i in range(1,5):
            if (float(splited[i])>1.0 or float(splited[i])<0.0):
                return False
        return True
        