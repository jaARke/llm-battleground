'use client'

import * as React from 'react'
import * as ProgressPrimitive from '@radix-ui/react-progress'
import { cva, type VariantProps } from 'class-variance-authority'

import { cn } from '@/lib/utils'

const progressVariants = cva(
  'relative w-full overflow-hidden rounded-full',
  {
    variants: {
      variant: {
        default: 'bg-primary/20 h-2',
        glass: 'h-3 bg-[var(--glass-border)]',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

const progressIndicatorVariants = cva(
  'h-full w-full flex-1 transition-all',
  {
    variants: {
      variant: {
        default: 'bg-primary',
        'glass-primary': 'bg-gradient-to-r from-[var(--gradient-primary-start)] via-[var(--gradient-primary-via)] to-[var(--gradient-primary-end)]',
        'glass-success': 'bg-gradient-to-r from-[var(--gradient-success-start)] via-[var(--gradient-success-via)] to-[var(--gradient-success-end)]',
        'glass-warning': 'bg-gradient-to-r from-[var(--gradient-warning-start)] via-[var(--gradient-warning-via)] to-[var(--gradient-warning-end)]',
      },
    },
    defaultVariants: {
      variant: 'default',
    },
  }
)

function Progress({
  className,
  value,
  variant,
  indicatorVariant,
  ...props
}: React.ComponentProps<typeof ProgressPrimitive.Root> & 
  VariantProps<typeof progressVariants> & {
    indicatorVariant?: VariantProps<typeof progressIndicatorVariants>['variant']
  }) {
  return (
    <ProgressPrimitive.Root
      data-slot="progress"
      className={cn(progressVariants({ variant }), className)}
      {...props}
    >
      <ProgressPrimitive.Indicator
        data-slot="progress-indicator"
        className={progressIndicatorVariants({ variant: indicatorVariant || (variant === 'glass' ? 'glass-primary' : 'default') })}
        style={{ transform: `translateX(-${100 - (value || 0)}%)` }}
      />
    </ProgressPrimitive.Root>
  )
}

export { Progress, progressVariants, progressIndicatorVariants }
