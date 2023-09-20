import openai
import time
import json
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured


# Load your API key from an environment variable or secret management service
BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = BASE_DIR / 'secrets.json'
with open(secret_file) as file:
    secrets = json.loads(file.read())

def get_secret(setting, secrets_dict=secrets):
    try:
        return secrets_dict[setting]
    except KeyError:
        error_msg = f'Set the {setting} environment variable'
        raise ImproperlyConfigured(error_msg)
    
openai.api_key = get_secret('GPT_SECRET_KEY')


# $데이터 베이스$, 줄여서 DB 특정 다수의 이용자들에게 필요한 정보를 제공한다든지 조직 내에서 필요로 하는 정보를 체계적으로 축적하여 그 조직 내의 이용자에게 필요한 정보를 제공하는 정보 서비스 기관의 심장부에 해당된다.
#    일반적으로 응용 프로그램과는 별개의 미들웨어[1]를 통해서 관리된다. 데이터베이스 자체만으로는 거의 아무 것도 못하기 때문에 그걸 관리하는 시스템과 통합돼 제공되며 따라서 정확한 명칭은 $데이터베이스 관리 시스템$(DBMS)[2]이 된다. 데이터베이스만 제공되는 건 CSV같이 아주 단순한 데이터에 국한되는데 이걸 직접 사용하는 경우는 많지 않고 이런 데이터를 RAW데이터로 간주해 다른 DBMS시스템에 적재하고 사용하는 게 일반적이다.
def gpt_sum(data):

    # 역할 부여
    messages = [
        {"role": "system", 
        "content" : """"
        당신은 노트를 필기하는 학생입니다. 
        제공하는 글을 대상으로 제목을 포함하여 노트를 필기하세요. 
        요구사항은 아래와 같습니다. 
        1. 7줄 필기노트를 작성하세요. 
        2. 핵심 키워드 혹은 핵심 문장은 $사과$와 같이 $로 처음과 끝을 감싸서 제공됩니다. 핵심 문장을 바탕으로 노트를 작성하세요.
        3. 노트의 제목은 []로 표현해야 하고, 마지막 문장을 제외한 각 문장의 끝은 \n\n으로 표기합니다.
        4. 각 문장은 키워드 : 설명 과 같은 형식으로 작성하도록 합니다. 각 문장은 가능한한 짧게 작성합니다.
        """
        },
        {"role": "user", 
        "content": """
        $사과$는 맛있는 과일입니다. 사과는 여러 종류가 있으며, 대표적으로 $홍옥$과 $아카네$가 있습니다. 
        홍옥은 빨간색을 띠는 특징을 가지며, 아카네는 그보다 연한 색깔과 부드러운 맛을 가집니다. 
        사과는 비타민 C가 풍부하므로 건강에 좋습니다. 
        또한, 사과에는 다양한 미네랄과 식이섬유가 함유되어 있어 소화를 돕습니다. 
        $아이들$은 사과의 달콤한 맛을 좋아하며, 간식으로 섭취하기에 좋습니다. 
        사과는 주스, 파이, 잼 등 다양한 요리에 사용될 수 있습니다. 
        유기농 사과는 화학물질이 사용되지 않아 $건강$에 더욱 좋다고 알려져 있습니다.
        """},
        {"role": "assistant", 
        "content": """
        [사과의 특징 및 이점]# 사과 : 맛있는 과일\n\n# 홍옥 : 빨간색을 띠는 사과의 종류\n\n# 아카네 : 연한 색과 부드러운 맛의 사과\n\n# 비타민 C, 미네랄, 식이섬유 : 사과의 영양소, 건강에 좋음\n\n# 아이들 : 사과의 달콤한 맛을 좋아함\n\n# 요리 활용 : 주스, 파이, 잼 등으로 활용 가능\n\n# 유기농 사과 : 화학물질 미사용, 건강에 더 좋음
        """},
        {"role": "user", 
        "content" : """
        데이터베이스는 다양한 정보를 저장, 관리하고, 검색하는데 사용되는 중요한 시스템입니다. 이러한 데이터베이스를 효율적으로 설계하고 운영하기 위한 몇 가지 주요 개념들을 살펴보겠습니다.
        $정규화$는 데이터베이스 설계의 핵심 원칙 중 하나입니다. 이것은 데이터 중복을 최소화하고, 데이터의 무결성을 유지하는 설계 방법입니다. 정규화를 통해 여러 테이블에 중복으로 저장되는 정보를 줄이고, 데이터의 일관성을 확보할 수 있습니다.
        데이터베이스 내에서, $엔터티$는 정보의 기본 단위로서 흔히 테이블로 표현됩니다. 각 테이블은 그 자체로 하나의 엔터티를 나타냅니다. 테이블 간의 $관계$는 엔터티 간의 연결을 나타내며, $일대일, 일대다, 다대다$ 등의 관계 유형으로 표현됩니다.
        데이터를 빠르게 검색하기 위해 $인덱스$라는 구조를 사용합니다. 인덱스는 특정 테이블의 한 또는 여러 필드에 대해 생성될 수 있으며, 데이터의 검색 속도를 크게 향상시킬 수 있습니다.
        데이터베이스에서 $뷰$는 특정 목적을 위해 여러 테이블의 정보를 조합한 가상의 테이블을 의미합니다. 뷰는 실제 데이터를 저장하지 않지만, 사용자에게 필요한 정보를 제공하는데 유용하게 사용됩니다.
        마지막으로, $무결성$은 데이터베이스의 데이터가 정확하고 일관되게 유지되도록 하는 규칙입니다. 무결성은 주로 제약 조건을 통해 데이터베이스에 적용되며, 데이터의 품질과 신뢰도를 보장하는데 중요한 역할을 합니다.
        이렇게 데이터베이스 설계는 다양한 원칙과 규칙을 통해 정보를 체계적이고 효율적으로 관리할 수 있게 돕습니다.
        """},
        {"role": "assistant", 
        "content" : """
        [데이터베이스 설계]# 정규화 : 데이터 중복을 최소화하는 설계 방법\n\n# 엔터티 : 정보의 기본 단위, 테이블로 표현\n\n# 관계 : 테이블 간의 연결\n\n# 인덱스 : 데이터 검색 속도 향상을 위한 구조\n\n# 일대일, 일대다, 다대다 : 엔터티 간 관계 유형\n\n# 뷰 : 하나 이상의 테이블로부터 파생된 가상 테이블\n\n# 무결성 : 데이터의 정확성과 일관성을 유지하는 규칙
        """},
    ]

    # # user_content = input("user : ")
    messages.append({"role": "user", "content": f"{data}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    result = completion.choices[0].message["content"].lstrip()

    print(f"GPT : {result}")
    return result


# 퀴즈 생성
def gpt_pro(data):
    # 역할 부여
    messages = [
        {"role" : "system",
        "content" : """
        당신의 역할은 4지선다 객관식 문제를 4개 만드는 것입니다.
        아래 규칙을 따라 문제를 만들어주세요.
        1. 입력으로 문자열이 주어집니다. 이 문자열을 대상으로 문제를 만들면 됩니다.
        2. 문제의 시작과 끝은 &로 감쌉니다. 예를 들어 &다음중 사과의 색이 아닌것을 고르시오& 와 같습니다.
        3. 객관식은 #으로 시작하여 #으로 끝납니다. 예를 들어 
        #빨간색# 
        #노란색# 
        #초록색# 
        #보라색#
        와 같습니다.
        4. 문제에 대한 정답을 제공해야합니다. 예를들어 위 문제의 경우 정답은 보라색이므로 정답번호인 4를 리턴합니다.
        정답은 %로 감싸서 제공합니다. %4%
        5. 문제에 대한 해설을 제공해야합니다. 해설은 1줄에서 2줄 사이로 제공합니다. 해설은 @로 감싸서 제공합니다.
        @사과는 빨간색,노란색,초록색 등의 색상을 갖는데 보락색은 존재하지 않으므로 정답은 4번입니다.@
        """},
        {"role":"user",
        "content":"""
        [술의 어원]
        #1 어원 : 삼국시대에서 출발한 낱말
        #2 압록강의 풍부성(豐夫城) : 고구려의 술잔 받침인 소파홀(肖巴忽)에 대한 기록
        #3 소파(肖巴) : 고구려의 '술' 어형으로 추정
        #4 신라의 이벌찬 : 서발한(舒發翰) 또는 서불한(舒弗邯)이라고 불렸으며, 주다(酒多)로 훈차되기도 함
        #5 주다(酒多) : 사람들이 '많다'의 옛말 '하다'의 어간을 표현하여 술을 의미
        #6 酒 : 신라어 '서발' 또는 '서불'에 대응되는 술을 의미
        """},
        {"role": "assistant",
        "content" : """
        &고구려에서 '술'을 의미하는 어형은 무엇인가요?&
        #압록강의 풍부성#
        #신라의 이벌찬#
        #소파(肖巴)#
        #서발 또는 서불#
        %3%

        @고구려에서 '술'을 의미하는 어형은 '소파(肖巴)'입니다. 따라서 정답은 3번입니다.@
        &삼국시대에서 출발한 '술'에 관한 낱말은 무엇인가요?&
        #어원#
        #압록강의 풍부성#
        #주다(酒多)#
        #酒#
        %1%

        @삼국시대에서 출발한 '술'에 관한 낱말은 '어원'입니다. 따라서 정답은 1번입니다.@
        &'서발' 또는 '서불'이 대응되는 글자는 무엇인가요?&
        #소파(肖巴)#
        #신라의 이벌찬#
        #서발한(舒發翰)#
        #酒#
        %4%

        @'서발' 또는 '서불'이 대응되는 글자는 '酒'입니다. 따라서 정답은 4번입니다.@
        &사람들이 '많다'의 옛말 '하다'의 어간을 표현하여 술을 의미하는 말은 무엇인가요?&
        #서발 또는 서불#
        #압록강의 풍부성#
        #소파(肖巴)#
        #주다(酒多)#
        %4%
        @사람들이 '많다'의 옛말 '하다'의 어간을 표현하여 술을 의미하는 말은 '주다(酒多)'입니다. 따라서 정답은 4번입니다.@
        """},
        {"role":"user",
        "content":"""
        [데이터베이스의 신뢰성과 안정성]
        #1 SQL : 데이터베이스 질의 언어로, 데이터를 관리하고 검색하는 데 사용된다.
        #2 인덱스 : 데이터베이스에서 데이터 검색 속도를 향상시키기 위한 자료 구조.
        #3 DBMS : 데이터베이스 관리 시스템으로, 데이터를 안전하게 저장, 관리하며 다양한 기능을 제공한다.
        #4 ACID : 데이터베이스의 트랜잭션 처리에서의 신뢰성과 안정성을 보장하는 네 가지 속성. 원자성(Atomicity), 일관성(Consistency), 고립성(Isolation), 지속성(Durability)을 의미한다.
        """},
        {
        "role": "assistant",
        "content": """
        &데이터베이스 질의 언어로, 데이터를 관리하고 검색하는 데 사용되는 것은 무엇인가?&
        #SQL#
        #인덱스#
        #DBMS#
        #ACID#
        %1%
        @데이터베이스 질의 언어로, 데이터를 관리하고 검색하는 데 사용되는 것은 'SQL'입니다. 따라서 정답은 1번입니다.@
        
        &데이터베이스에서 데이터 검색 속도를 향상시키기 위한 자료 구조는 무엇인가?&
        #SQL#
        #인덱스#
        #DBMS#
        #ACID#
        %2%
        @데이터베이스에서 데이터 검색 속도를 향상시키기 위한 자료 구조는 '인덱스'입니다. 따라서 정답은 2번입니다.@

        &데이터를 안전하게 저장하고, 관리하며 다양한 기능을 제공하는 시스템은 무엇인가?&
        #SQL#
        #인덱스#
        #DBMS#
        #ACID#
        %3%
        @데이터를 안전하게 저장하고, 관리하며 다양한 기능을 제공하는 시스템은 'DBMS'입니다. 따라서 정답은 3번입니다.@

        &데이터베이스의 구조와 제약 조건에 관한 전반적인 명세를 나타내는 것은 무엇인가?&
        #스키마(Schema)#
        #ER 모델(Entity-Relationship Model)#
        #뷰(View)#
        #데이터 독립성(Data Independence)#
        %1%
        @데이터베이스의 구조와 제약 조건에 관한 전반적인 명세를 나타내는 것은 '스키마(Schema)'입니다. 따라서 정답은 1번입니다.@
        """},
        {"role": "user",
        "content": """
        [우주의 기본 개념]
        #1 목성(Jupiter) : 태양계에서 가장 큰 행성으로, 굵은 줄무늬와 대적점으로 유명하다.
        #2 토성(Saturn) : 반지가 있는 행성으로 알려져 있으며, 여러 개의 위성을 가지고 있다.
        #3 G형 주계열성(G-type Main-sequence star) : 태양과 같은 타입의 별로, 중간 크기의 별들 중 하나다.
        #4 은하(Galaxy) : 별, 별 사이의 가스, 먼지, 그리고 어두운 물질로 구성된 대규모의 중력적으로 연결된 천체 집합.
        """},
        {
        "role": "assistant",
        "content": """
        &태양계에서 가장 큰 행성은 무엇인가?&
        #목성(Jupiter)#
        #토성(Saturn)#
        #지구(Earth)#
        #금성(Venus)#
        %1%
        @태양계에서 가장 큰 행성은 '목성(Jupiter)'입니다. 따라서 정답은 1번입니다.@

        &어느 행성이 반지로 유명한가?&
        #목성(Jupiter)#
        #토성(Saturn)#
        #지구(Earth)#
        #금성(Venus)#
        %2%
        @반지로 유명한 행성은 '토성(Saturn)'입니다. 따라서 정답은 2번입니다.@

        &태양과 같은 타입의 별은 어떤 형태의 별인가?&
        #B형 주계열성#
        #G형 주계열성(G-type Main-sequence star)#
        #M형 레드 드워프#
        #O형 별#
        %2%
        @태양과 같은 타입의 별은 'G형 주계열성(G-type Main-sequence star)'입니다. 따라서 정답은 2번입니다.@

        &별, 별 사이의 가스, 먼지 등으로 구성된 대규모의 천체 집합은 무엇인가?&
        #행성#
        #은하(Galaxy)#
        #성운(Nebula)#
        #블랙홀(Black Hole)#
        %2%
        @별, 별 사이의 가스, 먼지 등으로 구성된 대규모의 천체 집합은 '은하(Galaxy)'입니다. 따라서 정답은 2번입니다.@
        """}
    ]

    # user_content = input("user : ")
    messages.append({"role": "user", "content": f"{data}"})

    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    result = completion.choices[0].message["content"].strip()

    print(f"GPT Quiz: {result}")
    return result