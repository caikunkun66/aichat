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
山东星卡由山东电信官方发行，亚平科技平台提供销售服务，拥有官方授权，确保每一张卡品的正规性和售后服务的有保障。选择这款卡，您无需担心用卡后的归属问题，正规合法。

办理流程：

    选择心仪套餐(用户可以通过 亚平科技平台在线申请和购买 ，渠道正规，操作简单快捷。)

    提交实名资料(需本人实名资料)

    审核通过后发货

    收到后自助激活(在线激活方便快捷，只需关注官方公众号或前往运营商指定的渠道进行办理和激活即可。在激活过程中需要上传身份证信息和进行活体认证以确保用户身份的真实性。)

    激活成功开始使用



注意事项：

本套餐专为官方正规手机卡，非物联网卡。

激活方式为自动激活，激活预存100元。

办理年龄范围为20-65周岁。

个人擅自买卖实名电话卡属违法行为,请勿将号卡租借、贩卖给他人如被他人利用发生涉恐、诈骗、骚扰等非法违规行为您将承担相应法律责任,请您确保规范使用：

            (1)切勿将短信随机码告知他人,务必自行输入。

            (2)切勿将本人办理的手机卡买卖、出借和给与他人。

            (3)切勿协助他人进行身份信息认证。


''',
'''
山东星卡官方办理入口指南

在寻找高效、便捷的通信服务时，山东星卡无疑是众多用户的心仪之选。作为由山东电信官方发行的优质手机卡，山东星卡不仅提供了多样化的套餐选择，还通过正规渠道确保了每一张卡片的正规性和售后服务的全面保障。对于想要在亚平科技平台办理山东星卡的用户来说，了解官方办理入口及流程至关重要。

办理入口：
    亚平科技平台 作为电信官方授权的销售平台，是您办理山东星卡的官方、正规渠道。在亚平科技平台上，您可以轻松找到山东星卡的各类套餐信息，并进行在线申请和购买。该平台操作简便，流程透明，能够为您提供一站式的购卡体验。

办理流程详解
选择心仪套餐：
首先，登录亚平科技平台，浏览山东星卡提供的多种套餐选项。根据您的通信需求和预算，选择最适合自己的套餐。亚平科技平台提供详尽的套餐介绍和比较，帮助您做出明智的选择。
提交实名资料：
在选定套餐后，按照平台提示填写并提交实名资料。请注意，确保提供的资料真实有效，以便通过后续的审核流程。
审核通过后发货：
您的申请资料将提交至山东电信官方进行审核。审核通过后，亚平科技平台将迅速为您发货，确保您能够尽快收到心仪的山东星卡。
收到后自助激活：
收到山东星卡后，您可以通过关注官方公众号或前往运营商指定的渠道进行自助激活。激活过程简单快捷，只需按照提示上传身份证信息和进行活体认证即可。请确保在激活过程中保持网络连接畅通，以便顺利完成激活。
激活成功开始使用：
激活成功后，您就可以开始享受山东星卡带来的优质通信服务了。无论是日常通话、上网冲浪还是其他通信需求，山东星卡都能满足您的期待。
注意事项
正规性保证：山东星卡为官方正规手机卡，非物联网卡。请用户放心使用。

激活预存：激活时需预存100元，具体详情请以平台或官方公告为准。

年龄限制：办理年龄范围为20-65周岁，请符合条件的用户进行申请。

规范使用：个人擅自买卖实名电话卡属违法行为。请用户务必规范使用手机卡，切勿将短信随机码告知他人、买卖或出借手机卡给他人使用，以免承担不必要的法律责任。

通过亚平科技平台办理山东星卡是一个便捷、安全的选择。作为官方授权的销售平台，亚平科技将为您提供全方位的购卡服务和售后保障。赶快行动起来吧！
''',
'''
山东星卡作为一种大流量卡套餐，在市场上具有多个显著的优点，以下是对其优点的详细归纳：

——————————————————————————————————————————————————

    ①长期稳定的套餐: 提供长达20年的长期套餐，用户购买后无需担心套餐变动或频繁更换的问题，享受长期的稳定服务。这种长期性不仅为用户省去了频繁充值的麻烦，还能够在一定程度上节省通讯费用。

    ②高性价比: 套餐价格相对较低，但提供的流量却相当充足。例如，29元即可享受155G的通用流量和30G的定向流量，这对于需要大量流量的用户来说是非常划算的。此外，其流量使用也相对灵活，超出套餐部分按5元/G计费，用户可以根据自己的需求灵活使用。

    ③高速稳定的网络: 支持5G网络并兼容4G，用户可以根据自己所在地区的网络情况选择使用。其网络速度稳定且快速，无论是浏览网页、观看高清视频还是进行在线游戏，都能得到流畅而稳定的网络连接。

    ④激活选号的便利性: 支持用户在线激活并选号，这一功能打破了传统流量卡固定号码的限制，让用户可以根据自己的喜好和需求选择一个独特的号码。这种个性化的选号方式不仅增加了用户的满意度，还使得沟通更加有趣和个性化。

    ⑤便捷的销户操作: 支持用户通过APP直接进行线上销户操作，无需到营业厅办理繁琐的手续。这一功能为用户提供了极大的便利，使得用户在使用过程中更加省心省力。

    ⑥不断升级的流量: 具备不断升级流量的特点。例如，其套餐从最初的100G升级到185G，但价格并未上涨。这种加量不加价的方式让用户感受到了实实在在的优惠和福利。

-------------------------------------------------------------------------------------------------------------------------------------

虽然具有诸多优点，但也存在一些缺点，以下是对其缺点的归纳：

——————————————————————————————————————————————————

    ①不赠送语音通话时长：山东星卡套餐主要侧重于流量服务，并不包含免费的语音通话时长。如果用户需要频繁进行语音通话，可能需要额外支付通话费用，这对于通话需求较高的用户来说可能不太友好。

    ②流量加包实现，不能开副卡共享：山东星卡的流量是通过加包方式实现的，这意味着用户无法将流量共享给副卡或其他设备使用。这对于有多设备上网需求的用户来说可能不太方便。

    ③不能跨月使用：山东星卡的流量使用通常是按月计算的，无法跨月累积使用。如果用户在本月内没有使用完套餐内的流量，剩余的流量将在月底清零，无法留到下个月继续使用。

    ④归属地可能因收货地而异：由于山东星卡的销售渠道和方式可能因地区而异，因此用户购买后可能发现卡的归属地并非自己所在的城市或地区。这可能会对某些用户造成一定的不便，特别是在需要享受特定地区优惠或服务时。

    ⑤可能需要二次身份证认证：为了保障用户的信息安全和防止电信诈骗等违法行为，山东星卡在激活或使用过程中可能会要求用户进行二次身份证认证。虽然这是为了用户的安全考虑，但也可能给用户带来一定的麻烦和不便。

-------------------------------------------------------------------------------------------------------------------------------------

需要注意的是，以上缺点并非山东星卡所独有，而是部分流量卡或电话卡套餐可能存在的共性问题。用户在选择购买时可以根据自己的实际需求和情况进行权衡和考虑。同时，随着市场的变化和技术的进步，山东星卡也在不断优化和改进产品和服务，以更好地满足用户的需求和期望。
''',
'''
实名认证条件：

需填写机主本人姓名及身份证号码

套餐电话卡到手后需上传身份证正面、反面及本人正面免冠照片进行激活

线上登记的机主姓名需与实名开户的机主姓名及身份证信息一致

开户和激活信息将在国政通联网对比，通过后才能激活使用

办理年龄：

20-65周岁

激活方式：

自助激活，激活时需强制充值100元话费

资费及优惠：

激活需充值100元，不充值无法享受优惠活动

原套餐资费：29元/月，包含30G定向流量。优惠后资费：29元/月，包含155G通用流量+30G定向流量

首月赠送30元体验金，即首月免租，套餐流量按天折算到账

激活72小时内自动叠加流量包、减免包，月租保持29元，包含155G通用流量和30G定向流量（赠送流量有效期20年）

发货说明：

新疆、西藏、云南及偏远地区无法发货，具体以运营商审核为准

请注意，以上信息基于提供的描述整理，具体办理时还需参考相关运营商的详细规定和政策
''',
'''
山东星卡的激活流程相对简单且便捷，以下是一个详细的激活步骤指南：

激活前准备：
确保您已经收到了山东星卡的实体卡片。

准备好您的身份证原件，因为激活过程中需要进行身份验证。

确保您的手机能够访问互联网，以便完成在线激活。

激活步骤：
关注官方公众号：

打开微信APP，搜索并关注“山东电信”微信公众号。如果找不到，可以尝试搜索“中国电信”官方公众号，因为激活流程可能因地区而异，但总体流程相似。

进入激活界面：

在公众号菜单中找到“新号卡开通”或类似的选项，点击进入激活界面。如果公众号中没有直接的激活入口，您可以尝试在公众号内发送关键词如“激活”、“新号卡”等，以获取激活链接或指导。

上传身份证信息：

按照提示，上传您的身份证正反面照片。请确保照片清晰、四角完整，并在光线充足的环境下拍摄。

完成活体认证：

根据提示，进行活体认证。这通常涉及到录制一段视频或进行面部识别，以确保是您本人在操作。

选号与确认：

在完成身份验证后，您将进入选号界面。由于山东星卡通常是当地运营商推出的优惠套餐，可能无法选择特定归属地的号码，但您可以在提供的号码中选择一个满意的。

确认您的选择并继续下一步。

充值与激活：

根据提示进行首次充值。通常，山东星卡会有首充优惠活动，如首充100元送话费等，按照要求完成充值。

充值成功后，您的山东星卡将被正式激活。此时，您可以开始享受套餐内的各项服务了。

注意事项
在激活过程中，请确保您提供的信息真实有效，以免影响激活成功率和后续使用。

如果您在激活过程中遇到任何问题，可以联系平台客服人员寻求帮助。他们将通过电话、在线客服等方式为您提供支持。

激活后，请妥善保管您的山东星卡及相关信息，以免丢失或被盗用。

此外，虽然不同渠道或时间点的激活流程可能略有差异，但总体上都遵循上述步骤。如果您在激活过程中遇到与上述步骤不符的情况，请以实际操作为准。
''',
'''
对于山东星卡是否真实的问题，我们可以从以下几个方面进行验证：

—————————————————————————————————————————————————————

官方认证与授权：山东星卡由山东电信官方出品，具有正式的官方认证和授权。这意味着该卡符合国家通信行业的各项规定和标准，经过了严格的测试和审核。
官方渠道查询：通过电信的官方网站、客服热线或官方授权的平台等渠道，可以查询到关于山东星卡的详细信息，包括套餐内容、资费标准、办理流程等。
用户评价：在各大电商平台、社交媒体或电信的用户论坛上，可以搜索到关于山东星卡的用户评价。真实的用户反馈可以帮助我们了解该卡的实际使用情况和服务质量。
套餐细节：了解套餐的具体内容，如流量大小、有效期、是否支持5G等，以及是否有额外的限制条件，如不能开副卡、不能跨月使用等。
激活与办理流程：了解并确认该卡的激活和办理流程是否正规、便捷。山东星卡提供了详细的办理指南和客户服务支持。
-------------------------------------------------------------------------------------------------------------------------------------

山东星卡确实是由电信发行的，它是真实存在且可靠的。但请注意，由于市场上存在各种类似的流量卡套餐，且信息可能随时间发生变化，因此在购买前请务必通过官方渠道进行确认和查询。
''',
'''
山东星卡目前不支持办理副卡，山东星卡是否可以办理副卡可能因不同套餐和地区政策而异。

山东星卡在过去是支持办理副卡的，并且可以与主卡共享账户余额，享受同样的折扣优惠，这为用户提供了很大的便利。

随着时间和政策的变化，可能有些套餐或地区已经不再支持办理副卡，或者对副卡的办理设置了新的条件和限制。

因此，在考虑办理山东星卡副卡时，可以采取以下步骤以确保获取最准确的信息)：

访问官方渠道：直接访问山东电信的官方网站或关注其官方微信公众号，查找关于山东星卡及副卡办理的最新政策和信息。
咨询客服：拨打山东电信的客服热线或在线联系客服人员，咨询您所在地区及所选套餐是否支持办理副卡，并了解具体的办理流程和条件。
关注优惠活动：山东电信可能会不定期推出优惠活动，包括副卡免费用或享受一定补贴等，您可以关注这些活动以获取更多实惠。
由于政策和信息可能随时变化，无法完全反映当前最新情况。因此，在办理之前，请务必通过官方渠道获取最准确的信息。
''',
'''
山东星卡作为一款大流量卡套餐，在市场上凭借其独特的优势和稳定的性能，赢得了不少用户的青睐。那么，它到底好不好用呢？我们可以从以下几个方面进行综合评价：

一、套餐内容丰富，性价比高

山东星卡提供了多种套餐选择，尤其是其主打套餐，如29元享受185G（含155G通用+30G定向）的流量，这在市场上是极具竞争力的。对于需要大量流量的用户来说，这无疑是一个非常划算的选择。而且，山东星卡的套餐价格相对稳定，用户无需担心价格频繁波动，能够长期享受高性价比的流量服务。

二、网络稳定，速度快

山东星卡支持5G网络并兼容4G，这意味着用户可以根据自己所在地区的网络情况选择最适合自己的网络模式。无论是浏览网页、观看高清视频还是进行在线游戏，山东星卡都能提供稳定且快速的网络连接，确保用户在使用过程中不会遇到卡顿或掉线等问题。

三、激活与办理流程简便

用户购买山东星卡后，可以通过官方公众号或运营商指定的渠道进行激活和办理。整个流程相对简单快捷，用户只需按照提示上传身份证信息和进行活体认证即可。这种便捷的办理方式大大节省了用户的时间和精力。

四、用户反馈积极

从用户的反馈来看，山东星卡的口碑普遍较好。用户认为其套餐性价比高、流量多、资费低，且服务稳定可靠。虽然有一些用户提到山东星卡不赠送语音通话时长，但对于大多数以流量为主的用户来说，这并不影响其使用体验。

五、平台售后有保障

山东星卡由中国电信官方发行，并由具有十年行业经验的亚平科技平台提供销售服务。这为用户提供了强有力的售后保障。用户在使用过程中遇到任何问题或需要咨询时，都可以及时联系客服并获得专业的解答和帮助。

六、需注意的缺点

当然，任何产品都不是完美的。山东星卡也存在一些需要用户注意的地方。例如，它不赠送语音通话时长，对于通话需求较高的用户来说可能不太友好；其流量不能跨月使用，剩余流量将在月底清零；归属地可能因收货地而异等。但这些缺点并非山东星卡所独有，而是部分流量卡或电话卡套餐可能存在的共性问题。

------------------------------------------------------------------------------------------------------------------------------------

综上所述，山东星卡作为一款大流量卡套餐，在套餐内容、性价比、网络稳定性、激活办理流程以及用户反馈等方面都表现出色。虽然它也存在一些需要用户注意的地方，但总体来说是一款非常实用的流量卡产品。对于需要大量流量的用户来说，山东星卡无疑是一个值得考虑的选择。
''',
'''
山东星卡作为一种流量卡套餐，其靠谱性和真实性可以从以下几个方面来评估：

——————————————————————————————————————————————————

一、正规性与稳定性

    正规性：山东星卡是正规的流量卡套餐，由山东电信官方出品。其提供的套餐内容和服务均符合相关法规和政策要求。

    稳定性：相比其他大流量卡套餐，山东星卡具有更高的稳定性。它不仅可以长期办理，很少下架，而且套餐有效期长达20年，用户无需担心套餐随时变动或失效的问题。  

二、套餐内容与性价比

    套餐内容：山东星卡提供29元185G（含155G通用+30G定向）流量套餐。这些套餐不仅月租费用相对较低，而且提供的流量也相对较多，非常适合需要大流量的用户。

    性价比：从性价比角度来看，山东星卡的套餐内容非常划算。用户可以根据自己的需求选择合适的套餐，并在长期内享受稳定的流量服务。

三、用户评价与反馈

    用户对山东星卡的评价普遍较为积极。他们认为山东星卡套餐性价比高、流量多、资费低，且服务稳定可靠。同时，也有部分用户提到山东星卡不赠送语音通话时长，但通话费用较低（0.1元/分钟），对于通话需求不高的用户来说影响不大。

四、激活与办理流程

    山东星卡的激活和办理流程相对简单快捷。用户只需关注官方公众号或前往运营商指定的渠道进行办理和激活即可。在激活过程中需要上传身份证信息和进行活体认证以确保用户身份的真实性。

五、平台售后保障

    山东星卡由中国电信官方发行，亚平科技平台提供销售服务，具有十年行业经验，拥有官方授权，确保每一张卡品的正规性和售后服务的有保障。选择这款卡，您无需担心用卡后的归属问题，正规合法。

六、注意事项

    用户在办理山东星卡时需要注意套餐的具体内容和有效期等信息，并根据自己的需求选择合适的套餐。

    激活过程中需要按照提示进行操作并充值一定金额的话费以享受优惠活动。同时需要注意不要更换卡槽或进行其他可能影响风控的行为以免被系统风控。



-------------------------------------------------------------------------------------------------------------------------------------

综上所述，山东星卡是一种靠谱的、真实的流量卡套餐。它具有正规性、稳定性、高性价比等优点，并且得到了用户的积极评价。用户在办理和激活过程中仍需注意相关事项以确保顺利使用。
''',
'''
山东星卡是正规卡，以下是关于其正规性的详细介绍：

——————————————————————————————————————————————————————

官方认证与授权：山东星卡由山东电信官方出品，具有正式的官方认证和授权。这意味着该卡不仅符合国家通信行业的各项规定和标准，还经过了严格的测试和审核，确保了服务的正规性和合法性。用户在电信营业厅或官方渠道购买时，均可得到官方的核验和说明，进一步保证了购买的正规性。
套餐内容与稳定性：山东星卡提供多种大流量套餐选择，如29元185G（含155G通用+30G定向）等，满足不同用户的流量需求。这些套餐不仅流量充足、资费合理，而且具有高度的稳定性，用户可以长期使用而无需担心套餐随时变动或失效的问题。此外，套餐有效期长达20年，为用户提供了长期稳定的流量服务保障。
用户评价与反馈：山东星卡在市场上广受欢迎，众多用户对其给予了高度评价。用户普遍认为其套餐性价比高、流量多、资费低，且服务稳定可靠。这些正面的用户评价和反馈，进一步证明了山东星卡的正规性和可靠性。
激活与办理流程：山东星卡的激活和办理流程简单快捷，用户可以通过官方公众号或运营商指定的渠道进行办理和激活。这一流程的设计，不仅方便了用户，也进一步保证了服务的正规性和合法性。
平台售后保障：山东星卡由山东电信官方发行，并由具有丰富行业经验的亚平科技平台提供销售服务。这意味着用户在购买和使用过程中，可以享受到电信公司提供的强大售后保障。任何问题和纠纷，都可以得到及时有效的解决。
---------------------------------------------------------------------------------------------------------------------------------------

综上所述，山东星卡作为一张由电信公司正规销售和发行的电话卡套餐，具有官方认证和授权、稳定的套餐内容、积极的用户评价、便捷的激活办理流程以及强大的售后保障。可以确认山东星卡是正规卡。
'''
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