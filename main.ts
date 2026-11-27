// news-image-20261127: copy the rendered front page to the output dir.
//
// Reads news.png beside this file, validates it thoroughly, and writes it
// to $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png), then
// re-reads the landed file and verifies its sha256 matches.
// Never deletes the output directory; only creates it if missing, and
// writes alongside anything already there.
import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const IEND = Buffer.from([
  0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82,
]);
const MAX_BYTES = 1024 * 1024; // 1 MiB
const EXPECTED_WIDTH = 1024;
const EXPECTED_HEIGHT = 1024;

function fail(message: string): never {
  console.error(`news-image-20261127: error: ${message}`);
  process.exit(1);
}

function pngDimensions(buf: Buffer): { width: number; height: number } {
  // PNG layout: 8-byte signature, then IHDR chunk:
  // length (4 BE) + type "IHDR" (4) + width (4 BE) + height (4 BE).
  if (buf.length < 33) {
    fail("news.png is too short to hold an IHDR chunk");
  }
  const ihdrLength = buf.readUInt32BE(8);
  if (ihdrLength !== 13) {
    fail(`news.png IHDR length is ${ihdrLength}, expected 13`);
  }
  if (buf.toString("ascii", 12, 16) !== "IHDR") {
    fail("news.png first chunk is not IHDR");
  }
  return {
    width: buf.readUInt32BE(16),
    height: buf.readUInt32BE(20),
  };
}

const here = dirname(fileURLToPath(import.meta.url));
const srcPath = join(here, "news.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const outPath = join(outDir, "entry.png");

// Cheap pre-check: refuse an oversized file before reading it fully.
const srcStat = await stat(srcPath).catch(() =>
  fail(`cannot stat ${srcPath} (run render.py first)`)
);
if (srcStat.size > MAX_BYTES) {
  fail(`news.png is ${srcStat.size} bytes, over the 1 MiB limit`);
}

const png = await readFile(srcPath);

if (!png.subarray(0, 8).equals(PNG_MAGIC)) {
  fail("news.png does not start with the PNG magic bytes");
}
if (!png.subarray(png.length - 12).equals(IEND)) {
  fail("news.png does not end with a valid IEND chunk");
}
const { width, height } = pngDimensions(png);
if (width !== EXPECTED_WIDTH || height !== EXPECTED_HEIGHT) {
  fail(`news.png is ${width}x${height}, expected 1024x1024`);
}

const sha256 = createHash("sha256").update(png).digest("hex");

await mkdir(outDir, { recursive: true });
await writeFile(outPath, png);

const landed = await readFile(outPath);
if (landed.length !== png.length) {
  fail(`landed file is ${landed.length} bytes, expected ${png.length}`);
}
const landedHash = createHash("sha256").update(landed).digest("hex");
if (landedHash !== sha256) {
  fail(`landed file hash mismatch: ${landedHash} != ${sha256}`);
}

console.log(
  `news-image-20261127: wrote ${outPath} (${png.length} bytes, ` +
    `1024x1024, sha256 ${sha256})`
);
