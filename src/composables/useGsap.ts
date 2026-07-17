import { onMounted, onUnmounted } from 'vue';
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

export function useRevealAnimations() {
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let ctx: gsap.Context | undefined;

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

      gsap.utils.toArray<HTMLElement>('[data-reveal]').forEach((el) => {
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
    });
  });

  onUnmounted(() => ctx?.revert());
}
