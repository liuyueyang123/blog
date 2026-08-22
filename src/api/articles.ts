/**
 * 文章 API
 */
import apiClient from './client'
import type { Article } from '../types/content'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
  total?: number
}

/** 获取所有已发布文章 */
export async function getArticles(): Promise<Article[]> {
  const { data } = await apiClient.get<ApiResponse<Article[]>>('/articles')
  return data.data
}

/** 根据 slug 获取文章详情 */
export async function getArticleBySlug(slug: string): Promise<Article> {
  const { data } = await apiClient.get<ApiResponse<Article>>(`/articles/${slug}`)
  return data.data
}
