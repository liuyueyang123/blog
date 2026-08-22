/**
 * 个人资料 API
 */
import apiClient from './client'
import type { Profile } from '../types/content'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
  total?: number
}

/** 获取个人资料（含社交链接与能力卡片） */
export async function getProfile(): Promise<Profile> {
  const { data } = await apiClient.get<ApiResponse<Profile>>('/profile')
  return data.data
}
