var juice = require('juice');
const fs = require("fs");

const args = process.argv.slice(2);
var string = fs.readFileSync(args[0], 'utf8')


options = {webResources : {
	images : true
}}
juice.juiceResources(string, options, function(err, html) {
	fs.writeFile(args[0].replace('.html', '_inline.html'), html, (err) => {
	    if (err) return console.error(err);
	    console.log("File successfully written !");
	});
});
