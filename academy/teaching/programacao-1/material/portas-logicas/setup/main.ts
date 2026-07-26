// Wheel navigation — one mechanical tick = one slide
export default ({ router }: { router: { forward(): void; back(): void } }) => {
  let accum = 0
  let timer: ReturnType<typeof setTimeout> | undefined
  window.addEventListener('wheel', (e: WheelEvent) => {
    const dy = e.deltaMode === 0 ? e.deltaY : e.deltaY * 100
    accum += dy
    clearTimeout(timer)
    timer = setTimeout(() => { accum = 0 }, 400)
    if (accum >= 100)       { accum = 0; router.forward() }
    else if (accum <= -100) { accum = 0; router.back() }
  }, { passive: true })
}
