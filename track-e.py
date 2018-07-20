import json
import math
import functools
import operator
import random
import datetime
from PIL import Image, ImageFilter,ImageDraw
from time import sleep


## Data Load
f=open("detected_data_set.json","r")

json_data=f.read()

data=json.loads(json_data)

def id_gen():
    dt=datetime.datetime.now()
    return dt.strftime('%d%H%M%S-%f')


hexa_gen=lambda:"#"+"%06x"%random.randint(0,0xFFFFFF)
#id 는 같은 세대의 이미지들끼리 합치지 않기를 위함
def data_parser(image_info,generation):
    image=Image.open(image_info['image'])
    #Current Image Log
    print(image_info['image'])
    
    temp_light_tower=[]
    #한 사진에 여려명의 얼굴이 들어갈 수 있음
    #faces가 없는 경우
    if not 'faces' in image_info['result']:
        return []
    for face in image_info['result']['faces']:
        # x = int(face['x']*image.width)
        # w = int(face['w']*image.width)
        # y = int(face['y']*image.height)
        # h = int(face['h']*image.height)
        face['x'] = int(face['x']*image.width)
        face['w'] = int(face['w']*image.width)
        face['y'] = int(face['y']*image.height)
        face['h'] = int(face['h']*image.height)
        temp_light_tower.append(DetectedObject(face,generation,True,image_info['image'],hexa_gen()))
        sleep(0.05)
    return temp_light_tower
        

class DetectedObject:
    def __init__(self,face_info,generation,is_new,source,color):
        self.face_info=face_info
        self.generation=generation
        self.is_new=is_new
        self.previous_detected_object=None
        self.source=source
        self.color=color
        self.id=id_gen()

        self.center_x=int((face_info['x']+face_info['x']*2)/2)
        self.center_y=int((face_info['y']+face_info['y']*2)/2)
    
class LightTower:
    # d == pixel distance
    # p == similarity constant
    def __init__(self,d=200,p=10):
        self.set_d(d)
        self.set_p(p)
        self.fishing_ground=[]
        self.r=lambda:"%06x"%random.randint(0,0xFFFFFF)
        self.cur_r="#e9e9e9"
        self.workdir=""
        self.debug_mode=False

    def set_d(self,d):
        self.d=d
    def set_p(self,p):
        self.p=p
    def commit(self):
        print("##########COMMIT##########")
        for idx,face in enumerate(self.fishing_ground):
            print(idx,face.id," Face] X=>",face.center_x,"Y=>",face.center_y)
            # 자신의 중심점과 타겟의 중심점간의 유클리드 거리를 구하여
            # d의 조건과 만족하는지 계산하고 계산된 타겟을 선정하여
            # 유사도 연산을 진행함
            candidate_list=[]
            for target_face in self.fishing_ground:
                # 자기 자신인가?
                if( target_face.id == face.id):
                    continue

                print("\t",target_face.id," Target Face] X=>",target_face.center_x,"Y=>",target_face.center_y)
                dist=self.euclidean_distance(face.center_x,face.center_y,target_face.center_x,target_face.center_y)
                
                # 타켓이 범위내 있는지?
                if(dist>self.d):
                    print("\tFAIL ] d>",dist,self.d)
                    continue
                # 타켓이 새로운 인식체인지? 
                if(target_face.is_new==False):
                    print("\tFAIL ] not new")
                    continue
                # 같은 시점에 생성된 객체인지?
                if(face.generation == target_face.generation):
                    print("\tFAIL ] same timeline")
                    continue
                print("\t**PASS ] Tareget DIST[",dist,self.d,"] NEW[",target_face.is_new,"] TIMELINE[",face.generation,target_face.generation,"]")
                
                if(self.debug_mode==True):   
                    input()
                candidate_list.append(target_face)
            
            # 후보자를 못찾았을 경우
            if len(candidate_list) <= 0:
                print("[Fail there's no candidate] too nerf")
                continue

            # 가장 유사도가 높은 이미지를 선택 0 이 같은 이미지
            min_idx=0
            min_result=0x7fffff
            for idx,candidate in enumerate(candidate_list):
                result=self.measure_similiaration(face,candidate)
                print(candidate.id ,"][RMS]",result)
                if(result<min_result):
                    min_result=result
                    min_idx=idx
            
            if(min_result>self.p):
                print("[Fail similiarity pass fail] too nerf")
                continue
            print("[Merge process start MIN ",face.id,"id =>" ,candidate_list[min_idx].id,"]")
            for ind,bug_fix_please in enumerate(self.fishing_ground):
                if self.fishing_ground[ind].id==candidate_list[min_idx].id:
                    self.fishing_ground[ind].color=face.color
                    self.fishing_ground[ind].is_new=False
                    self.fishing_ground[ind].previous_detected_object=face
            # # for color;
            # self.fishing_ground[candidate_list[min_idx] in self.fishing_ground].color=face.color
            # # 

            # self.fishing_ground[candidate_list[min_idx] in self.fishing_ground].is_new=False

            # self.fishing_ground[candidate_list[min_idx] in self.fishing_ground].previous_detected_object=face
            
            # # print(self.fishing_ground[candidate_list[min_idx] in self.fishing_ground].previous_detected_object.source)

            self.fishing_ground.remove(face)
            self.show_fishing_ground()
        
        # 이번에 새로 들어온 객체들이 이미 다 포함 됬다면 픽스
        for idx,face in enumerate(self.fishing_ground):
            if face.is_new==True:
                print("[FIXED fish]",face.id,"TRUE=>FALSE")
                face.is_new=False
            else:
                pass
        
        self.show_fishing_ground()
            
    def show_fishing_ground(self):
        print("\n########FISHING POOL##########")
        for idx,val in enumerate(self.fishing_ground):
            print(val.id,"]",val.generation,val.is_new,val.source,val.previous_detected_object)
        print("########FISHING POOL##########\n")        


    def measure_similiaration(self,face,candidate):
        h1_crop=Image.open(face.source).crop((face.face_info['x'],face.face_info['y'],face.face_info['x']+face.face_info['w'],face.face_info['y']+face.face_info['h']))
        h2_crop=Image.open(candidate.source).crop((candidate.face_info['x'],candidate.face_info['y'],candidate.face_info['x']+candidate.face_info['w'],candidate.face_info['y']+candidate.face_info['h']))

        h1=h1_crop.histogram()
        h2=h2_crop.histogram()

        rms=math.sqrt(functools.reduce(operator.add,map(lambda a,b:(a-b)**2,h1,h2))/len(h1))
        
        return rms
    def push(self,obj):
        self.fishing_ground=self.fishing_ground+obj

    def euclidean_distance(self,x1,y1,x2,y2):
        return int(((x2-x1)**2+(y2-y1)**2)**0.5)

    def draw_pool_to_image(self,image):
        image=Image.open(image)
        rectangle=ImageDraw.Draw(image)

        for idx,val in enumerate(self.fishing_ground):
            self.travling_draw(val,image,rectangle)
        dt=datetime.datetime.now()
        image.save(self.workdir+dt.strftime('%Y%m%d%H%M%S%f')+".jpg","JPEG")
    


    def travling_draw(self,fish,image,rectangle):
        
        if(fish.previous_detected_object==None):
            return
        else:
            self.travling_draw(fish.previous_detected_object,image,rectangle)

        x=fish.face_info['x']
        w=fish.face_info['w']
        y=fish.face_info['y']
        h=fish.face_info['h']

        rectangle.rectangle(((x,y),(x+w,y+h)),outline=fish.color)
        

if __name__ == "__main__":
    # into data pipe line
    d=200
    p=10

    lt=LightTower(d=d,p=p)
    lt.workdir="result/d"+str(d)+"p"+str(p)+"/"
    for idx,dt in enumerate(data):
        lt.push(data_parser(dt,idx))
        lt.commit()
        lt.draw_pool_to_image(dt['image'])

    
    # Simple Test Code
    # lt=LightTower()
    # lt.push(data_parser(data[0],0))
    # lt.commit()
    # lt.push(data_parser(data[1],1))
    # lt.commit()

    # Measure Function Test Code
    # lt=LightTower()
    # lt.push(data_parser(data[0],0))
    # lt.measure_similiaration(lt.fishing_ground[0],lt.fishing_ground[1])


    