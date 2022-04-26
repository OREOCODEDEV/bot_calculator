from hoshino import Service

sv = Service(
    "四则运算器",
    help_="""四则运算器\n
    计算群聊中的四则运算消息，并发送结果\n
    使用方法：直接发送四则运算公式；如"1+1\"""",
)


def check_message_valid(input_str):
    valid_str_set = set(
        ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "+", "-", "*", "/", ".", " "]
    )
    return True if input_str - valid_str_set == set([]) else False


@sv.on_message()
async def calc_message(bot, ev):
    try:
        eval_msg = str(ev.message)
        if not check_message_valid(eval_msg):
            await bot.finish()
        result = "= " + str(eval(eval_msg))
        await bot.send(ev, result)
    except Exception as e:
        sv.logger.error(
            "An error occurred while trying calculate with this message:%s ,%s ,%s"
            % (ev.message, Exception, e)
        )
