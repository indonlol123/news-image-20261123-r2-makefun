// Entry point for "The World in a Day" — 23 November 2026 news image.
// It places the pre-rendered front page (entry.png, drawn by render.py)
// at $MAKEFUN_OUTPUT_DIR/entry.png. Node 22 standard library only, no
// network, no randomness: every run writes the exact same bytes.
import { existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1048576;

const root = dirname(fileURLToPath(import.meta.url));
const source = join(root, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

if (!existsSync(source)) {
  throw new Error(`missing entry image next to main.ts: ${source}`);
}
const bytes = readFileSync(source);
if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (statSync(source).size !== bytes.length) {
  throw new Error("entry.png changed while being read");
}

mkdirSync(targetDir, { recursive: true });
writeFileSync(join(targetDir, "entry.png"), bytes);
console.log(`wrote entry.png (${bytes.length} bytes) to ${targetDir}`);
