import random
import math
import sys
import time
import numpy as np
import matplotlib.pyplot as plt

#inital condition
actual_width = 62.7
actual_height = 30.4
#virtual height width
# width = 627
width  =627
height = 304
radius = int(1.6 / actual_height * height)
hole_radius = int(width / actual_width * 2)
# Table coordinates
x1 = 100
y1 = 100
hole_positions = [(x1, y1), (x1 + width // 2, y1), (x1 + width, y1),
                  (x1, y1 + height), (x1 + width // 2, y1 + height), (x1 + width, y1 + height)]

vir_hole_positions = [(x1 + radius, y1 + radius), (x1 + width /2, y1 + radius), (x1 + width - radius, y1 + radius),
                      (x1 + radius, y1 + height - radius), (x1 + width / 2, y1 + height - radius), (x1 + width - radius, y1 + height - radius)]

actualwidth =62.7
actualheight=30.4
width=627
height=304
radius=int(1.6/actualheight*height)
holeradius=int(width/actualwidth*2)
holex=[x1,x1+width/2,x1+width,x1,x1+width/2,x1+width]
holey=[y1,y1,y1,y1+height,y1+height,y1+height]
virholex=[x1+radius,x1+width/2,x1+width-radius,x1+radius,x1+width/2,x1+width-radius]
virholey=[y1+radius,y1+radius,y1+radius,y1+height-radius,y1+height-radius,y1+height-radius]
# Distance and vector functions
def distance_and_vector(n1x, n1y, n2x, n2y):
    dx = n1x - n2x
    dy = n1y - n2y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return round(dist, 2), dx, dy
def point_to_vector(n1x, n1y, vector_x, vector_y, dot_x, dot_y):
    dist_to_vector = math.sqrt(vector_x ** 2 + vector_y ** 2)
    ball_to_ball_x = dot_x - n1x
    ball_to_ball_y = dot_y - n1y
    dot_product = vector_x * ball_to_ball_x + vector_y * ball_to_ball_y
    if dot_product >= 0:
        shadow_length = dot_product / dist_to_vector
        ratio = shadow_length / dist_to_vector
        shadow_x = n1x + vector_x * ratio
        shadow_y = n1y + vector_y * ratio
        normal_length = distance_and_vector(dot_x, dot_y, shadow_x, shadow_y)[0]
        return normal_length
    else:
        return -1
# Generate random balls
def is_overlapping(x, y, existing_balls, radius):
    for bx, by in existing_balls:
        if math.sqrt((x - bx) ** 2 + (y - by) ** 2) < 2 * radius:
            return True
    return False

def generate_balls(ball_count, radius):
    cuex = random.randint(x1 + radius, x1 + width - radius)
    cuey = random.randint(y1 + radius, y1 + height - radius)
    ball_positions = []

    while len(ball_positions) < ball_count:
        x = random.randint(x1 + radius, x1 + width - radius)
        y = random.randint(y1 + radius, y1 + height - radius)
        if not is_overlapping(x, y, ball_positions, radius):
            ball_positions.append((x, y))

    ballx_set = [pos[0] for pos in ball_positions]
    bally_set = [pos[1] for pos in ball_positions]

    return cuex, cuey, ballx_set, bally_set, ball_count

# Calculate aim point() 
def calculate_aim_point(ball_x, ball_y, target_x, target_y, ball_diameter):
    # 计算从球到目标的向量
    vector_x = target_x - ball_x
    vector_y = target_y - ball_y
    
    # 计算向量的长度
    length = math.sqrt(vector_x ** 2 + vector_y ** 2)
    
    # 计算单位向量（方向向量）
    unit_vector_x = vector_x / length
    unit_vector_y = vector_y / length
    
    # 计算一个球直径的距离
    aim_distance = 2*ball_diameter
    
    # 计算在球的后方一个直径的点
    aim_point_x = ball_x - unit_vector_x * aim_distance
    aim_point_y = ball_y - unit_vector_y * aim_distance
    
    return aim_point_x, aim_point_y

# Calculate distance from point to line segment
def point_to_line_distance(px, py, x1, y1, x2, y2, radius, i, j, value):
    dx = x2 - x1
    dy = y2 - y1
    apx = px - x1
    apy = py - y1
    d_mag_squared = dx ** 2 + dy ** 2
    if d_mag_squared == 0:
        dist = math.sqrt(apx ** 2 + apy ** 2)
        closest_point = (x1, y1)
    else:
        t = (apx * dx + apy * dy) / d_mag_squared
        if t < 0:       
            closest_point = (x1, y1)
            dist = math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
        elif t > 1:
            closest_point = (x2, y2)
            dist = math.sqrt((px - x2) ** 2 + (py - y2) ** 2)
        else:
            qx = x1 + t * dx
            qy = y1 + t * dy
            dist = math.sqrt((px - qx) ** 2 + (py - qy) ** 2)
    if dist <= radius:
        value += 1
        return value, px, py
    return value, 0, 0

# Function to find the minimum negative integer in a nested list
def find_min_negative_integer_in_nested_list(lst):
    min_negative = None
    min_position1 = None
    min_position2 = None

    for i, sublist in enumerate(lst):
        for j, value in enumerate(sublist):
            if isinstance(value, (int, float)) and value < 0:
                if min_negative is None or value > min_negative:
                    min_negative = value
                    min_position1, min_position2 = i, j

    return min_negative, min_position1, min_position2

def perpendicular_points(p_x, p_y, q_x, q_y, distance):
    # 计算向量 pq
    vector_pq_x = q_x - p_x
    vector_pq_y = q_y - p_y
    
    # 计算向量 pq 的垂直向量
    perpendicular_vector_x = -vector_pq_y
    perpendicular_vector_y = vector_pq_x
    
    # 计算垂直向量的模长
    magnitude = math.sqrt(perpendicular_vector_x**2 + perpendicular_vector_y**2)
    
    # 计算单位垂直向量
    unit_vector_x = perpendicular_vector_x / magnitude
    unit_vector_y = perpendicular_vector_y / magnitude
    
    # 计算左侧点位
    left_point_x = p_x + distance * unit_vector_x
    left_point_y = p_y + distance * unit_vector_y
    
    # 计算右侧点位
    right_point_x = p_x - distance * unit_vector_x
    right_point_y = p_y - distance * unit_vector_y
    
    return left_point_x, left_point_y, right_point_x, right_point_y

# Main game logic functions (main1 and main2)
def method1(cuex, cuey, objx, objy,ninex,niney,objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys ,values1, ballcount, ballx_set, bally_set):
    print("method1")
    routenumber=1
    judge_nine_way=False
    objtoholes = []
    vxs = []
    vys = []
    obj_hole_angles=[]
    cue_obj_angles=[]
    obj_ninehitpointxs=[]
    obj_ninehitpointys=[]
    for i in range(6):
        obj_hole_angle = vector_angle(objx,objy,ninex,niney,vir_hole_positions[i][0],vir_hole_positions[i][1])
        obj_ninehitpointx,obj_ninehitpointy=calculate_aim_point(objx,objy,ninehitpointxs[i],ninehitpointys[i],radius)
        obj_ninehitpointxs.append(obj_ninehitpointx)
        obj_ninehitpointys.append(obj_ninehitpointy)
        cue_obj_angle = vector_angle(cuex, cuey, obj_ninehitpointxs[i],obj_ninehitpointys[i],ninex,niney)
        if  cue_obj_angle <  100:
            cue_obj_angle=-cue_obj_angle
        cue_obj_angles.append(cue_obj_angle)
        if  obj_hole_angle < 100:
            obj_hole_angles.append(-obj_hole_angle)
        else:
            obj_hole_angles.append(obj_hole_angle)
        if cue_obj_angle < 0 and obj_hole_angles[i] < 0:
            judge_nine_way=True
    print("cue-nine-angle",cue_obj_angle)
    print("obj-hole_angle",obj_hole_angles)
    print("nine_way",judge_nine_way)
    if judge_nine_way==True:
        routenumber=1.1
        for i in range(6):
            cuetoobjdis, objtocuex, objtocuey = distance_and_vector(cuex, cuey, ninex,niney)
            obj_ninedis,_,_=distance_and_vector(objx,objy,ninex,niney)
            ninetohole, _,_= distance_and_vector(objx, objy, vir_hole_positions[i][0], vir_hole_positions[i][1])
            objtoholes.append(ninetohole)
            vxs.append(objtocuex)
            vys.append(objtocuey)
            
        #detect the obstacle on the route   
        main1_1obstacles = target_hole(objhitpointxs, objhitpointys, ballcount, ballx_set, bally_set,6)
        way1scores = []
        for i in range(6):
            way1score = cal_score(cuetoobjdis + objtoholes[i], obj_hole_angles[i], values1[i], main1_1obstacles[i])
            way1scores.append(way1score)
        print("way1scores",way1scores)
        #judge the kiss nine ball
        nine_to_hole_point=[]
        for i in range(6):
            nine_to_hole=calculate_aim_point(ninex,niney,vir_hole_positions[i][0],vir_hole_positions[i][1],radius)
            nine_to_hole_point.append(nine_to_hole)
        
        #pick the biggest and negative score(def)
        non_positive_scores = [score for score in way1scores if score <= 0]
        if non_positive_scores:
            max_non_positive_score = max(non_positive_scores)
            best_index = way1scores.index(max_non_positive_score)
            best_virholex = vir_hole_positions[best_index][0]
            best_virholey = vir_hole_positions[best_index][1]
            first_hitpointx = obj_ninehitpointxs[best_index]
            first_hitpointy = obj_ninehitpointys[best_index]
            final_hitpointx = ninehitpointxs[best_index]
            final_hitpointy = ninehitpointys[best_index]
            bestvx = vxs[best_index]
            bestvy = vys[best_index]
            routeobs = main1_1obstacles[best_index]
            hitcuepointx, hitcuepointy = calculate_aim_point(cuex, cuey, final_hitpointx, final_hitpointy, radius)
            finalobsx = []
            finalobsy = []
            countobs = 0
            for i in range(ballcount):
                countobs, px, py = point_to_line_distance(ballx_set[i], bally_set[i], objx, objy, best_virholex, best_virholey, 2 * radius, i, 1, countobs)
                if px > 0:
                    finalobsx.append(px)
                    finalobsy.append(py)
            cue_obstacle=edge_detect(hitcuepointx,hitcuepointy)
            final(routenumber,max_non_positive_score, bestvx, bestvy, routeobs, hitcuepointx, hitcuepointy,cue_obstacle)
            print("nine_way",judge_nine_way)
            linexs=[cuex,first_hitpointx,final_hitpointx,best_virholex]
            lineys=[cuey,first_hitpointy,final_hitpointy,best_virholey]
            screen2(ballcount,routenumber,3,linexs,lineys,obj_ninehitpointxs,obj_ninehitpointys,ninehitpointxs,ninehitpointys,cuex,cuey,objx,objy,ninex,niney)
            # screen1(ballcount,routenumber,obj_ninehitpointx,ninehitpointys,obj_ninehitpointxs,obj_ninehitpointys,ninehitpointxs,ninehitpointys,objx,objy,best_virholex,best_virholey,final_hitpointx,final_hitpointy,objx,objy)
            return max_non_positive_score, bestvx, bestvy, routeobs, hitcuepointx, hitcuepointy
        else:
            return method1(cuex, cuey, objx, objy, ninex,niney,objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys,values1, ballx_set, bally_set, ballcount)
    # else if:
    #     routenumber=1.2
#calculate the distance(cue,obj,holes)
    else:
        routenumber=1
        for i in range(6):
            cuetoobjdis, objtocuex, objtocuey = distance_and_vector(cuex, cuey, objhitpointxs[i],objhitpointys[i])
            objtohole, _,_= distance_and_vector(objx, objy, vir_hole_positions[i][0], vir_hole_positions[i][1])
            objtoholes.append(objtohole)
            vxs.append(objtocuex)
            vys.append(objtocuey)
        #calculate the angle(cue,obj)
        cue_obj_holeangle = []
        for i in range(6):
            cue_obj_hole1 = vector_angle(cuex, cuey, objx, objy, vir_hole_positions[i][0], vir_hole_positions[i][1])
            if cue_obj_hole1 < 100:
                cue_obj_holeangle.append(-cue_obj_hole1)
            else:
                cue_obj_holeangle.append(cue_obj_hole1)
        print("cue_obj_hole_angle",cue_obj_holeangle)
        #detect the obstacle on the route
        main1obstacles = target_hole(objhitpointxs, objhitpointys, ballcount, ballx_set, bally_set,6)
        way1scores = []
        for i in range(6):
            way1score = cal_score(cuetoobjdis + objtoholes[i], cue_obj_holeangle[i], values1[i], main1obstacles[i])
            way1scores.append(way1score)
        print("way1score",way1scores)
        #judge the kiss nine ball
        nine_to_hole_point=[]
        for i in range(6):
            nine_to_hole=calculate_aim_point(ninex,niney,vir_hole_positions[i][0],vir_hole_positions[i][1],radius)
            nine_to_hole_point.append(nine_to_hole)
        
        #pick the biggest and negative score
        non_positive_scores = [score for score in way1scores if score <= 0]
        if non_positive_scores:
            max_non_positive_score = max(non_positive_scores)
            best_index = way1scores.index(max_non_positive_score)
            best_virholex = vir_hole_positions[best_index][0]
            best_virholey = vir_hole_positions[best_index][1]
            final_hitpointx = objhitpointxs[best_index]
            final_hitpointy = objhitpointys[best_index]
            bestvx = vxs[best_index]
            bestvy = vys[best_index]
            routeobs = main1obstacles[best_index]
            hitcuepointx, hitcuepointy = calculate_aim_point(cuex, cuey, final_hitpointx, final_hitpointy, radius)
            finalobsx = []
            finalobsy = []
            countobs = 0
            for i in range(ballcount):
                countobs, px, py = point_to_line_distance(ballx_set[i], bally_set[i], objx, objy, best_virholex, best_virholey, 2 * radius, i, 1, countobs)
                if px > 0:
                    finalobsx.append(px)
                    finalobsy.append(py)
            cue_obstacle=edge_detect(hitcuepointx,hitcuepointy)
            final(routenumber,max_non_positive_score, bestvx, bestvy, routeobs, hitcuepointx, hitcuepointy,cue_obstacle)
            linexs=[cuex,final_hitpointx,best_virholex]
            lineys=[cuey,final_hitpointy,best_virholey]
            screen2(ballcount,routenumber,2,linexs,lineys,objhitpointxs,objhitpointys,ninehitpointxs,ninehitpointys,cuex,cuey,objx,objy,ninex,niney)
            return max_non_positive_score, bestvx, bestvy, routeobs, hitcuepointx, hitcuepointy
        else:
            return main2(cuex, cuey, objx, objy, ninex,niney,objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys, ballx_set, bally_set, ballcount)

def mirror_point(line_m, line_b, point):
    x1, y1 = point
    if line_m == 'inf':  # 直线垂直的情况
        x2 = line_b  # 这里 line_b 是 x 的值
        y2 = y1
    else:
        # 计算交点
        x2 = (line_m * (y1 - line_b) + x1) / (line_m**2 + 1)
        y2 = (line_m * x2 + line_b)
    
    # 计算镜像点
    x_mirror = 2 * x2 - x1
    y_mirror = 2 * y2 - y1
    
    return (x_mirror, y_mirror)

def segment_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # 計算每個線段的斜率和截距
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    # if denominator == 0:
    #     return None  # 兩線段平行或共線，無交點

    # 計算交點
    px = ((x1*y2 - y1*x2)*(x3 - x4) - (x1 - x2)*(x3*y4 - y3*x4)) / denominator
    py = ((x1*y2 - y1*x2)*(y3 - y4) - (y1 - y2)*(x3*y4 - y3*x4)) / denominator

    return px,py

# def kiss_nine_ball(cuex,cuey,objx,objy,ninex,niney,):
    
    
    
def main2(cuex, cuey, objx, objy,ninex,niney ,objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys, ballx_set, bally_set, ballcount):
    routenumber=2
    boundaries = [
    (x1,y1,x1+width,y1,cuex,cuey),  # top
    (x1,y1+height,x1+width,y1+height,cuex,cuey),  # bottom
    (x1,y1,x1,y1+height,cuex,cuey),  # left
    (x1+width,y1,x1+width,y1+height,cuex,cuey)  # right
    ]
    #slope斜率
    slope=[0,0,'inf','inf']
    # slope_1=0
    # slope_2='inf'
    #side截距
    wall_side=[x1,x1+height,y1,y1+width]
    # top_side=x1
    # buttom_side=x1+height
    # left_side=y1
    # right_side=y1+width
    cue_obj_diss=[]
    cue_obj_vxs=[]
    cue_obj_vys=[]
    reflection_pointx_group=[]
    reflection_pointy_group=[]
    for j in range(4):
        cue_obj_dis=[]
        cue_obj_vx=[]
        cue_obj_vy=[]
        reflection_pointx=[]
        reflection_pointy=[]
        for i in range(6):
            x_mirror,y_mirror=mirror_point(slope[j],wall_side[j],(objhitpointxs[i],objhitpointys[i]))
            x,y=segment_intersection(*boundaries[j],x_mirror,y_mirror)
            dis,vx,vy=distance_and_vector(cuex,cuey,x,y)
            cue_obj_dis.append(dis)
            cue_obj_vx.append(vx)
            cue_obj_vy.append(vy)
            reflection_pointx.append(x)
            reflection_pointy.append(y)
        cue_obj_diss.append(cue_obj_dis)
        cue_obj_vxs.append(cue_obj_vx)
        cue_obj_vys.append(cue_obj_vy)
        reflection_pointx_group.append(reflection_pointx)
        reflection_pointy_group.append(reflection_pointy)
    obj_hole_diss=[]
    obj_hole_dis=[]
    for i in range(4):
        for j in range(6):
            dis,vx,vy=distance_and_vector(reflection_pointx_group[i][j],reflection_pointy_group[i][j],objx,objy)
            obj_hole_dis.append(dis)
        obj_hole_diss.append(obj_hole_dis)
    main2obstacles1=[]
    for i in range(0,4):
        values2=[]
        for j in range(0,6):
            value2=0
            for k in range(1,ballcount):
                value2,z,z=point_to_line_distance(ballx_set[k],bally_set[k],cuex,cuey,reflection_pointx_group[i][j],reflection_pointy_group[i][j],2*radius+1,i+1,j,value2)
                value2,z,z=point_to_line_distance(ballx_set[k],bally_set[k],objhitpointxs[i],objhitpointys[i],reflection_pointx_group[i][j],reflection_pointy_group[i][j],2*radius+1,i+1,j,value2)
            # if objhitpointxs[i]==virholex[i] and objhitpointys[i]==virholey[i]:
            #     value2+1
            values2.append(value2)
        main2obstacles1.append(values2)
    all_angle2=[]
    for i in range(0,4):
        cue_obj_holeangle2=[]
        for j in range(0,6):
            cue_obj_hole1=vector_angle(reflection_pointx_group[i][j],reflection_pointy_group[i][j],objx,objy,virholex[j],virholey[j])
            if cue_obj_hole1<90:
                cue_obj_holeangle2.append(-cue_obj_hole1)
            else:
                cue_obj_holeangle2.append(cue_obj_hole1)
        all_angle2.append(cue_obj_holeangle2)
    main2obstacles2=[]
    main2obstacles2=target_hole(objhitpointxs,objhitpointys,ballcount,ballx_set,bally_set,6)
    for i in range(4):
        print("angle",all_angle2[i])
        print("values2",main2obstacles1[i])  
    print("main2obs",main2obstacles2)
    print("main2cue_target_obs",main2obstacles1)
    way2scores2=[]
    for i in range(0,4):
        way2scores1=[]
        for j in range(0,6):
            score=cal_score(cue_obj_diss[i][j]+obj_hole_diss[i][j],all_angle2[i][j],main2obstacles1[i][j],main2obstacles2[j])
            if score<0:
                print(score)
            way2scores1.append(score)
        way2scores2.append(way2scores1) 
        print("way2score",i+1,way2scores2[i])
    bestscore, best_index1, best_index2 = find_min_negative_integer_in_nested_list(way2scores2)
    vxs2 = []
    vys2 = []
    for i in range(4):
        vxs1 = []
        vys1 = []
        for j in range(6):
            cue_point_dis, vx, vy = distance_and_vector(cuex, cuey, reflection_pointx_group[i][j], reflection_pointy_group[i][j])
            vxs1.append(vx)
            vys1.append(vy)
        vxs2.append(vxs1)
        vys2.append(vys1)

    if bestscore:
        best_virholex = vir_hole_positions[best_index2][0]
        best_virholey = vir_hole_positions[best_index2][1]
        final_hitpointx = objhitpointxs[best_index2]
        final_hitpointy = objhitpointys[best_index2]
        bestvx = vxs2[best_index1][best_index2]
        bestvy = vys2[best_index1][best_index2]
        reflectionx=reflection_pointx_group[best_index1][best_index2]
        reflectiony=reflection_pointy_group[best_index1][best_index2]
        print("x",reflection_pointx_group)
        print("y",reflection_pointy_group)
        finalobsx = []
        finalobsy = []
        countobs = 0
        for i in range(ballcount):
            countobs, px, py = point_to_line_distance(ballx_set[i], bally_set[i], objx, objy, best_virholex, best_virholey, 2 * radius-1, i, best_index2 + 1, countobs)
            if px > 0:
                finalobsx.append(px)
                finalobsy.append(py)
        hitcuepointx,hitcuepointy=calculate_aim_point(cuex,cuey,reflectionx,reflectiony,radius)
        cue_obstacle=edge_detect(hitcuepointx,hitcuepointy)
        final(routenumber,bestscore,bestvx,bestvy,countobs,hitcuepointx,hitcuepointy,cue_obstacle)
        linexs=[cuex,reflectionx,final_hitpointx,best_virholex]
        lineys=[cuey,reflectiony,final_hitpointy,best_virholey]
        screen2(ballcount,routenumber,3,linexs,lineys,objhitpointxs,objhitpointys,ninehitpointxs,ninehitpointys,cuex,cuey,objx,objy,ninex,niney)
        return bestscore, bestvx, bestvy, countobs, hitcuepointx,hitcuepointy
    return main3(cuex, cuey, objx, objy,ninex,niney,objhitpointxs,objhitpointys,ninehitpointxs,ninehitpointys, ballx_set, bally_set, ballcount)
    
#僅需計路徑上的障礙物來進行路徑選擇
def main3(cuex, cuey, objx, objy,ninex,niney,objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys ,ballx_set, bally_set, ballcount):
    routenumber=3
    left_pointx,left_pointy,right_pointx,right_pointy=perpendicular_points(objx,objy,cuex,cuey,2*radius)
    second_cue_pointx=[]
    second_cue_pointy=[]
    second_cue_pointx.append(left_pointx)
    second_cue_pointy.append(left_pointy)
    second_cue_pointx.append(right_pointx)
    second_cue_pointy.append(right_pointy)
    objtoholes = []
    cue_obj_diss=[]
    cue_obj_vxs=[]
    cue_obj_vys=[]
    for i in range(2):
        cue_objdis,cue_vx,cue_vy=distance_and_vector(cuex,cuey,second_cue_pointx[i],second_cue_pointy[i])
        cue_obj_diss.append(cue_objdis)
        cue_obj_vxs.append(cue_vx)
        cue_obj_vys.append(cue_vy)
    values4=[]
    for j in range(2):
        value4=0
        for i in range(ballcount):
            value4,_,_=point_to_line_distance(ballx_set[i],bally_set[i],cuex,cuey,second_cue_pointx[j],second_cue_pointy[j],2*radius-1,i,j,value4)
        values4.append(value4)
    way3scores2=[]
    for i in range(2):
        way3scores = []
        for j in range(6):
            way3score = cal_score(cue_obj_diss[i], 1, values4[i],0)
            way3scores.append(way3score)
        way3scores2.append(way3scores)
    print(way3scores2)
    non_positive_scores = [score for score in way3scores if score <= 0]
    if non_positive_scores:
        max_non_positive_score = max(non_positive_scores)
        best_index = way3scores.index(max_non_positive_score)
        final_hitpointx = second_cue_pointx[best_index]
        final_hitpointy = second_cue_pointy[best_index]
        bestvx = cue_obj_vxs[best_index]
        bestvy = cue_obj_vys[best_index]
        routeobs=values4[best_index]
        hitcuepointx, hitcuepointy = calculate_aim_point(cuex, cuey, final_hitpointx, final_hitpointy, radius)
        cue_obstacle=edge_detect(hitcuepointx,hitcuepointy)
        final(routenumber,max_non_positive_score, bestvx, bestvy,routeobs, hitcuepointx, hitcuepointy,cue_obstacle)
        print(values4)
        linexs=[cuex,final_hitpointx]
        lineys=[cuey,final_hitpointy]
        #ballcount,routenumber,hitcuepointx,hitcuepointy,objx,objy,best_virholex,best_virholey,target_hitx,targethity,reflectionx,reflectiony
        screen2(ballcount,routenumber,1,linexs,lineys,objhitpointxs,objhitpointys,ninehitpointxs,ninehitpointys,cuex,cuey,objx,objy,ninex,niney)
        return max_non_positive_score, bestvx, bestvy, cue_obstacle, hitcuepointx, hitcuepointy
    else:
        routenumber=4
        routeobs=values4[1]
        final_hitpointx=objhitpointxs[1]
        final_hitpointy=objhitpointys[1]
        hitcuepointx, hitcuepointy = calculate_aim_point(cuex, cuey, final_hitpointx, final_hitpointy, radius)
        cue_obstacle=edge_detect(hitcuepointx,hitcuepointy)
        final(routenumber,way3scores[1],cue_obj_vxs[1],cue_obj_vys[1],"x", hitcuepointx, hitcuepointy,cue_obstacle)
        #ballcount,routenumber,hitcuepointx,hitcuepointy,objx,objy,best_virholex,best_virholey,target_hitx,targethity,reflectionx,reflectiony
        print(values4)
        linexs=[cuex,final_hitpointx]
        lineys=[cuey,final_hitpointy]
        screen2(ballcount,routenumber,1,linexs,lineys,objhitpointxs,objhitpointys,ninehitpointxs,ninehitpointys,cuex,cuey,objx,objy,ninex,niney)
        return way3scores[1],cue_obj_vxs[1],cue_obj_vys,values4[1],cue_obstacle,hitcuepointx,hitcuepointy

    
    
def vector_angle(n1x, n1y, n2x, n2y, n3x, n3y):
    vx1, vy1 = n2x - n1x, n2y - n1y
    vx2, vy2 = n3x - n2x, n3y - n2y
    dotproduct = vx1 * vx2 + vy1 * vy2
    magnitude1 = math.sqrt(vx1 ** 2 + vy1 ** 2)
    magnitude2 = math.sqrt(vx2 ** 2 + vy2 ** 2)
    cos = dotproduct / (magnitude1 * magnitude2)
    cos = max(-1, min(1, cos))
    rad = math.acos(cos)
    deg = math.degrees(rad)
    return deg

def cal_score(distance, angle, cue_objobs, obj_holeobs):
    score = ((angle * -22) + (distance * -1) + (obj_holeobs * -4000))
    if angle > 0:
        score = abs(score)
    if cue_objobs > 0:
        score = abs(score)
    return score

def edge_detect(hitcuepointx,hitcuepointy):
    cue_obstacle=0
    if hitcuepointx - radius < x1 or hitcuepointx + radius > x1 + width or hitcuepointy - radius < y1 or hitcuepointy + radius > y1 + height:
        return True
    for i in range(ballcount):
        cue_obstacle,_,_=point_to_line_distance(ballx_set[i],bally_set[i],hitcuepointx,hitcuepointy,cuex,cuey,2*radius-1,i,1,cue_obstacle)
        return True
    return False

def target_hole(objhitpointxs, objhitpointys, ballcount, ballx_set, bally_set,hitpoint_count):
    obstacles = []
    for i in range(hitpoint_count):
        count = 0
        for j in range(ballcount):
            count, _, _ = point_to_line_distance(ballx_set[j], bally_set[j], objhitpointxs[i], objhitpointys[i], vir_hole_positions[i][0], vir_hole_positions[i][1], 2 * radius, i + 1, j, count)
        obstacles.append(count)
    return obstacles

#the final data need to publish
def final(routenumber,bestscore,bestvx,bestvy,obstacle,bestx,besty,cue_obstacle):
    print("---------------------------------------------")
    print("routenumber",routenumber)
    print("Score:", bestscore)
    print("vx, vy:", bestvx, bestvy)
    print("Obstacles on the route:", obstacle)
    print("x, y:", bestx, besty)
    print("there have obstacle around cue",cue_obstacle)
    # return ballx_set,bally_set,ballcount,cu
    # ex,cuey,bestscore, bestvx, bestvy, countobs, final_hitpointx, final_hitpointy,x,y
def screen2(ballccout,routenumber,linecount,linexs,lineys,objhitpointxs,objhitpointys,ninehitpointxs,ninehitpointys,cuex,cuey,objx,objy,ninex,niney):
    plt.title('Basic Plot in Matplotlib')
    plt.xlabel('X Axis Label')
    plt.ylabel('Y Axis Label')
    plt.grid()
    plt.plot([holex[0],holex[2]],[holey[0],holey[2]],[holex[2],holex[5]],[holey[2],holey[5]],
             [holex[5],holex[3]],[holey[5],holey[3]],[holex[3],holex[0]],[holey[3],holey[0]],color='black')
    print(linexs)
    print(lineys)
    for i in range(linecount):
       plt.plot((linexs[i],linexs[i+1]),(lineys[i],lineys[i+1]), linestyle = '-') 
    plt.plot(objx,objy,marker='o',ms=radius,color='yellow')
    plt.plot(cuex,cuey,marker='o',ms=radius,color='red')
    plt.plot(ninex,niney,marker='o',ms=radius,color='pink')
    for i in range(1,ballcount-1):
        plt.plot(ballx_set[i],bally_set[i],marker='o',ms=radius,color='blue')
    for i in range(6):
        plt.plot(hole_positions[i][0],hole_positions[i][1],marker = 'o',ms=holeradius,color='black')
        plt.plot(vir_hole_positions[i][0],vir_hole_positions[i][1],marker = 'o',ms=holeradius,color='black')
        plt.plot(objhitpointxs[i],objhitpointys[i],marker = 'o',ms=3,color='green')
        plt.plot(ninehitpointxs[i],ninehitpointys[i],marker = 'o',ms=3,color='green')
    plt.show()
        
        
def main(ballx_set,bally_set,ballcount,cuex,cuey):
    route=[]
    objhitpointxs= []
    objhitpointys = []
    ninehitpointxs=[]
    ninehitpointys=[]
    for i in range(6):
        hitpointx, hitpointy = calculate_aim_point(ballx_set[0], bally_set[0], vir_hole_positions[i][0], vir_hole_positions[i][1], radius)
        ninehitpointx,ninehitpointy=calculate_aim_point(ballx_set[ballcount-1],bally_set[ballcount-1],vir_hole_positions[i][0], vir_hole_positions[i][1], radius)
        objhitpointxs.append(hitpointx)
        objhitpointys.append(hitpointy)
        ninehitpointxs.append(ninehitpointx)
        ninehitpointys.append(ninehitpointy)
    #cue_target ball obstacle count
    values1 = []
    first_route_judge=False
    for i in range(6):
        value1 = 0
        for j in range(1,ballcount):
            value1, _, _ = point_to_line_distance(ballx_set[j], bally_set[j], cuex, cuey, objhitpointxs[i], objhitpointys[i], 2 * radius, "cue", j, value1)
        if value1==0:
            first_route_judge=True
        values1.append(value1)
    print("first_route_choice",values1,first_route_judge)
    if first_route_judge==True:
        return method1(cuex, cuey, ballx_set[0], bally_set[0],ballx_set[ballcount-1],bally_set[ballcount-1], objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys, values1, ballcount, ballx_set, bally_set)
    else:
        return main2(cuex, cuey, ballx_set[0], bally_set[0], ballx_set[ballcount-1],bally_set[ballcount-1],objhitpointxs, objhitpointys,ninehitpointxs,ninehitpointys,ballx_set, bally_set, ballcount,)

if __name__ == '__main__':
    balls=[]
    ballcount=8
    #def generate the ball
    cuex, cuey, ballx_set, bally_set, ball_count=generate_balls(ballcount,radius)
    print(ballx_set)
    print(bally_set)
    print("ballcount",ballcount)
    main(ballx_set,bally_set,ballcount,cuex,cuey)