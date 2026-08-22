/**
 * 个人资料数据 Composable
 */
import { ref, onMounted } from 'vue'
import type { Profile } from '../types/content'
import { getProfile } from '../api/profile'

/** 获取个人资料（单对象，初始为 null） */
export function useProfile() {
  const profile = ref<Profile | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      profile.value = await getProfile()
    } catch (e: any) {
      error.value = e.message || 'Failed to load profile'
    } finally {
      loading.value = false
    }
  })

  return { profile, loading, error }
}
