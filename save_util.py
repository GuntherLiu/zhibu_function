#encoding=utf-8

import shelve
from zhibu_session import ZhibuSession
import logger


def do_read(key='zhibu_session'):
    read = shelve.open('zhibu_session.bat')
    try:
        value = read[key]
    finally:
        read.close()
    return value


def do_write(value, key='zhibu_session'):
    write = shelve.open('zhibu_session.bat')
    try:
        write[key] = value
    finally:
        write.close()

def test1():
    comment_page_index = 580
    do_write(comment_page_index,'comment_page_index')

    content1 = u'我们要不忘初心，继续前进'
    content2 = u'我们要全心全意为人民服务'
    content3 = u'我们要保护国家，保护人民，时刻牢记为人民服务'
    content4 = u'我们要时刻牢记，空谈误国，实干兴邦'
    content5 = u'要坚决维护祖国和人民的利益'
    content6 = u'关注时事，思考前进的方向，既要低头赶路，也要抬头看路'
    content7 = u'家事国事天下事，事事关心'
    forum_list = [content1, content2, content3, content4, content5, content6, content7]
    do_write(forum_list, 'forum_list')

    idea1 = u'进入新时代，国际国内形势发生广泛而深刻的变化，改革发展面临着新形势新任务新挑战，我们要抓住机遇、迎接挑战，关键在于高举新时代改革开放旗帜，继续全面深化改革、全面扩大开放'
    idea2 = u'实体经济是一国经济的立身之本、财富之源。先进制造业是实体经济的一个关键，经济发展任何时候都不能脱实向虚'
    idea3 = u'中华民族奋斗的基点是自力更生，攀登世界科技高峰的必由之路是自主创新，所有企业都要朝这个方向努力奋斗'
    idea4 = u'党的十八大后我考察调研的第一站就是深圳，改革开放40周年之际再来这里，就是要向世界宣示中国改革不停顿、开放不止步，中国一定会有让世界刮目相看的新的更大奇迹。'
    idea5 = u'要坚持以人民为中心，把为人民谋幸福作为检验改革成效的标准，让改革开放成果更好惠及广大人民群众。'
    idea6 = u'实践证明，改革开放道路是正确的，必须一以贯之、锲而不舍、再接再厉。民营企业对我国经济发展贡献很大，前途不可限量。党中央一直重视和支持非公有制经济发展，这一点没有改变、也不会改变。'
    idea7 = u'改革开放是党和人民大踏步赶上时代的重要法宝，是坚持和发展中国特色社会主义的必由之路，是决定当代中国命运的关键一招，也是决定实现“两个一百年”奋斗目标、实现中华民族伟大复兴的关键一招。'
    idea8 = u'要掌握辩证唯物主义和历史唯物主义的方法论，以改革开放的眼光看待改革开放，充分认识新形势下改革开放的时代性、体系性、全局性问题，在更高起点、更高层次、更高目标上推进改革开放。'
    ideal_list = [idea1, idea2, idea3, idea4, idea5, idea6, idea7, idea8]
    do_write(ideal_list, 'ideal_list')

    view1 = u'深入学习贯彻习近平新时代中国特色社会主义思想和党的十九大精神，牢固树立“四个意识”，带头坚决维护习近平总书记的核心地位、坚决维护党中央权威和集中统一领导，坚持正确政治方向。#正能量#'
    view2 = u'不忘初心，方得始终。中国共产党人的初心和使命，就是为中国人民谋幸福，为中华民族谋复兴。这个初心和使命是激励中国共产党人不断前进的根本动力。全党同志一定要永远与人民同呼吸、共命运、心连心，永远把人民对美好生活的向往作为奋斗目标，以永不懈怠的精神状态和一往无前的奋斗姿态，继续朝着实现中华民族伟大复兴的宏伟目标奋勇前进。#两学一做#'
    view3 = u'一面旗帜，鲜红 红到我的血液里 感受一种使命的力量 把共产主义理想的火种 埋进我的心田 一面旗帜，鲜红 红到我的心灵里 把跳动的心霎时照亮 入队时戴上红领巾 握紧心愿的第一缕阳光 书写我人生的青春诗章 为中国人民谋幸福 为中华民族谋复兴 用自己的血液 书写自信与奔放 与为人民服务相映 百年风云激荡 百年铸就辉煌  从少年到青年 从少先队员成长为共青团员 队旗团旗总连着党旗 党旗连着我的魂魄'
    view4 = u'因势而谋、应势而动、顺势而为。党的十八大以来，以习近平同志为核心的党中央重视互联网、发展互联网、治理互联网，统筹协调涉及政治、经济、文化、社会、军事等领域信息化和网络安全重大问题，作出一系列重大决策，提出一系列重大举措，形成了网络强国战略思想，网信事业取得历史性成就，我国正从网络大国阔步迈向网络强国。'
    view5 = u'全面从严治党，强化党内监督 “青松恨不高千尺，恶竹应须斩万竿” “官有所畏，业有所成” “有权不能任性，敬畏方得始终”'

    view_list = [view1, view2, view3, view4, view5]
    do_write(view_list,'view_list')


def test():
    zhibu_session = ZhibuSession()
    zhibu_session.do_login()
    if zhibu_session.is_login():
        logger.logger('login success')
        do_write(zhibu_session)
    else:
        logger.logger('login failed')


if __name__ == '__main__':
    test()
