/**
 * 图片上传 API（admin 端）
 */
import apiClient from './client';

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

export async function uploadImage(file: File): Promise<string> {
  const form = new FormData();
  form.append('file', file);
  const { data } = await apiClient.post<ApiResponse<{ url: string }>>('/admin/upload', form);
  return data.data.url;
}
