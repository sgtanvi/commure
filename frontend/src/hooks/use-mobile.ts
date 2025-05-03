// frontend/src/hooks/use-mobile.ts
import { useState, useEffect } from "react"

/**
 * Returns `true` if the viewport width is <= `maxWidth` (in px).
 * You can adjust the breakpoint to whatever your design uses.
 */
export function useIsMobile(maxWidth = 768): boolean {
    const [isMobile, setIsMobile] = useState<boolean>(() => {
        if (typeof window === "undefined") return false
        return window.matchMedia(`(max-width: ${maxWidth}px)`).matches
    })

    useEffect(() => {
        if (typeof window === "undefined") return

        const mql = window.matchMedia(`(max-width: ${maxWidth}px)`)
        const handler = (e: MediaQueryListEvent) => setIsMobile(e.matches)

        // Listen for changes
        mql.addEventListener("change", handler)
        // Cleanup
        return () => mql.removeEventListener("change", handler)
    }, [maxWidth])

    return isMobile
}