import { addPath } from "app-module-path";
addPath(__dirname + "/../src");
addPath(__dirname + "/../gen");

export function deindent(s) {
	let m = s.match(/^[ \t]*(?=\S)/gm);
	if (!m)
		return s;

	let indent = Math.min(...m.map((e) => e.length));
	let re = new RegExp("^[ \\t]{" + indent + "}", "gm");
	return (indent > 0) ? s.replace(re, "") : s;
}

export function delocate(ast) {
	/* Cheap and nasty deep copy. */

	let newast = JSON.parse(JSON.stringify(ast));

	let prune = (o) => {
		if ((o !== null) && (typeof(o) == "object")) {
			delete o.location;
			for (let k in o)
				prune(o[k]);
		}
	};

	prune(newast);
	return newast;
}

