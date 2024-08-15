import json
from card_replacer import CardReplacer
from card_problem_title import ProblemTitle
from card_abstract import CardAbstract  
from openai import OpenAI  
from config import my_api_key
import datetime  
import random
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,BigInteger, SmallInteger,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base 
from sqlalchemy.exc import IntegrityError
from database import PortalPost, Session, add_post    

exampleCardPage = [
    '''
电信浙江星卡是一款备受用户青睐的大流量、高性价比的电话卡产品，特别是其29元135G+100分钟通话的长期套餐，更是吸引了众多用户的关注。以下是对浙江星卡及其29元套餐的详细介绍：

——————————————————————————————————————————————————————

一、浙江星卡概述

    浙江星卡是由中国电信浙江分公司推出的星卡大流量定制版，面向全国线上发售。该卡具有流量大、月租便宜、有效期长、无合约、可自选号等特点，被广大用户称为电信神卡。浙江星卡提供多种套餐选择，以满足不同用户的需求，其中29元135G+100分钟通话的套餐尤为受欢迎。

二、29元套餐详情

月租费用：29元/月

流量：包含105G国内通用流量+30G国内定向流量，总计135G。定向流量适用于特定APP，如头条系、腾讯系、百度系、阿里系、抖音、优酷等上百款常用应用，具体以运营商官方为准。

通话时长：100分钟国内通话时长

套餐外费用：超出套餐的流量按5元/GB计费，超出套餐的通话按0.1元/分钟计费，短信费用为0.1元/条。

三、优惠活动

首月免费：激活后首月赠送体验金或减免月租，用户可享受首月免费使用的优惠。

首充送话费：激活时首充50元，可额外获得一定的话费赠送，并享受套餐内的优惠内容。具体赠送金额和返还方式可能因活动而异，请以官方渠道信息为准。

长期可续约：该套餐为长期套餐，用户可根据自身需求选择是否续约。续约时，用户可根据运营商政策享受相应的优惠和服务。

四、办理及激活流程

用户可通过电信网上营业厅APP、线下营业厅、微信、支付宝等全渠道办理浙江星卡。

办理时需填写个人信息和在线选号（部分套餐可能不支持选号），提交成功后等待快递配送。

收到号卡后，用户需配合快递员或自行完成实名制激活操作，并按要求完成话费首充。激活过程中需准备好身份证原件，并确保信息的真实性和准确性。

五、注意事项

用户在办理和激活过程中需仔细阅读套餐详情和注意事项，避免产生不必要的误解和费用。

激活后需按照套餐规定使用，避免超出套餐范围产生额外费用。如有需要，可通过电信客服热线或前往营业厅进行咨询和办理相关业务。

---------------------------------------------------------------------------------------------------------------------------------

''',                ###关于浙江星卡
]

cardName = "浙江星卡"
newCardInfo = '''这是流量卡产品的内容：
中国电信电信浙江星
月租
29元月
(原月租39元)
全国流量
135G
105G通用+30G定向
通话
100 分钟
国内接听免费
优惠
首充50元赠送120元
资费介绍
原资费39元含5G通用+30G定向。
套餐外流量5元/G，语音0.1元/分钟，短信0.1元/条。
首月赠送40元体验金，相当于首月免月租(体验金当月有效)
专属渠道首充50元享受优惠活动不充值无法享受
①激活赠送40元话费体验金:激活当月有效，不退现金，不抵扣国漫及SP相
关费用可抵扣月租，即首月免月租。
②用户可参与充50送120元话费(本金50元一次性到账，赠金120元次月起分12个月，每月返10元)到期后根据运营商政策续约。
③充值激活后72小时之内店铺赠送105G通用流量/月(赠送24个月，到期后根据运营商政策续约)100分钟语音包(有效期1年，到期后可续约1年)
优惠后首月免费 月租29元归属地随机含105G通用流量+30G定向流量+100分钟 到期根据电信政策续签/注销
温馨提示
①首月套餐，按照当月剩余天数折算，下月初恢复完整套餐内容，办理号码与归属地随机不可指定，全国通用，办卡年龄限18-60周岁。
②国内流量、国内通话和接听免费范围不包括港澳台地区③不发货地区:贵州、广西、海南(海口、三亚除外)、云南、新疆、西藏具体以运营商审核为准。
定向流量
定向流量包含(百度系、网易系、头条系)快手、腾讯视频、优酷视频等上百款APP;具体定向流量APP可能有变动，以下仅供参考，具体定向流量请以运营商官方为准。
来 
5
'''
session = Session()
#标题
card_handler = ProblemTitle()
cardtitles = card_handler.generate_titles(cardName)  
#关键词
problem_replacer = CardReplacer()
cardreplacers = problem_replacer.generate_titles(cardName)  
#摘要
card_abstract = CardAbstract()
cardabstracts = card_abstract.generate_titles(cardName)
for i in range(10):  
    # print(cardtitles[i])        #标题
    # print(cardreplacers[i])     #关键词        
    # print(cardabstracts[i])     #摘要
     
    post_title_value = cardtitles[i]  
    # 检查 post_title 是否已经存在  
    existing_record = session.query(PortalPost).filter_by(post_title=post_title_value).first()  
    
    if existing_record:  
        print("数据已存在")
        continue  
    else:  
        # 使用 API 密钥和自定义的 base_url 创建 OpenAI 客户端
        client = OpenAI(  
            api_key = my_api_key,  # 替换为你的实际 API 密钥
            base_url="https://api.aiproxy.io/v1"  # 使用自定义代理的基础 URL
        )  
        # 创建聊天补全请求
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    'role': 'user',
                    'content': [
                        {
                        "type": "text",
                        "text": f'这是模板文章：{exampleCardPage[i]}',
                        },
                        {
                        "type": "text",
                        "text": f"""
                        >>>这是新卡品信息：{newCardInfo}
                        >>>请参考模板文章，利用新卡片信息（不一定用到全部），生成一篇{cardtitles[i]}
                        >>>输出HTML格式并且美化一下页面
                        >>>不要有任何多余的开头结尾,只需要文章内容，严禁出现山东星卡的信息
                        >>>看文章需求可能需要加：用户可以通过&nbsp;<a href="https://h5.yapingtech.com/#/pages/sales_index/index?agent_id=3" target="_self"><em>亚平科技平台在线申请和购买</em></a>&nbsp;，渠道正规，操作简单快捷。              
                        """,
                        },
                    ],
                },               
            ]
        )
        # print(chat_completion)
        # 从 chat_completion 的 choices 属性中提取第一条消息的 content 属性
        content1 = chat_completion.choices[0].message.content
        newContent = content1.replace('<','&lt;').replace('>','&gt;').replace('&lt;em&gt;','&lt;em&gt;').replace('/','\/').replace('"','&quot;')
        # print(newContent)

        # 获取当前时间的Unix时间戳（秒）  
        now = datetime.datetime.now(datetime.timezone.utc)     
        current_timestamp = int(now.timestamp())  
        # 计算从现在起一天（24小时）前的时间戳  
        one_day_later = current_timestamp - 24 * 60 * 60  
        # 计算从现在起三天（72小时）前的时间戳  
        three_days_later = current_timestamp - 24 * 60 * 60 * 4     
        # 在一天前和三天前之间生成一个随机的时间戳  
        random_timestamp = random.randint(three_days_later,one_day_later)

        # 生成随机浏览量  
        post_hitss = random.randint(666, 3000)  
        # 假设点赞量与浏览量的比例是一个范围，比如每100到200次浏览有1次点赞  
        # 我们可以生成一个随机比例（例如，每10到20浏览1次点赞），然后计算点赞量  
        like_ratio_denominators = random.randint(10, 20)  
        post_likes = post_hitss // like_ratio_denominators        
        # 为了避免在极低浏览量时点赞量为0（虽然按照上述逻辑几乎不会发生），  
        # 我们可以添加一个最小点赞量的保障  
        if post_likes == 0:  
            post_likes = 1  # 或者选择一个更小的最小值

        post_data = {
        "categories": 15,
        "post_title": cardtitles[i],
        "post_keywords": cardreplacers[i],
        "post_source": "",
        "post_hits": post_hitss,
        "post_like": post_likes,
        "sort": "0",
        "post_excerpt": cardabstracts[i],
        "user_id": 1,
        "more": json.dumps({
            "audio": "",
            "video": "",
            "thumbnail": 'url',
            "template": "",
            # **ArticleInfo,
            # **(master or {})
        }),  # 将字典合并并编码为 JSON 字符串
        "thumbnail": 'url',
        "published_time": random_timestamp,  # 需要替换为你的时间变量
        "create_time": current_timestamp,  # 当前时间戳
        "update_time": current_timestamp,  # 当前时间戳
        "post_content": newContent  # 等同于 PHP 的 htmlentities
        }
        add_post(post_data)   
