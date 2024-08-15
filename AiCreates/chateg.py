import random
import time
import hashlib
from redis import Redis

class ProductService:

    def run_product(self, type_: str, data: dict, tid: int = 0) -> dict:
        result = {}
        try:
            # 构建 Redis 锁的键
            key = "str:temp_lock_p:" + self.encode({
                'type': type_,
                'data': data,
            })

            # 尝试获取 Redis 锁，如果成功就代表未发送
            redis_client = Redis()
            if redis_client.set(f"str:temp_lock_p:{key}", True, nx=True, px=86400 * 1000):
                # 如果 Redis 锁成功设置，表明任务未被处理
                pass

            # 根据类型调用不同的处理方法
            if type_ == 'json':
                result = self.product_chat_json(data)
            elif type_ == 'img':
                result = self.product_chat_img(data['url'], data['title'])
            elif type_ == 'text':
                result = self.product_chat_text(data['content'])
            elif type_ == 'poster':
                result = self.product_chat_poster(data['content'])
            else:
                raise Exception('未知的类型')

            # 获取标题信息
            title_info = self.get_product_title(result.get('title'))
            if not title_info['product']:
                raise Exception('请填写标题: ' + self.encode(title_info))

            # 检查标题是否已存在
            if self.is_title_exist(title_info['product']) and tid == 0:
                return {
                    'status': 2,
                    'msg': '标题已存在',
                }

            # 根据运营商设置分类 ID
            title_info['operator'] = title_info['operator'].replace('中国', '')
            if tid == 0:
                if '移动' in title_info['operator']:
                    tid = 3
                elif '联通' in title_info['operator']:
                    tid = 2
                elif '电信' in title_info['operator']:
                    tid = 1
                elif '广电' in title_info['operator']:
                    tid = 4
                else:
                    raise Exception(f"运营商错误: {title_info['operator']}")

            # 处理非 JSON 类型的数据
            if type_ != 'json':
                poster = self.get_product_poster(result['source'])
                if not poster['product']:
                    raise Exception('请填写产品名称: ' + self.encode(poster))

                url = self.generate_product_poster(
                    poster['operator'],
                    poster['product'],
                    poster['price'],
                    poster['national_traffic'],
                    poster['directional_traffic'],
                    poster['call_duration'],
                    poster['total']
                )
            else:
                url = data.get('zhutu')

            # 生成随机点击数和点赞数
            count = random.randint(66, 3000)
            like = count * random.randint(1, 3) // 13

            # 获取 SEO 信息
            seo = self.product_chat_desc(result['content'])
            if not seo['keywords']:
                raise Exception('请填写关键词: ' + self.encode(seo))

            # 生成文章内容
            title = result.get('title')
            time_ = self.generate_random_datetime()
            html = f"<p class='img-zhutu'><img src='{url}' alt='{title}'></p>{result.get('content')}"
            html = html.replace('<h1>', '<h2>').replace('</h1>', '</h2>')
            html = html.replace('中国', '')

            # 添加文章到数据库
            self.add_post({
                "categories": tid,
                "post_title": title,
                "post_keywords": seo['keywords'],
                "post_source": "",
                "post_hits": count,
                "post_like": like,
                "sort": "0",
                "post_excerpt": seo['description'],
                'user_id': 1,
                "more": self.encode({
                    "audio": "",
                    "video": "",
                    "thumbnail": url,
                    "template": "",
                    **title_info,
                    **poster if poster else {}
                }),
                'thumbnail': url,
                "published_time": time_,
                "create_time": int(time.time()),
                "update_time": int(time.time()),
                "post_content": html,
            })
            return {
                'status': 3,
                'message': '文章已生成',
            }

        except Exception as e:
            # 捕获所有异常并发送错误消息
            text = f"【{self.get_env()}:系统错误】生成文章失败: " + self.encode({
                'type': type_,
                'data': data,
                'result': result,
                'error': str(e),
            })
            self.message_feishu(text)
            return {
                'status': 0,
                'msg': str(e),
            }

    # 其他辅助方法如 encode, get_product_title, is_title_exist 等需要自行实现
