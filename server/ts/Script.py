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
	'if': 'IF',
	'then': 'THEN',
	'else': 'ELSE',
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
]

literals = [
	"(", ")", ":", "+", "-", "*", "/", "%", "$", ".", "="
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

def t_error(t):
	logging.error("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()

# --- Parser/compiler -------------------------------------------------------

infix_operator_map = {
	'+': ast.Add,
	'-': ast.Sub,
	'*': ast.Mult,
	'/': ast.Div,
	'%': ast.Mod
}

precedence = (
	('left', '+', '-'),
	('left', '*', '/', '%')
)

def p_expression_infix(p):
	r'''
		expression : leaf '+' expression
		           | leaf '-' expression
		           | leaf '*' expression
		           | leaf '/' expression
		           | leaf '%' expression
	'''
	op = infix_operator_map[p[2]]
	p[0] = ast.BinOp(left=p[1], op=op, right=p[3])

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

# Substatements

def p_substatement_assign_var(p):
	r"substatement : ID '=' expression"
	p[0] = ast.Assign([ast.Name("var_"+p[1], ast.Store)], p[3])

def p_substatement_if(p):
	r"substatement : IF expression THEN substatements"
	p[0] = ast.If(test=p[2], body=p[4], orelse=[ast.Pass()])

def p_substatement_if_else(p):
	r"substatement : IF expression THEN substatements ELSE substatements"
	p[0] = ast.If(test=p[2], body=p[4], orelse=p[6])

def p_substatements_single(p):
	r"substatements : substatement"
	p[0] = [p[1]]

def p_substatements_multiple(p):
	r"substatements : substatement ':' substatements"
	p[0] = [p[1]] + p[3]

# Statements

def p_statement_empty(p):
	r"statement :"
	p[0] = ast.Pass()

def p_statement_substatements(p):
	r"statement : substatements"
	p[0] = p[1]

def p_statements_single(p):
	r"statements : statement"
	p[0] = [p[1]]

def p_statements_multiple(p):
	r"statements : statement NL statements"
	p[0] = [p[1]] + p[3]

def p_error(p):
    logging.error("Syntax error %s" % p)

parser = yacc.yacc(start='statements', debug=True, debuglog=logging)

if __name__=="__main__":
	script = '''
		x = 1
		x=x+1
	'''
	node = parser.parse(script)
	from unparse import Unparser
	print ast.dump(ast.Suite(body=node))
	Unparser(ast.If(test=ast.Name('True', ast.Load), body=node, orelse=[ast.Pass()]))

