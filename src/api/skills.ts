/**
 * 技能 API
 */
import apiClient from './client'
import type { SkillGroup } from '../types/content'

interface ApiResponse<T> {
  code: number
  message: string
  data: T
  total?: number
}

/** 获取所有技能组（含技能项，嵌套结构） */
export async function getSkillGroups(): Promise<SkillGroup[]> {
  const { data } = await apiClient.get<ApiResponse<SkillGroup[]>>('/skills')
  return data.data
}
