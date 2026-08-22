/**
 * 项目数据 Composable
 */
import { ref, onMounted } from 'vue'
import type { Project } from '../types/content'
import { getProjects, getProjectBySlug } from '../api/projects'

/** 获取项目列表 */
export function useProjects() {
  const projects = ref<Project[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      projects.value = await getProjects()
    } catch (e: any) {
      error.value = e.message || 'Failed to load projects'
    } finally {
      loading.value = false
    }
  })

  return { projects, loading, error }
}

/** 根据 slug 获取单个项目 */
export function useProject(slug: string) {
  const project = ref<Project | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      project.value = await getProjectBySlug(slug)
    } catch (e: any) {
      error.value = e.message || 'Failed to load project'
    } finally {
      loading.value = false
    }
  })

  return { project, loading, error }
}
