import mclang.syntax.blocks.If as if_block
import mclang.syntax.blocks.Else as else_block
import mclang.syntax.blocks.While as while_block
import mclang.syntax.blocks.Input as input_block
import mclang.syntax.blocks.Observer as observer_block
import mclang.syntax.blocks.Function as func_block
import mclang.syntax.expressions.Chat as chat
import mclang.syntax.expressions.Selector as selector
import mclang.syntax.expressions.Variable as var
import mclang.syntax.expressions.Configuration as config
import mclang.syntax.expressions.Execute as execute
import mclang.syntax.expressions.Default as default

if_block = if_block.Parser
else_block = else_block.Parser
while_block = while_block.Parser
input_block = input_block.Parser
observer_block = observer_block.Parser
func_block = func_block.Parser
chat = chat.Parser
selector = selector.Parser
var = var.Parser
config = config.Parser
execute = execute.Parser
default = default.Parser
