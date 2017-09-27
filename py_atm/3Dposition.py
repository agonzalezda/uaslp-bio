import ScrolledText as tkst
from numpy import*
from numpy.linalg import*
import cv2
import image

def get2Dp(img,method,umb,r,camera): # Obtener un punto centro de un circulo en una imagen
    img,img_s = image.preProccesing(img,False, True, method,umb)
    cv2.imwrite("seg" + str(camera) + ".jpg",img_s)
    cx,cy,nc = image.findVisualCue(img_s,2000,100000,r) # En esta funcion se puede seleccionar el area a tomar en cuenta
    if(nc>0):
        centers = zeros((nc,2))
        for j in range(nc):
            centers[j,0] = cx[j]
            centers[j,1] = cy[j]
            cv2.circle(img,(int(centers[j,0]),int(centers[j,1])),18,(255,255,0),-1)
        return img, True, centers
    else:
        return img, False,  0


def main():
    num_images = 5 # Numero de imagenes para la calibracion
    path = "images"
    i = 0
    method = 'th'
    umb = 100
    r = 0.7  # centricidad. entre mas cerca al 1 solo detectara circulos perfectos, entre mas cerca al 0 detecta objectos diferentes a circulos

    point2d_cam1 = zeros((num_images,2))
    point2d_cam2 = zeros((num_images,2))
    print point2d_cam1
    
    while(i<num_images):

        i = i + 1
        img_name1 = str(path) + "/calib_cam1_" + str(i) + ".jpg"
        img_name2 = str(path) + "/calib_cam2_" + str(i) + ".jpg"

        img1 = cv2.imread(img_name1,0)
        img2 = cv2.imread(img_name2,0)
        
        img1,success1,center1=get2Dp(img1,method,umb,r,1)
        img2,success2,center2=get2Dp(img2,method,umb,r,2)

        # Aqui puede poner una funcion que ordene los circulos segun su posicion.

    
        # Copia los circulos a la matriz principal
        if success1:
            print "Points in camera 1"
            print center1
            point2d_cam1[i-1,0] = center1[0,0]  # copiar x
            point2d_cam1[i-1,1] = center1[0,1]  # copiar y
        else:
            print "Points in camera 1 not avaliable"
        if success2:
            print "Points in camera 2"
            print center2
            point2d_cam2[i-1,0] = center2[0,0] # copiar x
            point2d_cam2[i-1,1] = center2[0,1] # copiar y
        else:
            print "Points in camera 2 not avaliable"

        
        cv2.imshow('img1', img1)
        cv2.imshow('img2', img2)
        opcion = cv2.waitKey()
        if opcion == 27:
            break

    print
    print "Points 2D camera 1"
    print point2d_cam1
    print "Points 2D camera 2"
    print point2d_cam2
    savetxt("data2D_cam1.txt", point2d_cam1, delimiter = ",", fmt = "%1.4f")
    savetxt("data2D_cam2.txt", point2d_cam2, delimiter = ",", fmt = "%1.4f")
    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
