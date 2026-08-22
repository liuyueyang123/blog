/**
 * Markdown 渲染工具（admin 编辑页预览用）
 */
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js/lib/common';
import 'highlight.js/styles/github-dark.css';

const md = new MarkdownIt({
  html: false, // 不渲染原始 HTML，防 XSS
  linkify: true,
  breaks: false,
});

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

export function renderMarkdown(content: string): string {
  return md.render(content);
}
