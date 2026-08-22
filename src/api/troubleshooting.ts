/**
 * 故障排查 API
 */
import apiClient from './client'
import type { TroubleshootingCase } from '../types/content'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
  total?: number
}

/** 获取所有已发布故障排查案例 */
export async function getTroubleshootingCases(): Promise<TroubleshootingCase[]> {
  const { data } = await apiClient.get<ApiResponse<TroubleshootingCase[]>>('/troubleshooting')
  return data.data
}
