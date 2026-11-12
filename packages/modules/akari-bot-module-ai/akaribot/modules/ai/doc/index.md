# ai

调用大语言模型完成多轮对话、网页检索与图片生成，调用费用按模型单价折算成花瓣扣除。可用的模型与图像服务由管理员配置，未配置模型时返回配置提示。

## 命令

### `ai`

<CommandUsage :usage="['ai', 'ai [<prompt>] [--ctx <turn_id>] [--llm <llm>] [--no-tools]']" :params="['prompt=发给大语言模型的提问', 'turn_id=要延续的对话轮次 ID', 'llm=要使用的大语言模型']" permission="public" :options="[{flag: '--ctx', desc: '指定要延续的对话轮次 ID。'}, {flag: '--llm', desc: '指定使用的大语言模型。'}, {flag: '--no-tools', desc: '禁止大语言模型调用工具。'}]" />

与大语言模型聊天，省略提问时等待下一条消息作为提问。

每条回复末尾附带轮次 ID 与续接命令，上下文窗口保留 1000 秒。非超级用户两次调用间隔不少于 10 秒；超级用户不扣花瓣，也不受冷却限制。

### `ai llm list`

<CommandUsage usage="ai llm list [--price]" permission="public" :options="[{flag: '--price', desc: '同时显示具体价格信息。'}]" />

查看支持的大语言模型列表。

### `ai llm price`

<CommandUsage usage="ai llm price <llm>" :params="['llm=要查询价格的大语言模型']" permission="public" />

查看指定大语言模型的花瓣价格。

### `ai llm set`

<CommandUsage usage="ai llm set <llm>" :params="['llm=要设为默认的大语言模型']" permission="admin" />

设置当前场景内默认的大语言模型。

### `ai llm instruct`

<CommandUsage usage="ai llm instruct [<instructions>]" :params="['instructions=自定义命令内容']" permission="public" />

设置大语言模型的自定义命令，省略参数则清除。

### `ai llm persona`

<CommandUsage usage="ai llm persona" permission="public" />

设置是否开启人格化，效果因模型而异。
