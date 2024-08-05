import random
import math
import sys
import time 
import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point, LineString
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
x1 = -311
y1 = 612
hole_positions = [(x1, y1), (x1 + width // 2, y1), (x1 + width, y1),
                  (x1, y1 + height), (x1 + width // 2, y1 + height), (x1 + width, y1 + height)]

vir_hole_positions=[(x1+radius,y1+height-radius),(x1+width/2,y1+height-radius),(x1+width-radius,y1+height-radius),(x1+radius,y1+radius),(x1+width/2,y1+radius),(x1-radius+width,y1+radius)]
actualwidth =62.7
actualheight=30.4
width=627
height=304
radius=int(1.6/actualheight*height)
holeradius=int(width/actualwidth*2)
holex=[x1,x1+width/2,x1+width,x1,x1+width/2,x1+width]
holey=[y1,y1,y1,y1+height,y1+height,y1+height]
# virholex=[x1+radius,x1+width/2,x1+width-radius,x1+radius,x1+width/2,x1+width-radius]
# virholey=[y1+radius,y1+radius,y1+radius,y1+height-radius,y1+height-radius,y1+height-radius]

def distance_and_vector(point1,point2):
    n1x,n1y=point1
    n2x,n2y=point2
    dx = n1x - n2x
    dy = n1y - n2y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return round(dist, 2), (dx, dy)

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
def is_overlapping(x, y,cuex,cuey,existing_balls, radius):
    for bx, by in existing_balls:
        if math.sqrt((x - bx) ** 2 + (y - by) ** 2) < 2 * radius and math.sqrt((x-cuex)**2+(y-cuey)**2)<2*radius:
            return True
    return False

def generate_balls(ballcount, radius):
    cuex = random.randint(x1 + radius, x1 + width - radius)
    cuey = random.randint(y1 + radius, y1 + height - radius)
    ball_positions = []

    while len(ball_positions) <= ballcount:
        x = random.randint(x1 + radius, x1 + width - radius)
        y = random.randint(y1 + radius, y1 + height - radius)
        if not is_overlapping(x, y,cuex,cuey, ball_positions, radius):
            ball_positions.append((x, y))

    ballx_set = [pos[0] for pos in ball_positions]
    bally_set = [pos[1] for pos in ball_positions]

    return cuex, cuey, ballx_set, bally_set, ballcount
def calculate_aim_point(obj_point,target_point, ball_diameter):
    # 计算从球到目标的向量
    ball_x,ball_y=obj_point
    target_x,target_y=target_point
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
    
    return (aim_point_x, aim_point_y)

def point_to_line_distance(obs_ball, obj_point, target_point, temp, obs_value):
    x1, y1 = obj_point
    x2, y2 = target_point
    px, py = obs_ball
    dx = x2 - x1
    dy = y2 - y1
    apx = px - x1
    apy = py - y1
    d_mag_squared = dx ** 2 + dy ** 2
    if d_mag_squared == 0:  # 线段退化为一个点
        dist = math.sqrt(apx ** 2 + apy ** 2)
    else:
        t = (apx * dx + apy * dy) / d_mag_squared
        
        if t < 0:
            closest_x, closest_y = x1, y1
        elif t > 1:
            closest_x, closest_y = x2, y2
        else:
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy
        
        dist = math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)
        # plt.plot([cuex,first_hitpoint[0]],[cuey,first_hitpoint[1]],linestyle='-')
    # if temp==1:
    #     plt.plot([px,closest_x],[py,closest_y],linestyle='-')
    if dist < 2.5* radius:
        obs_value += 1
        return obs_value, px, py
    return obs_value, 0, 0

def check_obstacle_ball(obs_ball,obj_point,target_point,obs_count):
    maskwidth = radius+8
    n1x,n1y=target_point
    n2x,n2y=obj_point
    vectorx = n1x - n2x
    vectory = n1y - n2y
    vectorlengh = math.sqrt(abs(vectorx)**2+abs(vectory)**2)
    unit_vector = np.array([vectorx/vectorlengh, vectory/vectorlengh])
    vector = np.array([vectorx+unit_vector[0]*radius, vectory+unit_vector[1]*radius])
    normal_unit_vector = np.array([unit_vector[1], -unit_vector[0]])
    # tengentdot = np.array([ballx-unit_vector[0]*r, bally-unit_vector[1]*r])
    ball = np.array([obj_point[0], obj_point[1]])
    first_poly = ball - normal_unit_vector*maskwidth
    second_poly = ball + normal_unit_vector*maskwidth
    third_poly = second_poly + vector
    fourth_poly = first_poly + vector
    ploy=(first_poly,second_poly,third_poly,fourth_poly)
    # plt.plot([first_poly[0],second_poly[0]],[first_poly[1],second_poly[1]],linestyle='-')
    # plt.plot([second_poly[0],third_poly[0]],[second_poly[1],third_poly[1]],linestyle='-')
    # plt.plot([third_poly[0],fourth_poly[0]],[third_poly[1],fourth_poly[1]],linestyle='-')
    # plt.plot([fourth_poly[0],first_poly[0]],[fourth_poly[1],first_poly[1]],linestyle='-')
    polygon = Polygon(ploy)
    shapely_objectballs = Point(obs_ball[0],obs_ball[1])
    if polygon.contains(shapely_objectballs):
        # points_in_poly_indices.append(i)
        obs_count += 1
    return obs_count
def vector_angle(point1,point2,point3):
    n1x, n1y = point1
    n2x, n2y = point2
    n3x, n3y = point3
    vx1, vy1 = n2x - n1x, n2y - n1y
    vx2, vy2 = n3x - n2x, n3y - n2y
    dotproduct = vx1 * vx2 + vy1 * vy2
    magnitude1 = math.sqrt(vx1 ** 2 + vy1 ** 2)
    magnitude2 = math.sqrt(vx2 ** 2 + vy2 ** 2)
    cos = dotproduct / (magnitude1 * magnitude2)
    cos = max(-1, min(1, cos))
    rad = math.acos(cos)
    deg = math.degrees(rad)
    if deg<=110:
        deg=-deg
    return deg

def cal_score(distance, angle, obj_holeobs):
    score = ((angle * 22) + (distance * -1) + (obj_holeobs * -4000))
    if angle > 0:
        score = abs(score)
    # if point_out_of_range==True:
    #     score = abs(score)
    return score


def mirror_point(line_m, line_b, point):
    x1,y1=(point)
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

    return (px,py)

# def kiss_nine_ball(cuex,cuey,objx,objy,ninex,niney,):
#the final data need to publish

    
def screen2(ballccout,routenumber):
    
    plt.title('Basic Plot in Matplotlib')
    plt.xlabel('X Axis Label')
    plt.ylabel('Y Axis Label')
    plt.grid()
    plt.plot([holex[0],holex[2]],[holey[0],holey[2]],[holex[2],holex[5]],[holey[2],holey[5]],
             [holex[5],holex[3]],[holey[5],holey[3]],[holex[3],holex[0]],[holey[3],holey[0]],color='black')
    # for i in range(linecount):
    #    plt.plot((lines[i],lines[i+2]),(lines[i+1],lines[i+3]), linestyle = '-') 
    plt.plot(cuex,cuey,marker='o',ms=2*radius,color='red')
    
    for i in range(ballccout):
        plt.plot(ballx_set[i],bally_set[i],marker='o',ms=2*radius,color='blue')
        plt.text(ballx_set[i], bally_set[i], ((ballx_set[i],bally_set[i]),i+1),color='black', fontweight='bold')
    for i in range(6):
        plt.plot(hole_positions[i][0],hole_positions[i][1],marker = 'o',ms=holeradius,color='black')
        plt.plot(vir_hole_positions[i][0],vir_hole_positions[i][1],marker = 'o',ms=holeradius,color='black')
    plt.show()
    
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
def main(cuex, cuey, ballx_set, bally_set, ballcount):
    main=method_chioce(ballx_set,bally_set,ballcount,cuex,cuey)
    main.main()
def final(self,routenumber,bestscore,bestvx,bestvy,obstacle,best_cue_hitpoint,cue_obstacle):
        print("---------------------------------------------")
        print("routenumber",routenumber)
        print("Score:", bestscore)
        print("vx, vy:", bestvx, bestvy)
        print("Obstacles on the route:", obstacle)
        print("x, y:", best_cue_hitpoint)
        print("there have obstacle around cue",cue_obstacle)
         
class method_chioce():
    def __init__(self,ballx_set,bally_set,ballcount,cuex,cuey):
        self.cue=(cuex,cuey)
        self.positions = [(ballx_set[i], bally_set[i]) for i in range(ballcount)]
        
        
        
    def main(self):
        self.all_ball_hitpoint=[]
        self.obj_hole_obs=[]
        for i in range(ballcount):
            temp2cal_hitpoint=[]
            temp2obj_hole_obs=[]
            for j in range(6):
                temp1cal_hitpoint=calculate_aim_point(self.positions[i],vir_hole_positions[j],radius/2)
                temp2cal_hitpoint.append(temp1cal_hitpoint)
                
                temp1obj_hole_obs=0
                for l in range(ballcount):
                    if i==l:
                        continue
                    temp1obj_hole_obs=check_obstacle_ball(self.positions[l],self.cue,temp1cal_hitpoint,temp1obj_hole_obs)
                    # temp1obj_hole_obs=check_obstacle_ball(self.positions[l],self.positions[i],vir_hole_positions[j],temp1obj_hole_obs)
                temp2obj_hole_obs.append(temp1obj_hole_obs)
            self.obj_hole_obs.append(temp2obj_hole_obs)
            self.all_ball_hitpoint.append(temp2cal_hitpoint)
        method1_scores=[]
        obj_hole_dis=[]
        obj_hole_angle=[]
        obj_hole_vector=[]
        for i in range(ballcount):
            temp3dis=[]
            temp2vector=[]
            temp2angle=[]
            for j in range(6):
                temp1dis,temp1vector=distance_and_vector(self.cue,self.all_ball_hitpoint[i][j])
                temp2dis,_=distance_and_vector(self.all_ball_hitpoint[i][j],vir_hole_positions[j])
                temp3dis.append(temp1dis+temp2dis)
                temp2vector.append(temp1vector)
                temp1angle=vector_angle(self.cue,self.all_ball_hitpoint[i][j],vir_hole_positions[j])
                temp2angle.append(temp1angle)
            obj_hole_angle.append(temp2angle)
            obj_hole_dis.append(temp3dis)
            obj_hole_vector.append(temp2vector)
        method1_judge=False
        for i in range(ballcount):
            temp2score=[]
            temp1score=0
            for j in range(6):
                temp1score=cal_score(obj_hole_dis[i][j],obj_hole_angle[i][j],self.obj_hole_obs[i][j])
                temp2score.append(temp1score)
                if temp1score < 0 :
                    method1_judge=True
            method1_scores.append(temp2score)
        print(self.obj_hole_obs)
        print(method1_scores)
        print(method1_judge)
        if method1_judge==True:
            max_non_positive_score,best_index1,best_index2=find_min_negative_integer_in_nested_list(method1_scores)
            best_virhole = vir_hole_positions[best_index2]
            first_hitpoint = self.all_ball_hitpoint[best_index1][best_index2]
            best_cue_hitpoint=calculate_aim_point(self.cue,first_hitpoint,radius/2)
            best_hit_vector = obj_hole_vector[best_index2]
            routeobs = self.obj_hole_obs[best_index1][best_index2]
            plt.plot(best_cue_hitpoint[0],best_cue_hitpoint[1],marker='o',ms=3,color='red')
            plt.plot([cuex,first_hitpoint[0]],[cuey,first_hitpoint[1]],linestyle='-',color='red')
            plt.plot([self.positions[best_index1][0],best_virhole[0]],[self.positions[best_index1][1],best_virhole[1]],linestyle='-',color='red')
            final(self,1,max_non_positive_score,best_hit_vector[0],best_hit_vector[1],routeobs,best_cue_hitpoint,0)
            screen2(ballcount,1)
            return max_non_positive_score,best_hit_vector[0], best_hit_vector[1], routeobs, best_cue_hitpoint[0], best_cue_hitpoint[1]
        else:
            print(method1_judge)
            return False
    
    
    
if __name__== '__main__':
    balls=[]
    ballcount=8
    #def generate the ball
    cuex, cuey, ballx_set, bally_set, ballcount=generate_balls(ballcount,radius)
    print(ballx_set)
    print(bally_set)
    ballcount+=1
    print("ballcount",ballcount)
    main(cuex, cuey, ballx_set, bally_set, ballcount)