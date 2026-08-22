/**
 * 时间线数据 Composable
 */
import { ref, onMounted } from 'vue'
import type { TimelineItem } from '../types/content'
import { getTimeline } from '../api/timeline'

/** 获取时间线列表 */
export function useTimeline() {
  const timeline = ref<TimelineItem[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)

  onMounted(async () => {
    try {
      timeline.value = await getTimeline()
    } catch (e: any) {
      error.value = e.message || 'Failed to load timeline'
    } finally {
      loading.value = false
    }
  })

  return { timeline, loading, error }
}
