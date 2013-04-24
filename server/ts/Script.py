# coding=UTF-8
#
# thickishstring server
# Copyright © 2013 David Given
#
# This software is redistributable under the terms of the Simplified BSD
# open source license. Please see the COPYING file in the distribution for
# the full text.

import logging
import ply.lex as lex
import ply.yacc as yacc
import ast

# --- Lexer -----------------------------------------------------------------

keywords = {
	'true': 'TRUE',
	'false': 'FALSE',
	'not': 'NOT',
	'and': 'AND',
	'or': 'OR',
	'if': 'IF',
	'then': 'THEN',
	'else': 'ELSE',
	'elseif': 'ELSEIF',
	'endif': 'ENDIF',
	'for': 'FOR',
	'next': 'NEXT',
	'break': 'BREAK',
	'continue': 'CONTINUE'
}

tokens = keywords.values() + [
	"ID",
	"NL",
	"NUMBER",
	"EQ",
	"NE",
	"LT",
	"LE",
	"GT",
	"GE",
	"ASSIGN"
]

literals = [
	"(", ")", ":", "+", "-", "*", "/", "%", "$", "."
]

t_ignore = ' \t'

def t_COMMENT(t):
	r';[^\n]*'
	pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    return t

def t_NL(t):
	r'\n'
	t.lexer.lineno += 1
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

t_EQ = r'=='
t_NE = r'(!=)|(<>)'
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'
t_ASSIGN = r'='

def t_error(t):
	logging.error("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

# --- Parser/compiler -------------------------------------------------------

alu_infix_operator_map = {
	'+': ast.Add,
	'-': ast.Sub,
	'*': ast.Mult,
	'/': ast.Div,
	'%': ast.Mod,
}

cmp_infix_operator_map = {
	'=': ast.Eq,
	'==': ast.Eq,
	'<>': ast.NotEq,
	'!=': ast.NotEq,
	'<': ast.Lt,
	'<=': ast.LtE,
	'>': ast.Gt,
	'>=': ast.GtE
}

precedence = (
	('left', 'OR'),
	('left', 'AND'),
	('left', 'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
	('left', '+', '-'),
	('left', '*', '/', '%')
)

def call_runtime(name, *args):
	return ast.Call(
		func=ast.Attribute(
			value=ast.Name("rt", ast.Load),
            attr=name
        ),
        args=args,
        keywords=[],
        kwargs=[],
        starargs=[])

def p_expression_infix(p):
	r'''
		expression : expression '+' expression
		           | expression '-' expression
		           | expression '*' expression
		           | expression '/' expression
		           | expression '%' expression
		           | expression ASSIGN expression
		           | expression EQ expression
		           | expression NE expression
		           | expression LT expression
		           | expression LE expression
		           | expression GT expression
		           | expression GE expression
	'''
	opname = p[2]
	right = p[3]

	if (p[2] in ('+', '-', '*', '/', '%')):
		op = alu_infix_operator_map[opname]
		p[0] = ast.BinOp(left=p[1], op=op, right=p[3])
	else:
		op = cmp_infix_operator_map[opname]
		p[0] = ast.Compare(left=p[1], ops=[op], comparators=[right])

def p_expression_and(p):
	r"expression : expression AND expression"
	p[0] = ast.BoolOp(op=ast.And, values=[p[1], p[3]])

def p_expression_or(p):
	r"expression : expression OR expression"
	p[0] = ast.BoolOp(op=ast.Or, values=[p[1], p[3]])

def p_expression_leaf(p):
	r"expression : leaf"
	p[0] = p[1]

def p_leaf_parenthesis(p):
	r"leaf : '(' expression ')'"
	p[0] = p[2]

def p_leaf_number(p):
	r"leaf : NUMBER"
	p[0] = ast.Num(p[1])

def p_leaf_id(p):
	r"leaf : ID"
	p[0] = ast.Name("var_"+p[1], ast.Load)

def p_leaf_global(p):
	r"leaf : '$' ID"
	p[0] = call_runtime("GetGlobal", ast.Str(p[2]))

def p_leaf_true(p):
	r"leaf : TRUE"
	p[0] = ast.Name("True", ast.Load)

def p_leaf_false(p):
	r"leaf : FALSE"
	p[0] = ast.Name("False", ast.Load)

def p_leaf_not(p):
	r"leaf : NOT leaf"
	p[0] = ast.UnaryOp(op=ast.Not, operand=p[2])

# Statements

def p_statement_assign_var(p):
	r"statement : ID ASSIGN expression"
	p[0] = ast.Assign([ast.Name("var_"+p[1], ast.Store)], p[3])

def p_statement_assign_global(p):
	r"statement : '$' ID ASSIGN expression"
	p[0] = ast.Expr(call_runtime("SetGlobal", ast.Str(p[2]), p[4]))

def p_statement_singleline_if(p):
	r"statement : IF expression THEN singlelinestatements"
	p[0] = ast.If(test=p[2], body=p[4], orelse=[])

def p_statement_singleline_if_else(p):
	r"statement : IF expression THEN singlelinestatements ELSE singlelinestatements"
	p[0] = ast.If(test=p[2], body=p[4], orelse=p[6])

def p_statement_multiline_if_else(p):
	r"statement : IF expression THEN NL statements else"
	p[0] = [ast.If(test=p[2], body=p[5], orelse=p[6])]

def p_else_empty(p):
	r"else : ENDIF"
	p[0] = []

def p_else_else(p):
	r"else : ELSE statements ENDIF"
	p[0] = p[2]

def p_else_elseif(p):
	r"else : ELSEIF expression THEN NL statements else"
	p[0] = [ast.If(test=p[2], body=p[5], orelse=p[6])]

def p_statement_empty(p):
	r"statement :"
	p[0] = []

def p_singlelinestatements_single(p):
	r"singlelinestatements : statement"
	p[0] = [p[1]]

def p_singlelinestatements_multiple(p):
	r"singlelinestatements : statement ':' singlelinestatements"
	p[0] = [p[1]] + p[3]

def p_statements_single(p):
	r"statements : singlelinestatements"
	p[0] = p[1]

def p_statements_multiple(p):
	r"statements : singlelinestatements NL statements"
	p[0] = p[1] + p[3]

def p_error(p):
    logging.error("Syntax error %s" % p)

parser = yacc.yacc(start='statements')

if __name__=="__main__":
	script = '''
		if not x then x = y: y=0: if z then
			x=y: y=0
		endif: z=0
	'''
	node = parser.parse(script)
	from unparse import Unparser
	print ast.dump(ast.Suite(body=node))
	Unparser(ast.If(test=ast.Name('True', ast.Load), body=node, orelse=[]))

