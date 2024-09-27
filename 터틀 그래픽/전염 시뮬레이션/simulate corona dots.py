import turtle
import random

tur = []
pos_x =[]
pos_y = []
hwak_list = []
hwak_dt = []
day = 1

N=int(input("얼마만큼의 인원을 배치 하겠습니까?"))
#N = 100 
n=int(input("첫 감염자는 몇명으로 하시겠습니까?"))
#n = 1
input_p=float(input("확진률은 몇 %로 하시겠습니까?"))
p=input_p//10
#p = 0.1
nMin=int(input("최소 확진자는 몇명으로 하시겠습니까"))
#nMin = 1
nMax=int(input("최대 확진자는 몇명으로 하시겠습니까"))
#nMax = 5

i = 0
while True:
    t1 = turtle.Turtle()
    if i == 0:
        screen = t1.getscreen()
        screen.setup(600, 600)
    t1.shape("circle")
    t1.speed("fastest")
    t1.penup()

    tmp_x = random.randint(-250, 250)
    tmp_y = random.randint(-250, 250)
    t1.goto(tmp_x, tmp_y)

    close_fg = False
    chk_cnt = len(pos_x)
    for i in range(chk_cnt):
        ds = t1.distance(pos_x[i], pos_y[i])
        if ds < 1:
            close_fg = True

    if close_fg:
        t1.hideturtle()
        print("근접 발생")
        continue

    tur.append(t1)
    pos_x.append(tmp_x)
    pos_y.append(tmp_y)
    i += 1
    print("t"+str(i), end=" ")

    if i >= N-1:
        break

    print(tmp_x, tmp_y)

# 1일차 감염자 붉은색 표시
for i in range(n):
    rnum = random.randrange(0, N)
    if hwak_list.count(rnum):
        n += 1
        continue
    tur[rnum].color("red")
    print("1일차 감염자 :", rnum)
    hwak_list.append(rnum)
    hwak_dt.append(1)

# 확진자 리스트를 날수별로 복사해서 반복문 실행
day_hwak_list = hwak_list[:]
print("day_hwak_list:", day_hwak_list)
print("hwak_list:", hwak_list)

while True:
    for i in day_hwak_list:
        print("확진자 :", i)
        idx = i
        m = random.randrange(nMin, nMax+1)
        print("접촉자 :", m, "명")

        # 확진자 기준 거리 계산, 리스트 생성
        ds_list = []
        ds_list.clear()
        for j in range(0, N):
            ds = tur[idx].distance(pos_x[j], pos_y[j])
            ds_list.append(ds)

        #확진자 본인의 거리는 0이지만, 최소값 제외를 위해서 10000 으로 입력
        ds_list[idx] = 10000
        l = 0
        for j in range(0, N):
            tmp_idx = ds_list.index(min(ds_list))
            if hwak_list.count(tmp_idx):
                ds_list[tmp_idx] = 10000
                l += 1
                continue
            else:
                print("접촉 :", idx, "-", tmp_idx)
                ds_list[tmp_idx] = 10000

                #감염여부 판단, 기준확률 p
                rp = random.randrange(0,100)
                if rp < p*100:
                    hwak_list.append(tmp_idx)
                    tur[tmp_idx].color("blue")
                    hwak_dt.append(day)
                    print("감염 : ", tmp_idx)
                l += 1
            # 접촉자 수가 차면 반복문 종료
            if l >= m:
                break

    print("day", day, "end")
    print("")
    day += 1

    day_hwak_list = hwak_list[:]
    print("day_hwak_list:", day_hwak_list)
    print("hwak_list:", hwak_list)

    if len(hwak_list) >= N-1:
        break

print(hwak_list)
print(hwak_dt)

turtle.mainloop()
