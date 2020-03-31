import tensorflow as tf
import numpy as np
import os,glob,cv2
from tkinter import *
from tkinter.filedialog import askdirectory
import tkinter.filedialog
import tkinter.messagebox

root = Tk()
root.title('淮扬菜识别')
filename=''
def xz():
    global filename
    filename = tkinter.filedialog.askopenfilename()
    if filename != '':
        lb.config(text = "您选择的文件是："+filename,font=("Monaco", 16))
        func()
    else:
        lb.config(text = "您没有选择任何文件",font=("Monaco", 16))

image_size = 64
num_channels = 3
images = []


def func():
    global filename
    global images

    # path = './training_data/yangzhou_fried_ices/yangzhouchaofan4.jpg'
    print(filename)
    if filename[-3:] != 'jpg' and filename[-3:] != 'png' and filename[-4:] != 'jpeg' and filename[-3:] != 'gif' and filename[-3:] != 'raw':
        tkinter.messagebox.showinfo('错误', '非法的图片格式')
        return
    image = cv2.imread(filename)
    # Resizing the image to our desired size and preprocessing will be done exactly as done during training
    image = cv2.resize(image, (image_size, image_size), 0, 0, cv2.INTER_LINEAR)
    images.append(image)
    images = np.array(images, dtype=np.uint8)
    images = images.astype('float32')
    images = np.multiply(images, 1.0 / 255.0)
    # The input to the network is of shape [None image_size image_size num_channels]. Hence we reshape.
    x_batch = images.reshape(1, image_size, image_size, num_channels)

    ## Let us restore the saved model
    sess = tf.Session()
    # Step-1: Recreate the network graph. At this step only graph is created.
    saver = tf.train.import_meta_graph('./huaiyang_cuisine/huaiyang_cuisine.ckpt-7900.meta')
    # Step-2: Now let's load the weights saved using the restore method.
    saver.restore(sess, './huaiyang_cuisine/huaiyang_cuisine.ckpt-7900')

    # Accessing the default graph which we have restored
    graph = tf.get_default_graph()

    # Now, let's get hold of the op that we can be processed to get the output.
    # In the original network y_pred is the tensor that is the prediction of the network
    y_pred = graph.get_tensor_by_name("y_pred:0")

    ## Let's feed the images to the input placeholders
    x = graph.get_tensor_by_name("x:0")
    y_true = graph.get_tensor_by_name("y_true:0")
    y_test_images = np.zeros((1, 7))

    ### Creating the feed_dict that is required to be fed to calculate y_pred
    feed_dict_testing = {x: x_batch, y_true: y_test_images}
    result = sess.run(y_pred, feed_dict=feed_dict_testing)
    # result is of this format [probabiliy_of_rose probability_of_sunflower]
    # dog [1 0]
    res_label = ['番茄炒蛋', '糖醋排骨', '韭菜炒蛋', '蚂蚁上树', '水金肴肉', '松鼠桂鱼', '扬州炒饭']
    print(res_label[result.argmax()])
    lab=Label(root,text=res_label[result.argmax()],font=("Monaco", 16))
    lab.pack()
    images=[]


lb0 = Label(root,text = '松鼠桂鱼/水金肴肉/蚂蚁上树/韭菜炒蛋/番茄炒饭/糖醋排骨/扬州炒饭',font=("Monaco", 16))
lb = Label(root,text = '文件格式支持jpg/png/gif',font=("Monaco", 16))
lb0.pack()
lb.pack()
btn1 = Button(root,text="浏览本地图片",command=xz,font=("Monaco", 16))
# btn2= Button(root,text="开始识别",command=func)
btn1.pack()
# btn2.pack()
root.mainloop()