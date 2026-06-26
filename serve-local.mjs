import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { extname, resolve, sep } from "node:path";

const root = resolve(process.cwd());
const port = Number(process.argv[2] || 8787);
const mimeTypes = {
    ".css": "text/css; charset=utf-8",
    ".html": "text/html; charset=utf-8",
    ".ico": "image/x-icon",
    ".jpg": "image/jpeg",
    ".js": "text/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".svg": "image/svg+xml"
};

const server = createServer(async (request, response) => {
    try {
        const requestUrl = new URL(request.url || "/", "http://localhost");
        const pathname = requestUrl.pathname === "/" ? "/index.html" : requestUrl.pathname;
        const relativePath = decodeURIComponent(pathname).replace(/^[/\\]+/, "");
        const filePath = resolve(root, relativePath);
        if (filePath !== root && !filePath.startsWith(`${root}${sep}`)) {
            response.writeHead(403).end("Forbidden");
            return;
        }
        const fileInfo = await stat(filePath);
        if (!fileInfo.isFile()) {
            response.writeHead(404).end("Not found");
            return;
        }
        const content = await readFile(filePath);
        response.writeHead(200, {
            "Cache-Control": "no-store",
            "Content-Type": mimeTypes[extname(filePath).toLowerCase()] || "application/octet-stream"
        });
        response.end(content);
    } catch {
        response.writeHead(404).end("Not found");
    }
});

server.listen(port, "127.0.0.1", () => {
    console.log(`Cinematic Prompt Builder is running at http://localhost:${port}`);
});
