const fs = require('fs');
const MWBot = require('mwbot');

const config = JSON.parse(fs.readFileSync("config.json", "utf8"));
const langdata = JSON.parse(fs.readFileSync("language-data.json", "utf8"));

languages = Object.keys(langdata);

async function main() {
	let args = process.argv.slice(2);
	if (!args.length) {
		console.log("Updating all languages...");
		args = languages;
	}

	const bot = new MWBot({ apiUrl: config.api });
	await bot.loginGetEditToken({
		username: config.username,
		password: config.password
	});

	for (let lang of args) {
		console.log("Updating " + lang);

		fs.readFile("output/missing-"+lang+".txt", "utf8", function (err, data) {
			if (err)
				return console.log(err);

			return bot.edit("Wikidata:Lexicographical coverage/"+lang+"/Missing", data, "update list");
		});
		await new Promise(r => setTimeout(r, 5000));

		fs.readFile("output/stats-"+lang+".txt", "utf8", function (err, data) {
			if (err)
				return console.log(err);

			return bot.edit("Wikidata:Lexicographical coverage/"+lang+"/Statistics", data, "update statistics");
		});
		await new Promise(r => setTimeout(r, 5000));

	}
}

main().catch(console.error);
