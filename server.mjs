import { createServer } from "node:http";
import { createReadStream, existsSync } from "node:fs";
import { stat } from "node:fs/promises";
import path from "node:path";

const root = path.resolve("public");
const port = Number(process.env.PORT || 3000);

const mimeTypes = new Map([
  [".avif", "image/avif"],
  [".css", "text/css; charset=utf-8"],
  [".gif", "image/gif"],
  [".html", "text/html; charset=utf-8"],
  [".ico", "image/x-icon"],
  [".jpg", "image/jpeg"],
  [".jpeg", "image/jpeg"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".png", "image/png"],
  [".svg", "image/svg+xml"],
  [".webp", "image/webp"],
  [".woff", "font/woff"],
  [".woff2", "font/woff2"],
]);

function resolveRequestPath(requestUrl) {
  const url = new URL(requestUrl, `http://localhost:${port}`);
  const decoded = decodeURIComponent(url.pathname);
  const normalized = path.normalize(decoded).replace(/^(\.\.[/\\])+/, "");
  let filePath = path.join(root, normalized);

  if (!filePath.startsWith(root)) {
    return null;
  }

  if (existsSync(filePath) && !path.extname(filePath)) {
    filePath = path.join(filePath, "index.html");
  }

  if (!existsSync(filePath) && !path.extname(filePath)) {
    filePath = path.join(root, normalized, "index.html");
  }

  if (!existsSync(filePath)) {
    filePath = path.join(root, "index.html");
  }

  return filePath;
}

const server = createServer(async (request, response) => {
  try {
    const filePath = resolveRequestPath(request.url || "/");
    if (!filePath) {
      response.writeHead(403);
      response.end("Forbidden");
      return;
    }

    const fileStat = await stat(filePath);
    if (!fileStat.isFile()) {
      response.writeHead(404);
      response.end("Not found");
      return;
    }

    const contentType = mimeTypes.get(path.extname(filePath).toLowerCase()) || "application/octet-stream";
    response.writeHead(200, { "content-type": contentType });
    createReadStream(filePath).pipe(response);
  } catch {
    response.writeHead(404);
    response.end("Not found");
  }
});

server.listen(port, () => {
  console.log(`Crays local mirror running at http://localhost:${port}`);
});
