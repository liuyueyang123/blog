/**
 * 项目 API
 */
import apiClient from './client'
import type { Project } from '../types/content'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
  total?: number
}

/** 获取所有已发布项目 */
export async function getProjects(): Promise<Project[]> {
  const { data } = await apiClient.get<ApiResponse<Project[]>>('/projects')
  return data.data
}

/** 根据 slug 获取项目详情 */
export async function getProjectBySlug(slug: string): Promise<Project> {
  const { data } = await apiClient.get<ApiResponse<Project>>(`/projects/${slug}`)
  return data.data
}
