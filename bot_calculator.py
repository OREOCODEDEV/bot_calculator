from hoshino import Service

help_str = '计算群聊中的四则运算消息，并发送结果\n使用方法：直接发送四则运算公式；如"1+1"'

sv = Service("四则运算器", help_=help_str)

VALID_SYMBOL_SET = {"+", "-", "*", "/"}
VALID_NUM_SET = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", " "}
VALID_ALL_SET = VALID_SYMBOL_SET | VALID_NUM_SET


def check_message_valid(input_str):
    input_str_set = set(input_str)
    if input_str_set & VALID_SYMBOL_SET == set():
        # 至少包含一个四则运算符号
        return False
    if not input_str_set - VALID_ALL_SET == set():
        # 除了四则运算不能包含其它内容
        return False
    if {input_str[0]} & (VALID_NUM_SET | {"+", "-"}) == set():
        # 首位必须为数字或+-
        return False
    if not {input_str[-1]} & VALID_SYMBOL_SET == set():
        # 不能以运算符号结尾
        return False
    return True


@sv.on_message()
async def calc_message(bot, ev):
    eval_msg = str(ev.message)
    if not check_message_valid(eval_msg):
        return
    await bot.send(ev, "= %f" + eval(eval_msg))
