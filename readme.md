# Simple object tracker on images

## kakao_vision_create_dataset.py 을 이용하여 데이터 셋을 생성
-  kakao_vision_create_dataset.py line 42
```python
if __name__ == "__main__":
    # 디렉토리 지정
    base_dir="samples/"
    
    # Kakao API key 지정
    API_URL=''
    MYAPP_KEY=''
``` 
- base_dir에 자신이 사용할 디렉토리를 **생성** 하고 입력
    - **base_dir에는 샘플 이미지들이 있어야 합니다.**
- API_URL과 MYAPP_KEY에 자신의 앱 키를 입력
### 결과 데이터 => detected_data_set.json

## track-e.py 를 통해 객체인식된 데이터 셋으로 부터 객체 트래킹
- track-e.py line 231
```python
if __name__ == "__main__":

    ## Data Load
    f=open("detected_data_set.json","r")
    json_data=f.read()
    data=json.loads(json_data)

    # into data pipe line
    d=200
    p=10
```
- 테스트 데이터셋 생성으로 얻어진 데이터를 로드 detected_data_set.json
- d는 거리 변수로 객체간의 거리가 낮을 수록 같은 객체일 확률이 높다는 가설을 위한 변수 입니다 d의 수치에 따라 허용 범위가 달라집니다. 높으면 높을수록 넓은 범위에서 인식이 가능하며 때에따라 전혀 다른 객체가 인식될 수 있습니다.

- p는 이미지 유사도 변수로 이미지 신뢰도 ( 0 일치 0 > 불일치도 계수 ) 에 따라서 인식하며 현재는 히스토그램으로 이미지 신뢰도를 추정하고 있습니다

가장 성공적인 변수 셋팅

d = 200
p = 11