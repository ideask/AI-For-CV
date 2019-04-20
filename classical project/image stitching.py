import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt


# 右边图片以得到的单应性矩阵逆变换回与左图一致，然后线性拼接
# 对于重叠的区域，靠近左边的部分，让左边图像内容显示的多一些，
# 靠近右边的部分，让右边图像的内容显示的多一些。
def ImageMerge(srcImg, warpImg):
    rows, cols = srcImg.shape[:2]
    for col in range(0, cols):
        if srcImg[:, col].any() and warpImg[:, col].any():
            left = col
            break
    for col in range(cols - 1, 0, -1):
        if srcImg[:, col].any() and warpImg[:, col].any():
            right = col
            break
    output = np.zeros([rows, cols, 3], np.uint8)  # 初始化输出图像矩阵
    for row in range(0, rows):
        for col in range(0, cols):
            if not srcImg[row, col].any():
                output[row, col] = warpImg[row, col]
            elif not warpImg[row, col].any():
                output[row, col] = srcImg[row, col]
            else:
                srcImgLen = float(abs(col - left))
                testImgLen = float(abs(col - right))
                alpha = srcImgLen / (srcImgLen + testImgLen)
                output[row, col] = np.clip(srcImg[row, col] * (1 - alpha) + warpImg[row, col] * alpha, 0, 255)  # 限制灰度值不超[0,255]
    return output

def ImageStitching(left_img_dir, right_img_dir):
    #上下左右边界填充像素设定
    top, bot, left, right = 100, 100, 0, 500
    #读入图片
    left_image = cv.imread(left_img_dir)
    right_image = cv.imread(right_img_dir)
    # 扩充图像的边界（填黑）
    left_image_bord = cv.copyMakeBorder(left_image, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))#常数填充：边界填充黑色
    right_image_bord = cv.copyMakeBorder(right_image, top, bot, left, right, cv.BORDER_CONSTANT, value=(0, 0, 0))#常数填充：边界填充黑色
    left_image_bord_gray = cv.cvtColor(left_image_bord, cv.COLOR_BGR2GRAY)#转成灰度图
    right_image_bord_gray = cv.cvtColor(right_image_bord, cv.COLOR_BGR2GRAY)#转成灰度图

    # find the keypoints and descriptors with SIFT
    sift = cv.xfeatures2d_SIFT().create()#SIFT初始化
    kp1, des1 = sift.detectAndCompute(left_image_bord_gray, None)#descriptors（128维），keypoints
    kp2, des2 = sift.detectAndCompute(right_image_bord_gray, None)

    # FLANN parameters
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    flann = cv.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1, des2, k=2)

    # Need to draw only good matches, so create a mask
    matchesMask = [[0, 0] for i in range(len(matches))]
    good = [] #筛选出最佳匹配的点
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7*n.distance:#获得的K个最佳匹配中取出来第一个和第二个，进行比值，比值小于0.7，则为好的匹配点
            good.append(m)
            matchesMask[i] = [1, 0] #匹配连线（最佳点有效）

    #画图参数设定，单个点颜色是红色，连线点为绿色，matchesMask只匹配最佳点（最佳点有效），flags连线样式
    draw_params = dict(matchColor=(0, 255, 0), singlePointColor=(255, 0, 0), matchesMask=matchesMask, flags=0)
    #画特征点匹配连线图
    match_img = cv.drawMatchesKnn(left_image_bord_gray, kp1, right_image_bord_gray, kp2, matches, None, **draw_params)


    MIN_MATCH_COUNT = 10
    if len(good) > MIN_MATCH_COUNT:
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        # 利用RANSAC算法获得最佳的单应性矩阵
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
        # 利用上面得到的单应性矩阵对右图进行逆变换
        warpImg = cv.warpPerspective(right_image_bord, np.array(M), (right_image_bord.shape[1], right_image_bord.shape[0]), flags=cv.WARP_INVERSE_MAP)
        #图像重叠部分线性合并
        output_img = ImageMerge(left_image_bord, warpImg)

    else:
        print("Not enough matches are found - {}/{}".format(len(good), MIN_MATCH_COUNT))
        output_img = None

    return output_img, match_img


if __name__ == '__main__':
    output_img, match_img = ImageStitching('left.jpg', 'right.jpg')
    # opencv is bgr, matplotlib is rgb
    output_img = cv.cvtColor(output_img, cv.COLOR_BGR2RGB)
    # show the result
    plt.figure()
    plt.subplot(1, 2, 1)
    plt.imshow(match_img)
    plt.subplot(1, 2, 2)
    plt.imshow(output_img)
    plt.show()
