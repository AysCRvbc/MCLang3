import mclang.syntax.expressions.Return as return_expr
return_expr = return_expr.Parser

import mclang.syntax.blocks.If as if_block
if_block = if_block.Parser

import mclang.syntax.blocks.Else as else_block
else_block = else_block.Parser

import mclang.syntax.blocks.While as while_block
while_block = while_block.Parser

import mclang.syntax.blocks.Input as input_block
input_block = input_block.Parser

import mclang.syntax.blocks.Observer as observer_block
observer_block = observer_block.Parser

import mclang.syntax.blocks.Function as func_block
func_block = func_block.Parser

import mclang.syntax.expressions.Chat as chat
chat = chat.Parser

import mclang.syntax.expressions.Selector as selector
selector = selector.Parser

import mclang.syntax.expressions.Variable as var
var = var.Parser

import mclang.syntax.expressions.Configuration as config
config = config.Parser

import mclang.syntax.expressions.Execute as execute
execute = execute.Parser

import mclang.syntax.expressions.lang.Call as lang_call
lang_call = lang_call.Parser

import mclang.syntax.expressions.lang.VariableSet as lang_varset
lang_varset = lang_varset.Parser

import mclang.syntax.expressions.lang.Unary as lang_unary
lang_unary = lang_unary.Parser

import mclang.syntax.expressions.Default as default
default = default.Parser
