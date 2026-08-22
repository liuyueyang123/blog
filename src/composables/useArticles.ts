/**
 * 文章数据 Composable
 * 封装加载状态和错误处理，视图只需调用即可
 */
import { ref, onMounted } from 'vue'
import type { Article } from '../types/content'
import { getArticles, getArticleBySlug } from '../api/articles'

/** 获取文章列表 */
export function useArticles() {
  const articles = ref<Article[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      articles.value = await getArticles()
    } catch (e: any) {
      error.value = e.message || 'Failed to load articles'
    } finally {
      loading.value = false
    }
  })

  return { articles, loading, error }
}

/** 根据 slug 获取单篇文章 */
export function useArticle(slug: string) {
  const article = ref<Article | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      article.value = await getArticleBySlug(slug)
    } catch (e: any) {
      error.value = e.message || 'Failed to load article'
    } finally {
      loading.value = false
    }
  })

  return { article, loading, error }
}
