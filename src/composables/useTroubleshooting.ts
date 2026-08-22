/**
 * 故障排查数据 Composable
 */
import { ref, onMounted } from 'vue'
import type { TroubleshootingCase } from '../types/content'
import { getTroubleshootingCases } from '../api/troubleshooting'

/** 获取故障排查案例列表 */
export function useTroubleshooting() {
  const troubleshootingCases = ref<TroubleshootingCase[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      troubleshootingCases.value = await getTroubleshootingCases()
    } catch (e: any) {
      error.value = e.message || 'Failed to load troubleshooting cases'
    } finally {
      loading.value = false
    }
  })

  return { troubleshootingCases, loading, error }
}
