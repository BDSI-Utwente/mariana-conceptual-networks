import * as textract from "textract";
import minimist from "minimist";
import glob from "glob";
import path from "path";
import fs from "fs";

const args = minimist(process.argv.slice(2), {
    alias: { outdir: "o", linebreaks: "l" },
    default: { linebreaks: true },
});
if (!args.outdir) {
    console.error(
        "output dir must be set; e.g. `extract -o data/text data/raw/*"
    );
}

for (const pattern of args._) {
    glob(pattern, (err, files) => {
        if (err) {
            console.error({ pattern, err });
            // continue;
        }

        for (const file of files) {
            const pdf = path.extname(file).toLowerCase() === ".pdf";
            textract.fromFileWithPath(
                file,
                {
                    preserveOnlyMultipleLineBreaks: pdf && args.linebreaks,
                    preserveLineBreaks: !pdf && args.linebreaks,
                },
                (err, text) => {
                    if (err) {
                        console.error({ pattern, file, err });
                        // continue;
                    }

                    let outfile = path.join(
                        args.outdir,
                        path.basename(file, path.extname(file)) + ".txt"
                    );
                    console.log(`${file} => ${outfile}`);
                    fs.writeFileSync(outfile, text, "utf8");
                }
            );
        }
    });
}
