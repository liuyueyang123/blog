/**
 * Markdown 渲染工具：markdown-it + highlight.js
 * 渲染正文 HTML，并提取 h2~h4 标题用于生成目录（TOC）。
 */
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js/lib/common';
import 'highlight.js/styles/github-dark.css';

export interface TocHeading {
  level: number;
  text: string;
  id: string;
}

export interface RenderedMarkdown {
  html: string;
  headings: TocHeading[];
}

const md = new MarkdownIt({
  html: false, // 不渲染原始 HTML，防 XSS
  linkify: true,
  breaks: false,
});

// 统一代码块渲染：加 hljs class + 按语言高亮
function renderCodeBlock(code: string, lang: string): string {
  let highlighted = md.utils.escapeHtml(code);
  if (lang && hljs.getLanguage(lang)) {
    try {
      highlighted = hljs.highlight(code, { language: lang, ignoreIllegals: true }).value;
    } catch {
      // 高亮失败则保留转义后的纯文本
    }
  }
  const langClass = lang ? ` language-${md.utils.escapeHtml(lang)}` : '';
  return `<pre><code class="hljs${langClass}">${highlighted}</code></pre>`;
}

md.renderer.rules.fence = (tokens, idx) => {
  const token = tokens[idx];
  const lang = token.info ? token.info.trim().split(/\s+/)[0] : '';
  return `${renderCodeBlock(token.content, lang)}\n`;
};

md.renderer.rules.code_block = (tokens, idx) => {
  return `${renderCodeBlock(tokens[idx].content, '')}\n`;
};

export function renderMarkdown(content: string): RenderedMarkdown {
  const headings: TocHeading[] = [];
  const tokens = md.parse(content, {});

  // 给 h2~h4 按顺序生成稳定 id，并收集标题用于 TOC
  let counter = 0;
  for (let i = 0; i < tokens.length; i += 1) {
    const token = tokens[i];
    if (token.type !== 'heading_open') continue;
    const level = Number(token.tag.slice(1));
    if (level < 2 || level > 4) continue;

    counter += 1;
    const id = `heading-${counter}`;
    token.attrSet('id', id);

    const inline = tokens[i + 1];
    const text = inline && inline.type === 'inline' ? (inline.content || '').trim() : '';
    headings.push({ level, text, id });
  }

  const html = md.renderer.render(tokens, md.options, {});
  return { html, headings };
}
