from sqlalchemy import BigInteger, SmallInteger, Text, create_engine, Column, Integer, String  
from sqlalchemy.orm import declarative_base  
from sqlalchemy.orm import sessionmaker  
from contextlib import contextmanager  

Base = declarative_base()  
  
# 模型定义...  
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
  
class PortalCategoryPost(Base):  
    __tablename__ = 'tb_portal_category_post'   
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)  
    post_id = Column(BigInteger, nullable=False, default=0, comment='文章id')  
    category_id = Column(BigInteger, nullable=False, default=0, comment='分类id')   
    status = Column(Integer, nullable=False, default=1, comment='状态,1:发布;0:不发布')  
  
class PortalTag(Base):  
    __tablename__ = 'tb_portal_tag'  
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment='分类id')  
    status = Column(Integer, nullable=False, default=1, comment='状态,1:发布,0:不发布')  
    recommended = Column(Integer, nullable=False, default=0, comment='是否推荐;1:推荐;0:不推荐')  
    post_count = Column(BigInteger, nullable=False, default=0, comment='标签文章数')  
    name = Column(String(20), nullable=False, default='', comment='标签名称')
  
class PortalTagPost(Base):  
    __tablename__ = 'tb_portal_tag_post'
    tag_id = Column(BigInteger, primary_key=True, nullable=False, default=0, comment='标签 id')  
    post_id = Column(BigInteger, primary_key=True, nullable=False, default=0, comment='文章 id')  
    status = Column(Integer, nullable=False, default=1, comment='状态,1:发布;0:不发布')
  


engine = create_engine('mysql+pymysql://root:root_123456@192.168.137.200:3306/yp_site')  # 替换为你的数据库连接字符串
Session = sessionmaker(bind=engine)
session = Session()
# 数据库连接的上下文管理器
@contextmanager
def db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

def add_post(data):
    # 处理 post_keywords，将中文逗号替换为英文逗号，并用英文逗号替换空格
    data['post_keywords'] = data['post_keywords'].replace('，', ',').replace(' ', ',')
    # 处理 post_title，去除 '中国'
    data['post_title'] = data['post_title'].replace('中国', '')

    # 将关键词字符串按逗号分割为列表
    keywords = data['post_keywords'].split(',')

    with db_session() as session:
        # 获取分类ID并从数据中删除
        categories_id = data.pop('categories')
        
        # 向 PortalPost 表中插入数据并获取插入的ID
        post = PortalPost(**data)
        session.add(post)
        session.flush()  # 获取插入的ID
        post_id = post.id

        # 删除原有的分类关联记录
        session.query(PortalCategoryPost).filter_by(post_id=post_id).delete()

        # 插入新的分类关联记录
        category_post = PortalCategoryPost(category_id=categories_id, post_id=post_id)
        session.add(category_post)

        # 删除原有的标签关联记录
        session.query(PortalTagPost).filter_by(post_id=post_id).delete()

        # 如果关键词不为空，则处理标签
        if keywords:
            for keyword in keywords:
                if not keyword:
                    continue

                # 查找标签是否已存在
                tag = session.query(PortalTag).filter_by(name=keyword).first()

                if not tag:
                    # 标签不存在，插入新标签并获取ID
                    tag = PortalTag(name=keyword)
                    session.add(tag)
                    session.flush()  # 获取插入的ID
                    tag_id = tag.id
                else:
                    # 标签已存在，获取其ID
                    tag_id = tag.id

                # 插入标签与文章的关联记录
                tag_post = PortalTagPost(tag_id=tag_id, post_id=post_id)
                session.add(tag_post)
  