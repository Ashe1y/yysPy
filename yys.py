import pyautogui as pg
import cv2 as cv
import time
import os
import numpy as np
import random

# 初始化变量，用于记录游戏中的挑战次数、胜利次数、失败次数，以及休眠时间
challengeCont = 1  # 挑战次数
control = False  # 控制打印
winCont = 0  # 胜利次数
defeatCont = 0  # 失败次数

def find_image_center(image_path, screen, threshold=0.5):
    """
    在屏幕中查找图像的中心位置。

    参数:
    image_path -- 图像文件的路径。
    screen -- 屏幕截图的图像数据。
    threshold -- 匹配的阈值，默认为0.5。

    返回:
    如果找到的图像匹配度超过阈值，则返回图像的中心坐标；否则返回None。
    """
    # 读取模板图像
    template = cv.imread(image_path, cv.IMREAD_UNCHANGED)
    template_gray = cv.cvtColor(template, cv.COLOR_BGR2GRAY)

    # 转换屏幕截图为灰度图像
    screen_gray = cv.cvtColor(screen, cv.COLOR_BGR2GRAY)

    # 进行模板匹配
    result = cv.matchTemplate(screen_gray, template_gray, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    # 检查匹配结果是否超过阈值
    if max_val >= threshold:
        top_left = max_loc
        w, h = template_gray.shape[::-1]

        # 生成匹配区域内的随机点
        random_x = random.randint(top_left[0], top_left[0] + w - 1)
        random_y = random.randint(top_left[1], top_left[1] + h - 1)

        return (random_x, random_y)

    else:
        return None

def prints():
    """
    打印当前的游戏统计信息。
    """
    print("--------------------------------------")
    print(f"第{challengeCont}次挑战")
    print("--------------------------------------")
    print(f"胜利{winCont}")
    print(f"失败{defeatCont}")
    print(f"共挑战{challengeCont-1}次")
    print("--------------------------------------")

while True:
    # 按任意键开始
    print("按任意键开始")
    k = input()

    while True:
        # 定义游戏各个状态的图像路径
        challenge = r'D:\yys\challenge.png'
        defeat = r'D:\yys\defeat.png'
        end = r'D:\yys\end.png'
        exits = r'D:\yys\exit.png'
        fight = r'D:\yys\fight.png'
        win = r'D:\yys\win.png'

        # 打印当前游戏统计信息
        prints()

        # 在屏幕中寻找挑战按钮
        challengeing = find_image_center(challenge, cv.cvtColor(np.array(pg.screenshot()), cv.COLOR_RGB2BGR))
        if challengeing:
            # 点击挑战按钮
            pg.click(challengeing)
            challengeCont += 1
            time.sleep(random.randint(5, 8))
            while True:
                # 在屏幕中寻找战斗按钮
                fighting = find_image_center(fight, cv.cvtColor(np.array(pg.screenshot()), cv.COLOR_RGB2BGR))
                if fighting:
                    print(f"战斗中...")
                    time.sleep(random.randint(3, 8))

                    # 在屏幕中寻找失败和胜利的标志
                    defeating = find_image_center(defeat, cv.cvtColor(np.array(pg.screenshot()), cv.COLOR_RGB2BGR))
                    wining = find_image_center(win, cv.cvtColor(np.array(pg.screenshot()), cv.COLOR_RGB2BGR))
                    if wining:
                        # 如果发现胜利标志，记录胜利并进行后续操作
                        print(f"战斗胜利")
                        winCont += 1
                        pg.click(wining)
                        time.sleep(random.randint(3, 5))
                        ending = find_image_center(end, cv.cvtColor(np.array(pg.screenshot()), cv.COLOR_RGB2BGR))
                        pg.click(ending)
                        print("结束")
                        time.sleep(random.randint(3, 5))
                        break

                    if defeating:
                        # 如果发现失败标志，记录失败并进行后续操作
                        print(f"失败")
                        defeatCont += 1
                        pg.click(defeating)
                        time.sleep(2)
                        break
        else:
            # 如果未找到挑战按钮，打印未找到的信息
            print(f"未找到图像 {challenge}")
            time.sleep(3)
