
class FastFill:

    def __init__(self) -> None:
        pass
    
    @classmethod
    def prompt_message(self, in_line, in_msg, in_history) -> list:
        prompt = f"""
        你是一个linux 终端专家
        请你根据以下提供的Background信息 根据用户的要求 User_request
        来补全 User_Command_Line 的内容
        Background: {in_history}
        User_Command_Line: {in_line}
        User_request: {in_msg}
        将你的输出用 <<< 和 >>> 包裹，同时将指令用$$$分割开来
        例如：<<<ls cat$$$cd cat$$$git checkout main>>>
        请你预测五个最有可能用户需要的命令
        """
        return [{"role": "user", "content": prompt}]

    @classmethod
    def get_commands(self, text):
        commands_str = text.split("<<<")[1].split(">>>")[0]
        commands_list = commands_str.split("$$$")
        return commands_list
