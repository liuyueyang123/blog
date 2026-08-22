/**
 * 项目管理 API（admin 端）
 */
import apiClient from './client';

export interface Project {
  id?: number;
  slug: string;
  title: string;
  subtitle: string;
  coverTone: string;
  tags: string[];
  role: string;
  result: string;
  overview: string;
  highlights: string[];
  githubUrl: string;
  isPublished?: boolean;
  sortOrder?: number;
}

export interface ProjectPayload {
  slug: string;
  title: string;
  subtitle: string;
  cover_tone: string;
  tags: string[];
  role: string;
  result: string;
  overview: string;
  highlights: string[];
  github_url: string;
  is_published: boolean;
  sort_order: number;
}

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  total?: number;
}

export async function getAdminProjects(): Promise<Project[]> {
  const { data } = await apiClient.get<ApiResponse<Project[]>>('/admin/projects');
  return data.data;
}

export async function createProject(project: ProjectPayload): Promise<Project> {
  const { data } = await apiClient.post<ApiResponse<Project>>('/admin/projects', project);
  return data.data;
}

export async function updateProject(id: number, project: Partial<ProjectPayload>): Promise<Project> {
  const { data } = await apiClient.put<ApiResponse<Project>>(`/admin/projects/${id}`, project);
  return data.data;
}

export async function deleteProject(id: number): Promise<void> {
  await apiClient.delete(`/admin/projects/${id}`);
}
