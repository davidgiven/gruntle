import {deindent, delocate} from "./testsuite";
import * as thickbasic from "thickbasic";

describe(__filename, () => {
	it("parses empty subroutines correctly", () => {
		let ast = thickbasic.compile(
			deindent(`
				sub test()
				endsub
			`));

		expect(ast).toEqual(
			{
				location: { offset: 1, line: 2, column: 1 },
				type: "sub",
				id: "test",
				body: {
					type: "seq",
					value: []
				},
				parameters: [],
			}
		);
	});

	it("parses subroutines with parameters correctly", () => {
		let ast = thickbasic.compile(
			deindent(`
				sub test(a, b, c)
				endsub
			`));

		expect(delocate(ast)).toEqual(
			{
				type: "sub",
				id: "test",
				body: {
					type: "seq",
					value: []
				},
				parameters: [
					{ type: "id", value: "a" },
					{ type: "id", value: "b" },
					{ type: "id", value: "c" }
				]
			}
		);
	});
});

