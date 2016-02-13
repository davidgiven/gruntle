import * as parser from "thickbasic-parser";

export function compile(text) {
	return parser.parse(text);
}

