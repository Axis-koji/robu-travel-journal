import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { extname, join, relative } from "node:path";

const root = process.cwd();
const errors = [];
const warnings = [];

function walk(dir) {
  return readdirSync(dir).flatMap((name) => {
    const fullPath = join(dir, name);
    return statSync(fullPath).isDirectory() ? walk(fullPath) : [fullPath];
  });
}

const textExtensions = new Set([".html", ".md", ".js", ".mjs", ".json", ".yml", ".yaml", ".css"]);
const ignoredDirectories = new Set([".git", "node_modules"]);
const files = walk(root).filter((file) => {
  const parts = relative(root, file).split(/[\\/]/);
  return !parts.some((part) => ignoredDirectories.has(part));
});
const textFiles = files.filter((file) => textExtensions.has(extname(file).toLowerCase()));

const forbiddenPublicLabels = ["公開前下書き"];
const mojibakeSignals = ["繧", "縺", "蜿", "譁", "髫", "蛹", "莠"];

for (const file of textFiles) {
  const relativePath = relative(root, file);
  const content = readFileSync(file, "utf8");

  const isAutomationFile =
    relativePath.startsWith("templates") ||
    relativePath.startsWith(".github") ||
    relativePath.startsWith("scripts") ||
    relativePath === "AUTOMATION.md";

  if (!isAutomationFile) {
    for (const label of forbiddenPublicLabels) {
      if (content.includes(label)) {
        errors.push(`${relativePath}: 公開ページに内部用表示「${label}」が残っています`);
      }
    }
  }

  if (!isAutomationFile) {
    const mojibakeCount = mojibakeSignals.reduce(
      (count, signal) => count + (content.split(signal).length - 1),
      0,
    );
    if (mojibakeCount >= 3) {
      errors.push(`${relativePath}: 文字化けの可能性があります`);
    }
  }
}

const indexPath = join(root, "index.html");
if (!existsSync(indexPath)) {
  errors.push("index.html がありません");
} else {
  const html = readFileSync(indexPath, "utf8");
  const imageReferences = [...html.matchAll(/(?:src|image)\s*[:=]\s*['"]([^'"]+\.(?:png|jpe?g|webp|gif|svg))['"]/gi)]
    .map((match) => match[1])
    .filter((path) => !/^https?:\/\//i.test(path) && !path.startsWith("data:"));

  for (const imagePath of new Set(imageReferences)) {
    const normalizedPath = imagePath.replace(/^\/+/, "");
    if (!existsSync(join(root, normalizedPath))) {
      errors.push(`index.html: 画像ファイルが見つかりません: ${imagePath}`);
    }
  }

  const videoReferences = [...html.matchAll(/(?:src|video)\s*[:=]\s*['"]([^'"]+\.(?:mp4|webm|ogv))['"]/gi)]
    .map((match) => match[1])
    .filter((path) => !/^https?:\/\//i.test(path) && !path.startsWith("data:"));

  for (const videoPath of new Set(videoReferences)) {
    const normalizedPath = videoPath.replace(/^\/+/, "");
    const fullVideoPath = join(root, normalizedPath);
    if (!existsSync(fullVideoPath)) {
      errors.push(`index.html: 動画ファイルが見つかりません: ${videoPath}`);
    } else if (statSync(fullVideoPath).size > 50 * 1024 * 1024) {
      errors.push(`index.html: 動画が50MBを超えています。外部動画サービスの埋め込みを検討してください: ${videoPath}`);
    }
  }

  if (!html.includes('lang="ja"')) warnings.push('index.html: lang="ja" を確認してください');
  if (!/<meta\s+name=["']description["']/i.test(html)) warnings.push("index.html: descriptionがありません");
}

const articleDir = join(root, "articles");
if (!existsSync(articleDir)) {
  errors.push("articles フォルダがありません");
}

for (const warning of warnings) console.warn(`警告: ${warning}`);
if (errors.length) {
  for (const error of errors) console.error(`エラー: ${error}`);
  process.exit(1);
}

console.log("公開前チェックに合格しました。");
