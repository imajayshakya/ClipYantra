'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive' | 'link';
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'icon';
  loading?: boolean;
  fullWidth?: boolean;
}

const buttonStyles = {
  base: 'inline-flex items-center justify-center font-medium transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 active:scale-[0.98]',
  variants: {
    primary: 'bg-brand-600 text-white hover:bg-brand-700 active:bg-brand-800 shadow-sm hover:shadow-md',
    secondary: 'bg-surface-200 text-surface-900 hover:bg-surface-300 active:bg-surface-400 dark:bg-surface-700 dark:text-surface-100 dark:hover:bg-surface-600 dark:active:bg-surface-500',
    outline: 'border-2 border-surface-300 bg-transparent hover:bg-surface-100 active:bg-surface-200 dark:border-surface-600 dark:hover:bg-surface-800 dark:active:bg-surface-700',
    ghost: 'bg-transparent hover:bg-surface-100 active:bg-surface-200 dark:hover:bg-surface-800 dark:active:bg-surface-700',
    destructive: 'bg-red-600 text-white hover:bg-red-700 active:bg-red-800 shadow-sm hover:shadow-md',
    link: 'bg-transparent text-brand-600 underline-offset-4 hover:underline dark:text-brand-400',
  },
  sizes: {
    sm: 'h-8 px-3 text-sm gap-1.5 rounded-md',
    md: 'h-10 px-4 text-sm gap-2 rounded-lg',
    lg: 'h-12 px-6 text-base gap-2 rounded-lg',
    xl: 'h-14 px-8 text-lg gap-2.5 rounded-xl',
    icon: 'h-10 w-10 p-0 rounded-lg',
  },
  fullWidth: 'w-full',
};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = 'primary', size = 'md', loading = false, fullWidth = false, children, disabled, ...props }, ref) => {
    const isDisabled = disabled || loading;

    return (
      <button
        ref={ref}
        className={cn(
          buttonStyles.base,
          buttonStyles.variants[variant],
          buttonStyles.sizes[size],
          fullWidth && buttonStyles.fullWidth,
          className
        )}
        disabled={isDisabled}
        aria-busy={loading}
        aria-disabled={isDisabled}
        {...props}
      >
        {loading && (
          <svg
            className="animate-spin h-4 w-4"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';

// Icon button variant
export interface IconButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  'aria-label': string;
  children: React.ReactNode;
}

export const IconButton = React.forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ className, variant = 'ghost', size = 'md', 'aria-label': ariaLabel, children, ...props }, ref) => {
    return (
      <Button
        ref={ref}
        variant={variant}
        size={size}
        className={cn('p-0', className)}
        aria-label={ariaLabel}
        {...props}
      >
        {children}
      </Button>
    );
  }
);

IconButton.displayName = 'IconButton';

// Button group for grouped actions
export interface ButtonGroupProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  ariaLabel?: string;
}

export const ButtonGroup = React.forwardRef<HTMLDivElement, ButtonGroupProps>(
  ({ className, children, ariaLabel, ...props }, ref) => {
    return (
      <div
        ref={ref}
        role="group"
        aria-label={ariaLabel}
        className={cn('inline-flex rounded-lg', className)}
        {...props}
      >
        {React.Children.map(children, (child, index) => {
          if (!React.isValidElement(child)) return child;
          const isFirst = index === 0;
          const isLast = index === React.Children.count(children) - 1;
          return React.cloneElement(child as React.ReactElement<any>, {
            className: cn(
              (child.props as any).className,
              !isFirst && 'rounded-l-none',
              !isLast && 'rounded-r-none',
              !isFirst && 'border-l-0'
            ),
          });
        })}
      </div>
    );
  }
);

ButtonGroup.displayName = 'ButtonGroup';