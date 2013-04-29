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
import time
import re
import __builtin__

# --- Lexer -----------------------------------------------------------------

keywords = {
	'sub': 'SUB',
	'endsub': 'ENDSUB',
	'nil': 'NIL',
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
	'step': 'STEP',
	'to': 'TO',
	'while': 'WHILE',
	'endwhile': 'ENDWHILE',
	'break': 'BREAK',
	'continue': 'CONTINUE',
	'return': 'RETURN'
}

tokens = keywords.values() + [
	"ID",
	"NL",
	"NUMBER",
	"STRING",
	"MARKUPBEGIN",
	"MARKUPEND",
	"EQ",
	"NE",
	"LT",
	"LE",
	"GT",
	"GE",
	"ASSIGN",
	"OPENBRACE",
	"CLOSEBRACE"
]

literals = [
	"(", ")", ":", "+", "-", "*", "/", "%", "$", ".", ",", "[", "]"
]

states = (
	('markuptext', 'exclusive'),
	('markupexpr', 'inclusive')
)

t_ignore = ' \t'

def t_COMMENT(t):
	r';[^\n]*'
	pass

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = keywords.get(t.value, 'ID')
    t.value = t.value.encode("UTF-8")
    return t

def t_NL(t):
	r'\n'
	t.lexer.lineno += 1
	return t

def t_NUMBER(t):
	r'\d+'
	t.value = int(t.value)
	return t

def t_STRING(t):
	r"'(?:(?:[^'\\])|(?:\\.))*'"
	s = "u"+t.value
	s = ast.literal_eval(s)
	t.value = s
	return t

t_EQ = r'=='
t_NE = r'(!=)|(<>)'
t_LE = r'<='
t_GE = r'>='
t_LT = r'<'
t_GT = r'>'
t_ASSIGN = r'='

def t_MARKUPBEGIN(t):
	r'"'
	t.lexer.push_state("markuptext")
	return t

def t_markuptext_STRING(t):
	r'(?:(?:[^"\\{])|(?:\\.))+'
	s = 'u"'+t.value.replace('"', '\\"')+'"'
	s = ast.literal_eval(s)
	t.value = s
	return t

def t_markuptext_MARKUPEND(t):
	r'"'
	t.lexer.pop_state()
	return t

def t_markuptext_OPENBRACE(t):
	r"{"
	t.lexer.bracelevel = 1
	t.lexer.push_state("markupexpr")
	return t

def t_markupexpr_OPENBRACE(t):
	r"{"
	t.lexer.bracelevel += 1
	return t

def t_markupexpr_CLOSEBRACE(t):
	r"}"
	t.lexer.bracelevel -= 1
	if (t.lexer.bracelevel == 0):
		t.lexer.pop_state()
	return t

def t_error(t):
	logging.error("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex(reflags=re.UNICODE)

# --- Parser/compiler -------------------------------------------------------

infix_operator_map = {
	'+': 'Add',
	'-': 'Sub',
	'*': 'Mult',
	'/': 'Div',
	'%': 'Mod',
	'=': 'Eq',
	'==': 'Eq',
	'<>': 'NotEq',
	'!=': 'NotEq',
	'<': 'Lt',
	'<=': 'LtE',
	'>': 'Gt',
	'>=': 'GtE'
}

prefix_operator_map = {
	'-': 'Neg',
	'not': 'Not'
}

precedence = (
	('left', 'OR'),
	('left', 'AND'),
	('left', 'ASSIGN', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'),
	('left', '+', '-'),
	('left', '*', '/', '%'),
	('right', 'UNARY'),
	('left', '(', '['),
	('left', '.'),
)

def call_runtime(name, lineno, col_offset, *args):
	return ast.Call(
		func=ast.Attribute(
			value=ast.Name(
				id="rt",
				ctx=ast.Load(),
				lineno=lineno,
				col_offset=col_offset
			),
            attr=name,
            ctx=ast.Load(),
            lineno=lineno,
            col_offset=col_offset
        ),
        args=list(args),
        keywords=[],
        kwargs=None,
        starargs=None,
        lineno=lineno,
        col_offset=col_offset
    )

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
	op = infix_operator_map[p[2]]
	p[0] = call_runtime(op, p.lineno(2), p.lexpos(2), p[1], p[3])

def p_expression_prefix(p):
	r'''
		expression : '-' expression %prec UNARY
		           | NOT expression %prec UNARY
	'''
	op = prefix_operator_map[p[1]]
	p[0] = call_runtime(op, p.lineno(2), p.lexpos(2), p[2])

def p_expression_and(p):
	r"expression : expression AND expression"
	p[0] = ast.BoolOp(
		op=ast.And(),
		values=[
			call_runtime(
				"CheckBoolean", p.lineno(1), p.lexpos(1), p[1]),
			call_runtime(
				"CheckBoolean", p.lineno(3), p.lexpos(3), p[3])
		],
		lineno=p.lineno(2),
		col_offset=p.lexpos(2)
	)

def p_expression_or(p):
	r"expression : expression OR expression"
	p[0] = ast.BoolOp(
		op=ast.Or(),
		values=[
			call_runtime(
				"CheckBoolean", p.lineno(1), p.lexpos(1), p[1]),
			call_runtime(
				"CheckBoolean", p.lineno(3), p.lexpos(3), p[3])
		],
		lineno=p.lineno(2),
		col_offset=p.lexpos(2)
	)

def p_expression_call(p):
	r"expression : expression callargs"
	p[0] = ast.Call(
		func=p[1],
        args=p[2],
        keywords=[],
        kwargs=None,
        starargs=None,
        lineno=p.lineno(2),
        col_offset=p.lexpos(2)
    )

def p_expression_index(p):
	r"expression : expression '[' expression ']'"
	p[0] = call_runtime(
		"Index", p.lineno(2), p.lexpos(2),
		p[1], p[3]
	)

def p_expression_property(p):
	r"expression : expression '.' ID"
	p[0] = call_runtime(
		"Property", p.lineno(2), p.lexpos(2),
		p[1],
		ast.Str(
			s=unicode(p[3]),
			lineno=p.lineno(3),
			col_offset=p.lineno(3)
		)
	)

def p_callargs(p):
	r"callargs : '(' arglist ')'"
	p[0] = [
		ast.Name(
			id="rt",
			ctx=ast.Load(),
			lineno=p.lineno(1),
			col_offset=p.lexpos(1)
		)
	] + p[2]

def p_arglist_empty(p):
	r"arglist :"
	p[0] = []

def p_arglist_single(p):
	r"arglist : expression"
	p[0] = [p[1]]

def p_arglist_multiple(p):
	r"arglist : expression ',' arglist"
	p[0] = [p[1]] + p[3]

def p_expression_leaf(p):
	r"expression : leaf"
	p[0] = p[1]

def p_leaf_parenthesis(p):
	r"leaf : '(' expression ')'"
	p[0] = p[2]

def p_leaf_number(p):
	r"leaf : NUMBER"
	p[0] = ast.Num(
		n=float(p[1]),
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_string(p):
	r"leaf : STRING"
	p[0] = ast.Str(
		s=p[1],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_id(p):
	r"leaf : ID"
	p[0] = ast.Name(
		id="var_"+p[1],
		ctx=ast.Load(),
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_global(p):
	r"leaf : '$' ID"
	p[0] = call_runtime(
		"GetGlobal",
		p.lineno(2),
		p.lexpos(2),
		ast.Str(
			s=p[2],
			lineno=p.lineno(2),
			col_offset=p.lexpos(2)
		)
	)

def p_leaf_nil(p):
	r"leaf : NIL"
	p[0] = ast.Name(
		id="None",
		ctx=ast.Load(),
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_true(p):
	r"leaf : TRUE"
	p[0] = ast.Name(
		id="True",
		ctx=ast.Load(),
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_false(p):
	r"leaf : FALSE"
	p[0] = ast.Name(
		id="False",
		ctx=ast.Load(),
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_list(p):
	r"leaf : '[' arglist ']'"
	p[0] = ast.Tuple(
		elts=p[2],
		ctx=ast.Load(),
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_leaf_markup(p):
	r"leaf : MARKUPBEGIN markupelements MARKUPEND"
	p[0] = call_runtime("MakeMarkup", p.lineno(1), p.lexpos(1),
		*p[2])

def p_markupelements_empty(p):
	r"markupelements :"
	p[0] = []

def p_markupelements_markupstring(p):
	r"markupelements : STRING markupelements"
	p[0] = [
		ast.Str(
			s=p[1],
			lineno=p.lineno(1),
			col_offset=p.lexpos(1)
		)
	] + p[2]

def p_markupelements_expr(p):
	r"markupelements : OPENBRACE expression CLOSEBRACE markupelements"
	p[0] = [p[2]] + p[4]

# Statements

# We can't allow bare expressions as statements due to ambiguity between =
# as assignment and = as comparison. So we have to add explicit call rules.

def p_statement_expression(p):
	r"statement : leaf callargs"
	p[0] = ast.Expr(
		value=ast.Call(
			func=p[1],
	        args=p[2],
	        keywords=[],
	        kwargs=None,
	        starargs=None,
	        lineno=p.lineno(2),
	        col_offset=p.lexpos(2)
	    ),
        lineno=p.lineno(1),
        col_offset=p.lexpos(1)
    )

def p_statement_assign_var(p):
	r"statement : ID ASSIGN expression"
	p[0] = ast.Assign(
		targets=[
			ast.Name(
				id="var_"+p[1],
				ctx=ast.Store(),
				lineno=p.lineno(1),
				col_offset=p.lexpos(1)
			)
		],
		value=p[3],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_assign_global(p):
	r"statement : '$' ID ASSIGN expression"
	p[0] = ast.Expr(
		value=call_runtime(
			"SetGlobal", p.lineno(3), p.lexpos(3),
			ast.Str(
				s=p[2],
				lineno=p.lineno(2),
				col_offset=p.lexpos(2)
			),
			p[4]
		),
		lineno=p.lineno(3),
		col_offset=p.lexpos(3)
	)

def p_statement_singleline_if(p):
	r"statement : IF expression THEN singlelinestatements"
	p[0] = ast.If(
		test=p[2],
		body=p[4],
		orelse=[],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_singleline_if_else(p):
	r"statement : IF expression THEN singlelinestatements ELSE singlelinestatements"
	p[0] = ast.If(
		test=p[2],
		body=p[4],
		orelse=p[6],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_multiline_if_else(p):
	r"statement : IF expression THEN NL statements else"
	p[0] = ast.If(
		test=p[2],
		body=p[5],
		orelse=p[6],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_else_empty(p):
	r"else : ENDIF"
	p[0] = []

def p_else_else(p):
	r"else : ELSE statements ENDIF"
	p[0] = p[2]

def p_else_elseif(p):
	r"else : ELSEIF expression THEN NL statements else"
	p[0] = [
		ast.If(
			test=p[2],
			body=p[5],
			orelse=p[6],
			lineno=p.lineno(1),
			col_offset=p.lexpos(1)
		)
	]

def p_statement_for_next(p):
	r"statement : FOR ID ASSIGN expression TO expression step statements NEXT"
	p[0] = ast.For(
		target=ast.Name(
			id="var_"+p[2],
			ctx=ast.Store(),
			lineno=p.lineno(2),
			col_offset=p.lexpos(2)
		),
        iter=call_runtime(
            "ForIterator",
            p.lineno(4),
            p.lexpos(4),
            p[4], p[6], p[7]
        ),
        body=p[8],
        orelse=[],
        lineno=p.lineno(1),
        col_offset=p.lexpos(1)
    )

def p_statement_step_empty(p):
	r"step :"
	p[0] = ast.Num(
		n=1.0,
		lineno=p.lineno(0),
		col_offset=p.lexpos(0)
	)

def p_statement_step_value(p):
	r"step : STEP expression"
	p[0] = p[2]

def p_statment_while_endwhile(p):
	r"statement : WHILE expression statements ENDWHILE"
	p[0] = ast.While(
		test=p[2],
		body=p[3],
		orelse=[],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_return(p):
	r"statement : RETURN expression"
	p[0] = ast.Return(
		value=p[2],
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_break(p):
	r"statement : BREAK"
	p[0] = ast.Break(
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_continue(p):
	r"statement : CONTINUE"
	p[0] = ast.Continue(
		lineno=p.lineno(1),
		col_offset=p.lexpos(1)
	)

def p_statement_empty(p):
	r"statement :"
	p[0] = ast.Pass(
			lineno=p.lineno(0),
			col_offset=p.lexpos(0)
			)

def p_singlelinestatements_single(p):
	r"singlelinestatements : statement"
	p[0] = [p[1]]

def p_singlelinestatements_multiple(p):
	r"singlelinestatements : statement ':' singlelinestatements"
	p[0] = [p[1]] + p[3]

def p_statements_single(p):
	r"statements : statement"
	p[0] = [p[1]]

def p_statements_multiple(p):
	r'''
		statements : statement ':' statements
		           | statement NL statements
	'''
	p[0] = [p[1]] + p[3]

# --- Toplevel statements ---------------------------------------------------

def p_toplevel_empty(p):
	r"toplevel :"
	p[0] = ast.Pass(
		lineno=p.lineno(0),
		col_offset=p.lexpos(0)
	)

def p_toplevel_sub(p):
	r"toplevel : SUB ID bracketedparameterlist statements ENDSUB"

	args = ast.arguments(
		args=(
			[
				ast.Name(
					id="rt",
					ctx=ast.Param(),
					lineno=0,
					col_offset=0
				)
			]
			+ p[3]
		),
		defaults=[],
		vararg=None,
		kwarg=None
	)

	p[0] = ast.FunctionDef(
		name="var_"+p[2],
		args=args,
		body=p[4],
		decorator_list=[],
		lineno=p.lineno(2),
		col_offset=p.lexpos(2)
	)

def p_bracketedparameterlist_empty(p):
	r"bracketedparameterlist :"
	p[0] = []

def p_bracketedparameterlist_brackets(p):
	r"bracketedparameterlist : '(' parameterlist ')'"
	p[0] = p[2]

def p_parameterlist_empty(p):
	r'''
		parameterlist :
	'''
	p[0] = []

def p_parameter(p):
	r'''
		parameter : ID
	'''
	p[0] = [
		ast.Name(
			id="var_"+p[1],
			ctx=ast.Param(),
			lineno=p.lineno(1),
			col_offset=p.lexpos(1)
		)
	]

def p_parameterlist_single(p):
	r'''
		parameterlist : parameter
	'''
	p[0] = p[1]

def p_parameterlist_multiple(p):
	r'''
		parameterlist : parameter ',' parameterlist
	'''
	p[0] = p[1] + p[3]

def p_toplevels_single(p):
	r"toplevels : toplevel"
	p[0] = [p[1]]

def p_toplevels_colon(p):
	r"toplevels : toplevel ':' toplevels"
	p[0] = [p[1]] + p[3]

def p_toplevels_newline(p):
	r"toplevels : toplevel NL toplevels"
	p[0] = [p[1]] + p[3]

def p_error(p):
    logging.error("Syntax error %s" % p)

parser = yacc.yacc(start='toplevels')

cache = {}

def compile(script):
	if (script in cache):
		return cache[script]

	starttime = time.time()

	node = parser.parse(script, tracking=True, debug=0)
	from unparse import Unparser

	module = ast.Module(
		body=node,
	    lineno=0,
	    col_offset=0
	)
	#print ast.dump(module, include_attributes=True)
	Unparser(module)
	print

	# Now we've created the AST for the Python module, compile it into a
	# code object...

	co = __builtin__.compile(module, "", "exec")

	# ...then run it to actually define the functions...

	scope = {}
	exec co in scope

	endtime = time.time()
	logging.info("compiled script in %.3fs", endtime - starttime)

	# ...cache and return.

	cache[script] = scope
	return scope


