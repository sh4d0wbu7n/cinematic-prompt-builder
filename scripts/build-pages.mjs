import { cp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { resolve, sep } from "node:path";

const root = resolve(process.cwd());
const dist = resolve(root, "dist");

if (!dist.startsWith(`${root}${sep}`)) {
    throw new Error("Refusing to write the Pages build outside the project.");
}

function stripOllamaSections(source) {
    return source
        .replace(/<!--[ \t]*OLLAMA-START[ \t]*-->[\s\S]*?<!--[ \t]*OLLAMA-END[ \t]*-->\s*/g, "")
        .replace(/\/\*[ \t]*OLLAMA-START[ \t]*\*\/[\s\S]*?\/\*[ \t]*OLLAMA-END[ \t]*\*\/\s*/g, "")
        .replace(/^[ \t]*\/\/ OLLAMA-START[\s\S]*?^[ \t]*\/\/ OLLAMA-END\s*\r?\n?/gm, "");
}

const source = await readFile(resolve(root, "index.html"), "utf8");
const page = stripOllamaSections(source)
    .replace("v4.2 (Still Image + Ollama)", "v4.2 (GitHub Pages)");

if (/Ollama|ollama/.test(page)) {
    throw new Error("The GitHub Pages build still contains Ollama code or UI.");
}

await rm(dist, { recursive: true, force: true });
await mkdir(dist, { recursive: true });
await Promise.all([
    cp(resolve(root, "assets"), resolve(dist, "assets"), { recursive: true }),
    cp(resolve(root, "favicon.png"), resolve(dist, "favicon.png")),
    writeFile(resolve(dist, "index.html"), page),
    writeFile(resolve(dist, ".nojekyll"), "")
]);

console.log("GitHub Pages build created in dist/ without Ollama enhancement.");
