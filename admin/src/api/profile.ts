/**
 * 个人资料管理 API（admin 端）
 */
import apiClient from './client';

export interface CapabilityCard {
  title: string;
  tech: string;
  practice: string;
}

export interface SocialLinks {
  githubUrl: string;
  email: string;
  bilibiliUrl: string;
  douyinUrl: string;
  xiaohongshuUrl: string;
  resumeUrl: string;
}

export interface Profile {
  name: string;
  handle: string;
  title: string;
  focus: string;
  intro: string;
  location: string;
  socialLinks: SocialLinks;
  capabilityCards: CapabilityCard[];
}

export interface ProfilePayload {
  name?: string;
  handle?: string;
  title?: string;
  focus?: string;
  intro?: string;
  location?: string;
  github_url?: string;
  email?: string;
  bilibili_url?: string;
  douyin_url?: string;
  xiaohongshu_url?: string;
  resume_url?: string;
  capability_cards?: CapabilityCard[];
}

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  total?: number;
}

export async function getAdminProfile(): Promise<Profile> {
  const { data } = await apiClient.get<ApiResponse<Profile>>('/admin/profile');
  return data.data;
}

export async function updateProfile(payload: ProfilePayload): Promise<Profile> {
  const { data } = await apiClient.put<ApiResponse<Profile>>('/admin/profile', payload);
  return data.data;
}
