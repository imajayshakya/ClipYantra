'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  hint?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
}

const inputStyles = {
  base: 'flex w-full rounded-lg border bg-surface-50 px-3 py-2.5 text-surface-900 placeholder:text-surface-400 transition-all duration-200 dark:bg-surface-800 dark:text-surface-100 dark:placeholder:text-surface-500',
  focus: 'focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 focus:outline-none',
  disabled: 'disabled:cursor-not-allowed disabled:opacity-50 disabled:bg-surface-100 dark:disabled:bg-surface-700',
  error: 'border-red-500 focus:border-red-500 focus:ring-red-500/20',
  sizes: {
    sm: 'h-8 text-sm px-2.5',
    md: 'h-10 text-sm',
    lg: 'h-12 text-base px-4',
  },
};

const labelStyles = 'mb-1.5 block text-sm font-medium text-surface-700 dark:text-surface-300';
const errorStyles = 'mt-1.5 text-sm text-red-600 dark:text-red-400';
const hintStyles = 'mt-1.5 text-sm text-surface-500 dark:text-surface-400';

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, label, error, hint, leftIcon, rightIcon, fullWidth = true, size = 'md', id, ...props }, ref) => {
    const inputId = id || React.useId();
    const errorId = error ? `${inputId}-error` : undefined;
    const hintId = hint ? `${inputId}-hint` : undefined;

    return (
      <div className={cn('w-full', fullWidth && 'w-full')}>
        {label && <label htmlFor={inputId} className={labelStyles}>{label}</label>}
        <div className="relative">
          {leftIcon && (
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-surface-400">
              {leftIcon}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            className={cn(
              inputStyles.base,
              inputStyles.focus,
              inputStyles.disabled,
              inputStyles.sizes[size],
              error && inputStyles.error,
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              className
            )}
            aria-invalid={!!error}
            aria-describedby={cn(errorId, hintId)}
            {...props}
          />
          {rightIcon && (
            <div className="absolute inset-y-0 right-0 flex items-center pr-3 text-surface-400">
              {rightIcon}
            </div>
          )}
        </div>
        {error && <p id={errorId} className={errorStyles} role="alert">{error}</p>}
        {hint && !error && <p id={hintId} className={hintStyles}>{hint}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';

// Textarea component
export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  hint?: string;
  fullWidth?: boolean;
}

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, hint, fullWidth = true, id, ...props }, ref) => {
    const textareaId = id || React.useId();
    const errorId = error ? `${textareaId}-error` : undefined;
    const hintId = hint ? `${textareaId}-hint` : undefined;

    return (
      <div className={cn('w-full', fullWidth && 'w-full')}>
        {label && <label htmlFor={textareaId} className={labelStyles}>{label}</label>}
        <textarea
          ref={ref}
          id={textareaId}
          className={cn(
            inputStyles.base,
            inputStyles.focus,
            inputStyles.disabled,
            'resize-y min-h-[100px]',
            error && inputStyles.error,
            className
          )}
          aria-invalid={!!error}
          aria-describedby={cn(errorId, hintId)}
          {...props}
        />
        {error && <p id={errorId} className={errorStyles} role="alert">{error}</p>}
        {hint && !error && <p id={hintId} className={hintStyles}>{hint}</p>}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';

// Select component
export interface SelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

export interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
  hint?: string;
  options: SelectOption[];
  placeholder?: string;
  fullWidth?: boolean;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, error, hint, options, placeholder, fullWidth = true, id, ...props }, ref) => {
    const selectId = id || React.useId();
    const errorId = error ? `${selectId}-error` : undefined;
    const hintId = hint ? `${selectId}-hint` : undefined;

    return (
      <div className={cn('w-full', fullWidth && 'w-full')}>
        {label && <label htmlFor={selectId} className={labelStyles}>{label}</label>}
        <div className="relative">
          <select
            ref={ref}
            id={selectId}
            className={cn(
              inputStyles.base,
              inputStyles.focus,
              inputStyles.disabled,
              'appearance-none pr-10',
              error && inputStyles.error,
              className
            )}
            aria-invalid={!!error}
            aria-describedby={cn(errorId, hintId)}
            {...props}
          >
            {placeholder && (
              <option value="" disabled>
                {placeholder}
              </option>
            )}
            {options.map((option) => (
              <option key={option.value} value={option.value} disabled={option.disabled}>
                {option.label}
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3 text-surface-400">
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
        {error && <p id={errorId} className={errorStyles} role="alert">{error}</p>}
        {hint && !error && <p id={hintId} className={hintStyles}>{hint}</p>}
      </div>
    );
  }
);

Select.displayName = 'Select';

// Checkbox component
export interface CheckboxProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label: string;
  description?: string;
  error?: string;
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ className, label, description, error, id, ...props }, ref) => {
    const checkboxId = id || React.useId();
    const descriptionId = description ? `${checkboxId}-description` : undefined;
    const errorId = error ? `${checkboxId}-error` : undefined;

    return (
      <div className="flex items-start gap-3">
        <input
          ref={ref}
          type="checkbox"
          id={checkboxId}
          className={cn(
            'h-4 w-4 mt-0.5 rounded border-surface-300 text-brand-600 focus:ring-2 focus:ring-brand-500/20 focus:ring-offset-2 dark:border-surface-600 dark:focus:ring-offset-surface-900',
            error && 'border-red-500 focus:ring-red-500/20',
            className
          )}
          aria-invalid={!!error}
          aria-describedby={cn(descriptionId, errorId)}
          {...props}
        )}
        <div className="flex flex-col">
          <label htmlFor={checkboxId} className="text-sm font-medium text-surface-900 dark:text-surface-100 cursor-pointer">
            {label}
          </label>
          {description && (
            <p id={descriptionId} className="mt-0.5 text-sm text-surface-500 dark:text-surface-400">
              {description}
            </p>
          )}
        </div>
        {error && <p id={errorId} className={errorStyles} role="alert">{error}</p>}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

// Radio group component
export interface RadioOption {
  value: string;
  label: string;
  description?: string;
  disabled?: boolean;
}

export interface RadioGroupProps {
  label?: string;
  error?: string;
  hint?: string;
  options: RadioOption[];
  value: string;
  onChange: (value: string) => void;
  name: string;
  orientation?: 'vertical' | 'horizontal';
  fullWidth?: boolean;
}

export const RadioGroup = React.forwardRef<HTMLDivElement, RadioGroupProps>(
  ({ className, label, error, hint, options, value, onChange, name, orientation = 'vertical', fullWidth = true }, ref) => {
    const groupId = React.useId();
    const errorId = error ? `${groupId}-error` : undefined;
    const hintId = hint ? `${groupId}-hint` : undefined;

    return (
      <div ref={ref} className={cn('w-full', fullWidth && 'w-full', className)} role="radiogroup" aria-labelledby={label ? groupId : undefined} aria-describedby={cn(errorId, hintId)} aria-invalid={!!error}>
        {label && <label id={groupId} className={labelStyles}>{label}</label>}
        <div className={cn('gap-3', orientation === 'horizontal' ? 'flex flex-wrap' : 'flex flex-col')}>
          {options.map((option) => (
            <label key={option.value} className={cn('flex items-start gap-3 cursor-pointer', option.disabled && 'opacity-50 cursor-not-allowed')}>
              <input
                type="radio"
                name={name}
                value={option.value}
                checked={value === option.value}
                onChange={() => onChange(option.value)}
                disabled={option.disabled}
                className="h-4 w-4 mt-0.5 border-surface-300 text-brand-600 focus:ring-2 focus:ring-brand-500/20 dark:border-surface-600"
              />
              <div>
                <span className="block text-sm font-medium text-surface-900 dark:text-surface-100">{option.label}</span>
                {option.description && (
                  <p className="mt-0.5 text-sm text-surface-500 dark:text-surface-400">{option.description}</p>
                )}
              </div>
            </label>
          ))}
        </div>
        {error && <p id={errorId} className={errorStyles} role="alert">{error}</p>}
        {hint && !error && <p id={hintId} className={hintStyles}>{hint}</p>}
      </div>
    );
  }
);

RadioGroup.displayName = 'RadioGroup';

// Switch component
export interface SwitchProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'type'> {
  label: string;
  description?: string;
  error?: string;
}

export const Switch = React.forwardRef<HTMLInputElement, SwitchProps>(
  ({ className, label, description, error, id, ...props }, ref) => {
    const switchId = id || React.useId();
    const descriptionId = description ? `${switchId}-description` : undefined;
    const errorId = error ? `${switchId}-error` : undefined;

    return (
      <div className="flex items-center gap-3">
        <label htmlFor={switchId} className="relative inline-flex items-center cursor-pointer">
          <input
            ref={ref}
            type="checkbox"
            id={switchId}
            className="sr-only peer"
            aria-invalid={!!error}
            aria-describedby={cn(descriptionId, errorId)}
            {...props}
          />
          <div className={cn(
            'w-11 h-6 rounded-full border-2 transition-colors duration-200',
            'peer-focus-visible:outline-none peer-focus-visible:ring-2 peer-focus-visible:ring-brand-500/20 peer-focus-visible:ring-offset-2',
            'peer-checked:bg-brand-600 peer-checked:border-brand-600',
            'peer-checked:after:translate-x-full',
            'dark:peer-checked:bg-brand-500 dark:peer-checked:border-brand-500',
            'peer-disabled:opacity-50 peer-disabled:cursor-not-allowed',
            error && 'peer-checked:bg-red-500 peer-checked:border-red-500',
            'bg-surface-200 border-surface-300 dark:bg-surface-700 dark:border-surface-600'
          )}>
            <span className={cn(
              'after:content-[""] after:absolute after:top-0.5 after:left-0.5 after:h-4 after:w-4 after:rounded-full after:bg-white after:shadow after:transition-transform after:duration-200',
              'dark:after:bg-surface-100'
            )} />
          </div>
        </label>
        <div className="flex flex-col">
          <span className="text-sm font-medium text-surface-900 dark:text-surface-100">{label}</span>
          {description && (
            <p id={descriptionId} className="mt-0.5 text-sm text-surface-500 dark:text-surface-400">{description}</p>
          )}
        </div>
        {error && <p id={errorId} className={errorStyles} role="alert">{error}</p>}
      </div>
    );
  }
);

Switch.displayName = 'Switch';

// Label component
export interface LabelProps extends React.LabelHTMLAttributes<HTMLLabelElement> {
  required?: boolean;
  children: React.ReactNode;
}

export const Label = React.forwardRef<HTMLLabelElement, LabelProps>(
  ({ className, required, children, ...props }, ref) => {
    return (
      <label
        ref={ref}
        className={cn(labelStyles, className)}
        {...props}
      >
        {children}
        {required && <span className="ml-1 text-red-500" aria-hidden="true">*</span>}
      </label>
    );
  }
);

Label.displayName = 'Label';