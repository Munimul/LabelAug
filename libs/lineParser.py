
def lineParse(splited,aug):
                listAug=['rotateC90','rotateC180','rotateC270','flipOnY']
                cla = int(splited[0])
                x_center = float(splited[1])
                y_center = float(splited[2])
                box_width = float(splited[3])
                box_height = float(splited[4])

                if (aug==listAug[0]): #rotateC90
                    new_xcenter= float(1-y_center)
                    new_ycenter= float(x_center)
                    new_width= box_height
                    new_height= box_width
                    return cla,new_xcenter,new_ycenter,new_width,new_height

                elif (aug==listAug[1]):#rotateC180
                    new_xcenter= float(1-x_center)
                    new_ycenter= float(1-y_center)
                    new_width= box_width
                    new_height= box_height
                    return cla,new_xcenter,new_ycenter,new_width,new_height
            
                elif (aug==listAug[2]):#rotateC270
                    new_xcenter= float(y_center)
                    new_ycenter= float(1-x_center)
                    new_width= box_height
                    new_height= box_width
                    return cla,new_xcenter,new_ycenter,new_width,new_height

                elif (aug==listAug[3]):#flipOnY
                    new_xcenter= float(1-x_center)
                    new_ycenter= float(y_center)
                    new_width= box_width
                    new_height= box_height
                    return cla,new_xcenter,new_ycenter,new_width,new_height

                else:
                    print("Not valid augmentation parameter! Try with 'C90', 'C180', 'C270' or 'FlipY' ")
                    return False
    
