import datetime  
import json
import random
from database import Session, add_post
# 获取当前时间的Unix时间戳（秒）  

session = Session()
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
# 创建新post对象:
# 定义数据字典
post_data = {
    "categories": 2,
    "post_title": 'test',
    "post_keywords": 's,sa,se',
    "post_source": "",
    "post_hits": post_hitss,
    "post_like": post_likes,
    "sort": "0",
    "post_excerpt": 'description',
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
    "post_content": 'html'  # 等同于 PHP 的 htmlentities
}
add_post(post_data) 