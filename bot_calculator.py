from hoshino import Service

help_str = '计算群聊中的四则运算消息，并发送结果\n使用方法：直接发送四则运算公式；如"1+1"'

sv = Service("四则运算器", help_=help_str)

VALID_SYMBOL_SET = {"+", "-", "*", "/"}
VALID_NUM_SET = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
VALID_ALL_SET = VALID_SYMBOL_SET | VALID_NUM_SET


def check_message_valid(input_str):
    # 因处理频率极高，出于性能考虑不使用正则匹配消息规则
    input_str_set = set(input_str)
    if input_str_set & VALID_SYMBOL_SET == set():
        # 至少包含一个四则运算符号
        return False
    if not input_str_set - VALID_ALL_SET == set():
        # 除了四则运算不能包含其它内容
        return False
    # 绝大部分消息在之前都已被过滤，可以适当增加复杂判定
    if {input_str[0]} & VALID_NUM_SET == set():
        if {input_str[0]} & {"+", "-"} == set():
            # 首位必须为数字或+-
            return False
        elif set(input_str[1:]) & VALID_SYMBOL_SET == set():
            # 首位为+-时后续消息至少包含一个运算符号
            return False
    if not {input_str[-1]} & VALID_SYMBOL_SET == set():
        # 不能以运算符号结尾
        return False
    if not input_str.find("/0") == -1:
        # 除零错误
        return False
    return True


@sv.on_message()
async def calc_message(bot, ev):
    eval_msg = ev.message.extract_plain_text()
    if not check_message_valid(eval_msg):
        # *安全警告：禁止禁用该消息有效性检查
        # 禁用消息有效性检查后会导致eval注入
        return
    await bot.send(ev, f"= {eval(eval_msg)}")
