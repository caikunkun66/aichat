from sqlalchemy import create_engine, Column, Integer, String, ForeignKey,BigInteger, SmallInteger,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 定义表模型
class PortalPost(Base):
    __tablename__ = 'tb_portal_post'  # 替换为你的表名

    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    parent_id = Column(BigInteger, nullable=False, default=0, comment='父级id')
    post_type = Column(SmallInteger, nullable=False, default=1, comment='类型,1:文章;2:页面')
    post_format = Column(SmallInteger, nullable=False, default=1, comment='内容格式;1:html;2:md')
    user_id = Column(BigInteger, nullable=False, default=0, comment='发表者用户id')
    post_status = Column(SmallInteger, nullable=False, default=1, comment='状态;1:已发布;0:未发布')
    comment_status = Column(SmallInteger, nullable=False, default=1, comment='评论状态;1:允许;0:不允许')
    is_top = Column(SmallInteger, nullable=False, default=0, comment='是否置顶;1:置顶;0:不置顶')
    recommended = Column(SmallInteger, nullable=False, default=0, comment='是否推荐;1:推荐;0:不推荐')
    post_hits = Column(BigInteger, nullable=False, default=0, comment='查看数')
    post_favorites = Column(Integer, nullable=False, default=0, comment='收藏数')
    post_like = Column(BigInteger, nullable=False, default=0, comment='点赞数')
    comment_count = Column(BigInteger, nullable=False, default=0, comment='评论数')
    create_time = Column(Integer, nullable=False, default=0, comment='创建时间')
    update_time = Column(Integer, nullable=False, default=0, comment='更新时间')
    published_time = Column(Integer, nullable=False, default=0, comment='发布时间')
    delete_time = Column(Integer, nullable=False, default=0, comment='删除时间')
    post_title = Column(String(100), nullable=False, default='', comment='post标题')
    post_keywords = Column(String(150), nullable=False, default='', comment='seo keywords')
    post_excerpt = Column(String(10000), nullable=False, default='', comment='post摘要')
    post_source = Column(String(150), nullable=False, default='', comment='转载文章的来源')
    thumbnail = Column(String(100), nullable=False, default='', comment='缩略图')
    post_content = Column(Text, nullable=True, comment='文章内容')
    post_content_filtered = Column(Text, nullable=True, comment='处理过的文章内容')
    more = Column(Text, nullable=True, comment='扩展属性,如缩略图;格式为json')
    subhead = Column(String(255), nullable=True, comment='副标题')
    sort = Column(Integer, nullable=False, default=10000, comment='排序')


# 配置数据库连接
engine = create_engine('mysql+pymysql://root:root_123456@192.168.137.200:3306/yp_site')  # 替换为你的数据库连接字符串
Session = sessionmaker(bind=engine)
session = Session()
# 假设我们要插入的数据包含字段 unique_field  
post_title_value = '中国电信 - 电信星冬卡19元185G - 畅享联通'  
  
# 检查 unique_field 是否已经存在  
existing_record = session.query(PortalPost).filter_by(post_title=post_title_value).first()  
  
if existing_record:  
    print("数据已存在")  
else:  
    # 创建新User对象:
    new_page = PortalPost(
    post_format=1,
    user_id=2002,
    post_status=1,
    comment_status=1, 
    is_top=0, 
    recommended=0, 
    post_hits=0,                            #浏览量
    post_favorites=0,                       #收藏量
    post_like=0,                            #点赞量
    comment_count=0, 
    create_time=0, 
    update_time=0, 
    published_time=0, 
    delete_time=0,
    post_title='示例文章标题', 
    post_keywords='关键词1,关键词2', 
    post_excerpt='摘要内容', 
    thumbnail='缩略图URL',
    post_content='文章内容', 
    )
    # 添加到session:
    session.add(new_page)
    # 发送SQL命令但不提交事务  
    session.flush()  
    # 现在可以访问new_user.id了  
    print(new_page.id)  
    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()

# def add_post(data: dict) -> None:
#     data['post_keywords'] = data['post_keywords'].replace('，', ',').replace(' ', ',')
#     data['post_title'] = data['post_title'].replace('中国', '')
#     keywords = data['post_keywords'].split(',')

#     try:
#         session.begin()  # 开始事务

#         # 插入新文章并获取 ID
#         post = PortalPost(
#             post_title=data['post_title'],
#             post_keywords=data['post_keywords'],
#             post_excerpt=data['post_excerpt'],
#             thumbnail=data['thumbnail']
#             # 添加其他需要的字段
#         )
#         session.add(post)
#         session.flush()  # 刷新以获取插入的 ID
#         post_id = post.id

#         # 更新分类
#         categories_id = data.pop('categories')
#         session.query(PortalCategoryPost).filter_by(post_id=post_id).delete()
#         category_post = PortalCategoryPost(category_id=categories_id, post_id=post_id)
#         session.add(category_post)

#         # 插入或更新标签
#         session.query(PortalTagPost).filter_by(post_id=post_id).delete()
#         for keyword in keywords:
#             if not keyword:
#                 continue
#             tag = session.query(PortalTag).filter_by(name=keyword).first()
#             if tag is None:
#                 tag = PortalTag(name=keyword)
#                 session.add(tag)
#                 session.flush()  # 刷新以获取插入的 ID
#             tag_post = PortalTagPost(tag_id=tag.id, post_id=post_id)
#             session.add(tag_post)

#         session.commit()  # 提交事务
#     except Exception as e:
#         session.rollback()  # 回滚事务
#         print(f"An error occurred: {e}")
#         raise

# 使用示例
# data = {
#     'post_title': '示例文章标题',
#     'post_keywords': '关键词1, 关键词2',
#     'post_excerpt': '摘要内容',
#     'thumbnail': '缩略图URL',
#     'categories': 1,
#     # 添加其他需要的字段
# }
# add_post(data)
