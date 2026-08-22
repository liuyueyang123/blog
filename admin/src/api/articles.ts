/**
 * 文章管理 API（admin 端）
 */
import apiClient from './client';

export interface Article {
  id?: number;
  slug: string;
  title: string;
  category: string;
  excerpt: string;
  date: string;
  readTime: string;
  content: string[];
  isPublished?: boolean;
  sortOrder?: number;
}

export interface ArticlePayload {
  slug: string;
  title: string;
  category: string;
  excerpt: string;
  date: string;
  read_time: string;
  content: string[];
  is_published: boolean;
  sort_order: number;
}

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  total?: number;
}

export async function login(username: string, password: string): Promise<string> {
  const { data } = await apiClient.post<ApiResponse<{ access_token: string }>>('/auth/login', {
    username,
    password,
  });
  return data.data.access_token;
}

export async function getAdminArticles(): Promise<Article[]> {
  const { data } = await apiClient.get<ApiResponse<Article[]>>('/admin/articles');
  return data.data;
}

export async function createArticle(article: ArticlePayload): Promise<Article> {
  const { data } = await apiClient.post<ApiResponse<Article>>('/admin/articles', article);
  return data.data;
}

export async function updateArticle(id: number, article: Partial<ArticlePayload>): Promise<Article> {
  const { data } = await apiClient.put<ApiResponse<Article>>(`/admin/articles/${id}`, article);
  return data.data;
}

export async function deleteArticle(id: number): Promise<void> {
  await apiClient.delete(`/admin/articles/${id}`);
}
