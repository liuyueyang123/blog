import { onMounted, onUnmounted, nextTick, watch, isRef, type Ref } from 'vue';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

/**
 * 滚动入场动画 composable。
 *
 * 数据改为 API 异步加载后，v-for 卡片在 onMounted 时可能尚未渲染，
 * 因此支持传入一个 loading ref：数据加载完成（loading 变 false）后
 * 自动补扫新出现的 [data-reveal] / [data-stagger] 元素。
 * 已动画化的元素用 WeakSet 记录，不会重复动画。
 *
 * 动画参数与原版完全一致，视觉效果不变。
 */
export function useRevealAnimations(loading?: Ref<boolean>) {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ctx: gsap.Context | undefined;
  const animated = new WeakSet<Element>();

  function setupReveals() {
    gsap.utils.toArray<HTMLElement>('[data-reveal]').forEach((el) => {
      if (animated.has(el)) return;
      animated.add(el);
      gsap.from(el, {
        y: 28,
        opacity: 0,
        duration: 0.62,
        ease: 'power2.out',
        scrollTrigger: {
          trigger: el,
          start: 'top 84%',
        },
      });
    });

    gsap.utils.toArray<HTMLElement>('[data-stagger]').forEach((group) => {
      if (animated.has(group)) return;
      animated.add(group);
      gsap.from(group.children, {
        y: 22,
        opacity: 0,
        duration: 0.5,
        ease: 'power2.out',
        stagger: 0.08,
        scrollTrigger: {
          trigger: group,
          start: 'top 82%',
        },
      });
    });
  }

  onMounted(() => {
    if (reduceMotion) {
      return;
    }

    ctx = gsap.context(() => {
      gsap.from('[data-hero-reveal]', {
        y: 24,
        opacity: 0,
        duration: 0.75,
        ease: 'power3.out',
        stagger: 0.12,
      });

      setupReveals();
    });

    // 异步数据渲染完成后补扫新元素
    if (isRef(loading)) {
      const rescan = () => nextTick(() => ctx?.add(() => setupReveals()));
      if (!loading.value) {
        rescan();
      } else {
        watch(loading, (val) => {
          if (!val) rescan();
        });
      }
    }
  });

  onUnmounted(() => ctx?.revert());
}
