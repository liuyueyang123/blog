/**
 * 时间线管理 API（admin 端）
 */
import apiClient from './client';

export interface TimelineItem {
  id?: number;
  time: string;
  title: string;
  detail: string;
  sortOrder?: number;
}

export interface TimelinePayload {
  time: string;
  title: string;
  detail: string;
  sort_order: number;
}

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  total?: number;
}

export async function getAdminTimeline(): Promise<TimelineItem[]> {
  const { data } = await apiClient.get<ApiResponse<TimelineItem[]>>('/admin/timeline');
  return data.data;
}

export async function createTimelineItem(payload: TimelinePayload): Promise<TimelineItem> {
  const { data } = await apiClient.post<ApiResponse<TimelineItem>>('/admin/timeline', payload);
  return data.data;
}

export async function updateTimelineItem(id: number, payload: Partial<TimelinePayload>): Promise<TimelineItem> {
  const { data } = await apiClient.put<ApiResponse<TimelineItem>>(`/admin/timeline/${id}`, payload);
  return data.data;
}

export async function deleteTimelineItem(id: number): Promise<void> {
  await apiClient.delete(`/admin/timeline/${id}`);
}
