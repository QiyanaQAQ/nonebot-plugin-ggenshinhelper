import traceback
from typing import Tuple

from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import Message
from nonebot.log import logger

__plugin_meta__ = PluginMetadata(
    name="原神查询补充工具",
    description="查询地图",
    usage="Map/查询地图 + 关键词",
    extra={
        "unique_name": "simplemusic",
        "example": "查询地图 神像",
        "author": "gjy <479760837@qq.com>",
        "version": "0.0.1",
    },
)

map_dic = {
    '神像':'2',
    '七天神像':'2',
    '锚点':'3',
    '传送锚点':'3',
    '秘境':'154',
    '忍冬之树':'158',
    '浪船':'190',
    '神樱':'316',

    '普通宝箱':'17',
    '精致的宝箱':'44',
    '珍贵的宝箱':'45',
    '华丽的宝箱':'46',
    '奇馈宝箱':'269',
    '宝箱':'17,44,45,46,269',

    '风神瞳':'5',
    '岩神瞳':'6',
    '雷神瞳':'194',
    '绯红玉髓':'141',

    '仙灵':'18,148',

    '限时挑战':'64',

    '丘丘人':'55',
    '丘丘萨满':'57',
    '盗宝团':'58',
    '史莱姆':'59',
    '野伏众':'209',
    '漂浮灵':'229',
    '愚人众':'54',
    '骗骗花':'47',

    '丘丘暴徒':'149',
    '大丘丘人':'149',
    '深渊法师':'24',
    '债务处理人':'25',
    '雷莹术士':'26',
    '遗迹机兵':'215',
    '遗迹重机':'150',
    '遗迹守卫':'27',
    '遗迹猎者':'28',
    '幼岩龙蜥':'49',
    '岩龙蜥':'169',
    '丘丘王':'53',
    '狂风之核':'257',
    '藏镜女士':'210',
    '镜女':'210',
    '兽境之狼':'265',
    '流血狗':'265',

    '落落莓':'29',
    '绝云椒椒':'30',
    '嘟嘟莲':'31',
    '清心':'32',
    '小灯草':'33',
    '琉璃袋':'34',
    '塞西莉亚花':'35',
    '霓裳花':'36',
    '蒲公英仔':'37',
    '琉璃百合':'38',
    '慕风蘑菇':'39',
    '石珀':'40',
    '钩钩果':'41',
    '夜泊石':'42',
    '风车菊':'43',
    '星螺':'78',
    '海灵芝':'185',
    '鬼兜虫':'196',
    '鸣草':'197',
    '血斛':'198',
    '绯樱绣球':'199',
    '晶化骨髓':'211',
    '珊瑚珍珠':'227',
    '天云草实':'228',
    '幽灯草':'266',


    '老石':'184',
    
    '晶蝶':'298,277,281,315',
    '雷晶蝶':'298',
    '冰晶蝶':'277',
    '风晶蝶':'281',
    '岩晶蝶':'315',
    
    '地灵龛':'8,9,212',
    '灵龛':'8,9,212',
    '蒙德地灵龛':'8',
    '璃月地灵龛':'9',
    '稻妻地灵龛':'212',

    '垂钓点':'261',
    '钓鱼':'261',

    '大伟丘':'87',

    '水晶':'16',
    '水晶矿':'16',
    '水晶块':'16',
    '魔晶矿':'80',
    '魔晶块':'80',
    '星银矿':'139',
    '星银块':'139',

    '圣遗物':'114',
    '狗粮':'114',

    '蒙德':'&center=75.22,-240.03&zoom=-0.50',
    '雪山':'&center=1165.00,0.00&zoom=0.00',
    '龙脊雪山':'&center=1165.00,0.00&zoom=0.00',
    '星落湖':'&center=-180.00,489.00&zoom=0.00',
    '苍风高地':'&center=263.32,-544.79&zoom=-0.50',
    '风起地':'&center=606.00,729.00&zoom=-0.50',
    '风龙废墟':'&center=-330.00,-663.00&zoom=0.00',

    '璃月':'&center=2348.00,-1703.00&zoom=-1.00',
    '狄花洲':'&center=1049.18,-1290.56&zoom=-0.50',
    '望舒客栈':'&center=1302.32,-1222.68&zoom=-0.50',
    '归离原':'&center=1798.19,-884.34&zoom=0.00',
    '无妄坡':'&center=741.75,-1185.75&zoom=1.00',
    '轻策庄':'&center=572.25,-1448.75&zoom=1.00',
    '琥牢山':'&center=1697.50,-2368.50&zoom=0.00',
    '庆云顶':'&center=1697.50,-2368.50&zoom=0.00',
    '璃月港':'&center=2864.50,-1299.50&zoom=0.00',
    '层岩地表':'&center=2882.50,-2544.50&zoom=1.50',
    '孤云阁':'&center=2503.50,-190.50&zoom=0.00',

    '稻妻':'&center=5585.71,2064.43&zoom=-1.50',
    '鹤观':'&center=8602.50,2169.50&zoom=-0.50',
    '清籁岛':'&center=6976.00,3466.00&zoom=-0.50',
    '海祈岛':'&center=6124.00,71.00&zoom=-0.50',
    '踏鞴砂':'&center=5836.00,2464.00&zoom=-0.50',
    '八酝岛':'&center=6068.00,1435.00&zoom=-0.50',
    '鸣神岛':'&center=4935.00,3512.00&zoom=-1.50',

}

def create_matchers():
    def create_handler() -> T_Handler:
        async def handler(matcher: Matcher, msg: Message = CommandArg()):
            keyword = msg.extract_plain_text().strip()
            url = "https://webstatic.mihoyo.com/ys/app/interactive-map/index.html?bbs_presentation_style=no_header&lang=zh-cn&_markerFps=24#/map/2?shown_types="
            if keyword and map_dic.has_key(keyword):
                param = map_dic[keyword]
                url = url + param

            await matcher.finish(url)
        return handler

    matcher = on_command(
        "Map",
        aliases=set(Tuple["Map","查询地图"]),
        block=True,
        priority=12,
    )
    matcher.append_handler(create_handler())



create_matchers()