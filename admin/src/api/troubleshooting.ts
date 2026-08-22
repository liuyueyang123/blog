/**
 * 故障排查管理 API（admin 端）
 */
import apiClient from './client';

export interface TroubleshootingCase {
  id?: number;
  slug: string;
  title: string;
  symptom: string;
  process: string;
  tools: string[];
  rootCause: string;
  resolution: string;
  review: string;
  isPublished?: boolean;
  sortOrder?: number;
}

export interface TroubleshootingPayload {
  slug: string;
  title: string;
  symptom: string;
  process: string;
  tools: string[];
  root_cause: string;
  resolution: string;
  review: string;
  is_published: boolean;
  sort_order: number;
}

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  total?: number;
}

export async function getAdminTroubleshooting(): Promise<TroubleshootingCase[]> {
  const { data } = await apiClient.get<ApiResponse<TroubleshootingCase[]>>('/admin/troubleshooting');
  return data.data;
}

export async function createTroubleshooting(payload: TroubleshootingPayload): Promise<TroubleshootingCase> {
  const { data } = await apiClient.post<ApiResponse<TroubleshootingCase>>('/admin/troubleshooting', payload);
  return data.data;
}

export async function updateTroubleshooting(
  id: number,
  payload: Partial<TroubleshootingPayload>,
): Promise<TroubleshootingCase> {
  const { data } = await apiClient.put<ApiResponse<TroubleshootingCase>>(`/admin/troubleshooting/${id}`, payload);
  return data.data;
}

export async function deleteTroubleshooting(id: number): Promise<void> {
  await apiClient.delete(`/admin/troubleshooting/${id}`);
}
