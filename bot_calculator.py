from hoshino import Service

help_str = '计算群聊中的四则运算消息，并发送结果\n使用方法：直接发送四则运算公式；如"1+1"'

sv = Service("四则运算器", help_=help_str)

VALID_SYMBOL_SET = set(["+", "-", "*", "/"])
VALID_NUM_SET = set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", " "]) | VALID_SYMBOL_SET


def check_message_valid(input_str):
    if not set(input_str) - VALID_NUM_SET == set([]):
        return False
    if set(input_str) & VALID_SYMBOL_SET == set([]):
        return False
    return True


@sv.on_message()
async def calc_message(bot, ev):
    try:
        eval_msg = str(ev.message)
        if not check_message_valid(eval_msg):
            return
        result = "= " + str(eval(eval_msg))
        await bot.send(ev, result)
    except Exception as e:
        sv.logger.error("An error occurred while trying calculate with this message:%s ,%s ,%s" % (ev.message, Exception, e))
