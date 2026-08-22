/**
 * 时间线 API
 */
import apiClient from './client'
import type { TimelineItem } from '../types/content'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
  total?: number
}

/** 获取时间线列表 */
export async function getTimeline(): Promise<TimelineItem[]> {
  const { data } = await apiClient.get<ApiResponse<TimelineItem[]>>('/timeline')
  return data.data
}
