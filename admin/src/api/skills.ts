/**
 * 技能管理 API（admin 端）：技能组 + 技能项双层结构
 */
import apiClient from './client';

export interface SkillItem {
  id?: number;
  groupId?: number;
  name: string;
  direction: string;
  scenario: string;
  status: string;
  sortOrder?: number;
}

export interface SkillGroup {
  id?: number;
  title: string;
  summary: string;
  items: SkillItem[];
  sortOrder?: number;
}

export const SKILL_STATUS_OPTIONS = [
  '有项目实践',
  '能够独立完成基础操作',
  '能够排查常见问题',
  '正在系统学习',
];

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  total?: number;
}

// ── 技能组 ──────────────────────────────────────────────

export async function getAdminSkillGroups(): Promise<SkillGroup[]> {
  const { data } = await apiClient.get<ApiResponse<SkillGroup[]>>('/admin/skills');
  return data.data;
}

export async function createSkillGroup(group: { title: string; summary: string; sort_order: number }): Promise<SkillGroup> {
  const { data } = await apiClient.post<ApiResponse<SkillGroup>>('/admin/skill-groups', group);
  return data.data;
}

export async function updateSkillGroup(id: number, group: Partial<{ title: string; summary: string; sort_order: number }>): Promise<SkillGroup> {
  const { data } = await apiClient.put<ApiResponse<SkillGroup>>(`/admin/skill-groups/${id}`, group);
  return data.data;
}

export async function deleteSkillGroup(id: number): Promise<void> {
  await apiClient.delete(`/admin/skill-groups/${id}`);
}

// ── 技能项 ──────────────────────────────────────────────

export async function createSkillItem(
  groupId: number,
  item: { name: string; direction: string; scenario: string; status: string; sort_order: number },
): Promise<SkillItem> {
  const { data } = await apiClient.post<ApiResponse<SkillItem>>(`/admin/skill-groups/${groupId}/items`, item);
  return data.data;
}

export async function updateSkillItem(
  itemId: number,
  item: Partial<{ name: string; direction: string; scenario: string; status: string; sort_order: number }>,
): Promise<SkillItem> {
  const { data } = await apiClient.put<ApiResponse<SkillItem>>(`/admin/skill-items/${itemId}`, item);
  return data.data;
}

export async function deleteSkillItem(itemId: number): Promise<void> {
  await apiClient.delete(`/admin/skill-items/${itemId}`);
}
