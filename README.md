# OrganizeAddonPackages
for VAM

사용법
AddonPackages에 넣고 python OrganizeAddonPackages.py 로 실행 하면 됩니다

파이썬이 설치되어 있는지 확인
cmd상태에서 python -V를 입력하면 설치된 파이썬 버전이 나옵니다
3.6 이상이면 될꺼에요

제작자.패키지.버전.var 이 구조의 파일들만 처리합니다  
하위 폴더도 스캔한 뒤 제일 깊은 곳에 있던 같은 패키지 위치로 최신 패키지를 이동시킵니다

예를 들어  
AddonPackages\creator.package1.5.var  
AddonPackages\creator\creator.package1.3.var  
AddonPackages\creator\hair\creator.package1.1.var  
이렇게 있으면 creator.packages1.1.var, creator.packages1.3.var는 old로 이동하고  
creator.package1.3.var는 creator\hair폴더로 이동합니다

저는  
AddonPackages\plugins  
AddonPackages\clothing\shoes  
이런식으로 분류 해놓는데  
한번만 분류해서 넣어놓으면 버전업할때 AddonPackages에 받아놓은 패키지들을 스크립트 돌려서 이동시킵니다

제작자 별로 분류 해놓는분들도 되긴하는데 기존에 없던 새로운 패키지들은 알아서 이동해주진 않습니다  
버전이 여러개라면 구버전들은 old로 이동되고 AddonPackags에 최신버전만 남습니다  
AddonPackages\creator 폴더가 있는데 그 폴더안에 구버전 패키지가 없다면  
AddonPackages\creator.new_package.1.var가 있어도 creator폴더로 옮겨주진 않는다는거죠  
구버전이 있던 폴더로 최신버전이 이동합니다

정리가 끝나면 AddonPackages\old 폴더에 구버전 패키지들이 제작자 명으로 폴더가 생성되서 분류가 됩니다  
AddonPackages\old\creator\creator.package1.1.var  
old에 들어있는 폴더를 AddonPackages에서 다른곳으로 빼놓으시면 초기 로딩 속도 개선에 도움이 됩니다  
하위버전 기능을 모두 포함한 상위 버전이라고 생각하면 지워도 되구요  
vamhub에서 쉽게 받을 수 있는 구버전이면 용량 차지하는거 생각해서 지우는게 좋습니다  
지워도 종속성에서 다운로드 가능이라고 뜨면 받지말고 그 패키지를 눌러서 최신버전이 받아져 있다면 대부분 상위버전만으로 가능합니다  
특정 하위버전이 없다고 문제생긴다면 그렇게 만든 패키지 제작자를 탓하세요  

파일을 지우는 조건은 파일명이 같고 크기가 같고 해시가 같을때 지웁니다  
크기가 같고 해시가 같지만 파일명(버전부분)이 다르다면 실제 파일명을 모르기 때문에 지우지 않습니다  

파일명이 같고 크기는 같은데 해시가 다를 경우는 풀었다가 같은 알고리즘으로 재압축 할 때 종종 일어납니다  
패키지 내부 파일들을 해시해야 같은지 비교 가능합니다  
7-Zip으로 내부 해시는 쉽게 확인 가능합니다  

creator.beautiful_hair.1.var  
creator.beautiful_hair2.1.var  
creator.beautiful_hair_v2.1.var  
이런식은 같은 패키지로 인식하지 않습니다  
제작자명과 패키지명이 일치해야 비교합니다  

AddonPackages에 몽땅 넣고 쓰시는분이나  
AddonPackages\제작자로 폴더 구분해서 쓰시거나  
AddonPackages\카테고리로 구분해서 쓰시거나 할때 분류를 도와주는 정도 입니다

AddonPackages\old 폴더와 AddonPackages\default 폴더는 검색하지 않습니다  

심볼릭 링크나 정션 같은 순환링크를 만들어 놓은 곳에서는 사용하지 마세요  
