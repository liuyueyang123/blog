/**
 * 技能数据 Composable
 */
import { ref, onMounted } from 'vue'
import type { SkillGroup } from '../types/content'
import { getSkillGroups } from '../api/skills'

/** 获取技能组列表（含技能项） */
export function useSkills() {
  const skillGroups = ref<SkillGroup[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      skillGroups.value = await getSkillGroups()
    } catch (e: any) {
      error.value = e.message || 'Failed to load skills'
    } finally {
      loading.value = false
    }
  })

  return { skillGroups, loading, error }
}
