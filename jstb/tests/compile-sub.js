import * as thickbasic from "thickbasic";
import {deindent} from "test-helpers";

describe(__filename, () => {
	it("parses empty subroutines correctly", () => {
		let ast = thickbasic.compile(
			deindent(`
				sub test()
				endsub
			`))

		expect(ast).toEqual(
			{
				location: { offset: 1, line: 2, column: 1 },
				type: "sub",
				id: "test",
				body: {
					type: "seq",
					value: []
				}
			}
		);
	});
});

