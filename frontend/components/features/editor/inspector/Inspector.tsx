'use client';

import * as React from 'react';
import { cn } from '@/lib/utils';
import { X, ChevronDown, ChevronUp, Trash2, Copy, Settings, Keyframe } from 'lucide-react';

interface InspectorProps {
  className?: string;
  selectedItem?: {
    type: 'clip' | 'track' | 'effect' | 'project';
    id: string;
    data: any;
  } | null;
  onDelete: (itemId: string) => void;
  onDuplicate: (itemId: string) => void;
  onPropertyChange: (itemId: string, property: string, value: any) => void;
  availableEffects: string[];
  onAddEffect: (itemId: string, effectId: string) => void;
  onRemoveEffect: (itemId: string, effectId: string) => void;
}

export function Inspector({
  className,
  selectedItem,
  onDelete,
  onDuplicate,
  onPropertyChange,
  availableEffects,
  onAddEffect,
  onRemoveEffect,
}: InspectorProps) {
  if (!selectedItem) {
    return (
      <div className={cn('flex flex-col h-full bg-surface-50 dark:bg-surface-900 p-6', className)}>
        <div className="flex-1 flex flex-col items-center justify-center text-surface-500">
          <Settings className="h-16 w-16 mb-4 opacity-30" />
          <h3 className="text-lg font-medium">No selection</h3>
          <p className="text-sm mt-1">Select a clip, track, or effect to inspect</p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn('flex flex-col h-full bg-surface-50 dark:bg-surface-900', className)}>
      {/* Header */}
      <div className="p-4 border-b border-surface-200 dark:border-surface-700 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <h2 className="text-lg font-semibold text-surface-900 dark:text-surface-100 capitalize">
            {selectedItem.type} inspector
          </h2>
          <span className="px-2 py-0.5 text-xs font-medium bg-brand-100 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300 rounded-full">
            {selectedItem.id.slice(0, 8)}...
          </span>
        </div>
        <div className="flex items-center gap-1">
          <button
            onClick={() => onDuplicate(selectedItem.id)}
            className="p-2 text-surface-500 hover:text-surface-700 dark:hover:text-surface-300 transition-colors rounded-lg hover:bg-surface-100 dark:hover:bg-surface-800"
            aria-label="Duplicate"
          >
            <Copy className="h-4 w-4" />
          </button>
          <button
            onClick={() => onDelete(selectedItem.id)}
            className="p-2 text-red-500 hover:text-red-700 transition-colors rounded-lg hover:bg-red-50 dark:hover:bg-red-900/30"
            aria-label="Delete"
          >
            <Trash2 className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {selectedItem.type === 'clip' && (
          <ClipInspectorPanel
            clip={selectedItem.data}
            onPropertyChange={(prop, value) => onPropertyChange(selectedItem.id, prop, value)}
            availableEffects={availableEffects}
            onAddEffect={(effectId) => onAddEffect(selectedItem.id, effectId)}
            onRemoveEffect={(effectId) => onRemoveEffect(selectedItem.id, effectId)}
          />
        )}

        {selectedItem.type === 'track' && (
          <TrackInspectorPanel
            track={selectedItem.data}
            onPropertyChange={(prop, value) => onPropertyChange(selectedItem.id, prop, value)}
          />
        )}

        {selectedItem.type === 'effect' && (
          <EffectInspectorPanel
            effect={selectedItem.data}
            onPropertyChange={(prop, value) => onPropertyChange(selectedItem.id, prop, value)}
          />
        )}

        {selectedItem.type === 'project' && (
          <ProjectInspectorPanel
            project={selectedItem.data}
            onPropertyChange={(prop, value) => onPropertyChange(selectedItem.id, prop, value)}
          />
        )}
      </div>
    </div>
  );
}

// Clip Inspector Panel
function ClipInspectorPanel({
  clip,
  onPropertyChange,
  availableEffects,
  onAddEffect,
  onRemoveEffect,
}: {
  clip: any;
  onPropertyChange: (prop: string, value: any) => void;
  availableEffects: string[];
  onAddEffect: (effectId: string) => void;
  onRemoveEffect: (effectId: string) => void;
}) {
  const [expandedSections, setExpandedSections] = React.useState({
    transform: true,
    appearance: true,
    effects: true,
    audio: true,
    metadata: false,
  });

  const toggleSection = (section: string) => {
    setExpandedSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  return (
    <div className="space-y-6">
      {/* Transform */}
      <InspectorSection title="Transform" expanded={expandedSections.transform} onToggle={() => toggleSection('transform')}>
        <div className="space-y-4">
          <InspectorRow label="Position">
            <div className="flex gap-2">
              <NumberInput
                label="X"
                value={clip.transform?.x || 0}
                onChange={(v) => onPropertyChange('transform', { ...clip.transform, x: v })}
                step={1}
                unit="px"
              />
              <NumberInput
                label="Y"
                value={clip.transform?.y || 0}
                onChange={(v) => onPropertyChange('transform', { ...clip.transform, y: v })}
                step={1}
                unit="px"
              />
            </div>
          </InspectorRow>
          <InspectorRow label="Scale">
            <div className="flex gap-2">
              <NumberInput
                label="X"
                value={clip.transform?.scaleX || 1}
                onChange={(v) => onPropertyChange('transform', { ...clip.transform, scaleX: v })}
                step={0.01}
                min={0.01}
                max={10}
              />
              <NumberInput
                label="Y"
                value={clip.transform?.scaleY || 1}
                onChange={(v) => onPropertyChange('transform', { ...clip.transform, scaleY: v })}
                step={0.01}
                min={0.01}
                max={10}
              />
            </div>
          </InspectorRow>
          <InspectorRow label="Rotation">
            <NumberInput
              value={clip.transform?.rotation || 0}
              onChange={(v) => onPropertyChange('transform', { ...clip.transform, rotation: v })}
              step={1}
              min={-360}
              max={360}
              unit="°"
            />
          </InspectorRow>
          <InspectorRow label="Anchor Point">
            <div className="flex gap-2">
              <NumberInput
                label="X"
                value={clip.transform?.anchorX || 0.5}
                onChange={(v) => onPropertyChange('transform', { ...clip.transform, anchorX: v })}
                step={0.01}
                min={0}
                max={1}
              />
              <NumberInput
                label="Y"
                value={clip.transform?.anchorY || 0.5}
                onChange={(v) => onPropertyChange('transform', { ...clip.transform, anchorY: v })}
                step={0.01}
                min={0}
                max={1}
              />
            </div>
          </InspectorRow>
          <InspectorRow label="Opacity">
            <SliderInput
              value={clip.transform?.opacity ?? 1}
              onChange={(v) => onPropertyChange('transform', { ...clip.transform, opacity: v })}
              min={0}
              max={1}
              step={0.01}
            />
          </InspectorRow>
        </div>
      </InspectorSection>

      {/* Appearance */}
      <InspectorSection title="Appearance" expanded={expandedSections.appearance} onToggle={() => toggleSection('appearance')}>
        <div className="space-y-4">
          <InspectorRow label="Blend Mode">
            <SelectInput
              value={clip.blendMode || 'normal'}
              onChange={(v) => onPropertyChange('blendMode', v)}
              options={[
                'normal', 'multiply', 'screen', 'overlay', 'darken', 'lighten',
                'color-dodge', 'color-burn', 'hard-light', 'soft-light', 'difference', 'exclusion'
              ]}
            />
          </InspectorRow>
          <InspectorRow label="Filter">
            <SelectInput
              value={clip.filter || 'none'}
              onChange={(v) => onPropertyChange('filter', v)}
              options={['none', 'grayscale', 'sepia', 'invert', 'blur', 'brightness', 'contrast', 'hue-rotate', 'saturate']}
            />
          </InspectorRow>
          <InspectorRow label="Filter Intensity">
            <SliderInput
              value={clip.filterIntensity || 1}
              onChange={(v) => onPropertyChange('filterIntensity', v)}
              min={0}
              max={2}
              step={0.01}
            />
          </InspectorRow>
        </div>
      </InspectorSection>

      {/* Effects */}
      <InspectorSection title="Effects" expanded={expandedSections.effects} onToggle={() => toggleSection('effects')}>
        <div className="space-y-4">
          {/* Applied effects */}
          {clip.effects?.length > 0 && (
            <div className="space-y-2">
              <h4 className="text-sm font-medium text-surface-700 dark:text-surface-300">Applied Effects</h4>
              {clip.effects.map((effect: any) => (
                <div key={effect.id} className="flex items-center justify-between p-3 bg-surface-100 dark:bg-surface-800 rounded-lg">
                  <div className="flex items-center gap-3">
                    <Keyframe className="h-5 w-5 text-surface-500" />
                    <div>
                      <p className="text-sm font-medium text-surface-900 dark:text-surface-100">{effect.name}</p>
                      <p className="text-xs text-surface-500">{effect.category}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => onRemoveEffect(effect.id)}
                    className="p-1.5 text-surface-400 hover:text-red-500 transition-colors rounded hover:bg-surface-200 dark:hover:bg-surface-700"
                    aria-label={`Remove ${effect.name}`}
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ))}
            </div>
          )}

          {/* Add effect */}
          <div className="pt-2 border-t border-surface-200 dark:border-surface-700">
            <h4 className="text-sm font-medium text-surface-700 dark:text-surface-300 mb-2">Add Effect</h4>
            <div className="flex flex-wrap gap-2">
              {availableEffects.map((effect) => (
                <button
                  key={effect}
                  onClick={() => onAddEffect(effect)}
                  className="px-3 py-1.5 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg hover:bg-brand-50 dark:hover:bg-brand-900/30 hover:border-brand-300 dark:hover:border-brand-700 transition-all"
                >
                  {effect}
                </button>
              ))}
            </div>
          </div>
        </div>
      </InspectorSection>

      {/* Audio */}
      <InspectorSection title="Audio" expanded={expandedSections.audio} onToggle={() => toggleSection('audio')}>
        <div className="space-y-4">
          <InspectorRow label="Volume">
            <SliderInput
              value={clip.audio?.volume ?? 1}
              onChange={(v) => onPropertyChange('audio', { ...clip.audio, volume: v })}
              min={0}
              max={2}
              step={0.01}
            />
          </InspectorRow>
          <InspectorRow label="Pan">
            <SliderInput
              value={clip.audio?.pan ?? 0}
              onChange={(v) => onPropertyChange('audio', { ...clip.audio, pan: v })}
              min={-1}
              max={1}
              step={0.01}
            />
          </InspectorRow>
          <InspectorRow label="Mute">
            <CheckboxInput
              checked={clip.audio?.muted || false}
              onChange={(v) => onPropertyChange('audio', { ...clip.audio, muted: v })}
            />
          </InspectorRow>
          <InspectorRow label="Fade In">
            <NumberInput
              value={clip.audio?.fadeIn || 0}
              onChange={(v) => onPropertyChange('audio', { ...clip.audio, fadeIn: v })}
              step={0.1}
              min={0}
              unit="s"
            />
          </InspectorRow>
          <InspectorRow label="Fade Out">
            <NumberInput
              value={clip.audio?.fadeOut || 0}
              onChange={(v) => onPropertyChange('audio', { ...clip.audio, fadeOut: v })}
              step={0.1}
              min={0}
              unit="s"
            />
          </InspectorRow>
        </div>
      </InspectorSection>

      {/* Metadata */}
      <InspectorSection title="Metadata" expanded={expandedSections.metadata} onToggle={() => toggleSection('metadata')}>
        <div className="space-y-3 text-sm">
          <div className="grid grid-cols-2 gap-2">
            <span className="text-surface-500">Duration</span>
            <span className="text-surface-900 dark:text-surface-100 font-mono">{clip.duration?.toFixed(2)}s</span>
            <span className="text-surface-500">Start Time</span>
            <span className="text-surface-900 dark:text-surface-100 font-mono">{clip.startTime?.toFixed(2)}s</span>
            <span className="text-surface-500">End Time</span>
            <span className="text-surface-900 dark:text-surface-100 font-mono">{clip.endTime?.toFixed(2)}s</span>
            <span className="text-surface-500">Media ID</span>
            <span className="text-surface-900 dark:text-surface-100 font-mono truncate max-w-[150px]">{clip.mediaId}</span>
          </div>
        </div>
      </InspectorSection>
    </div>
  );
}

// Track Inspector Panel
function TrackInspectorPanel({
  track,
  onPropertyChange,
}: {
  track: any;
  onPropertyChange: (prop: string, value: any) => void;
}) {
  return (
    <div className="space-y-6">
      <InspectorSection title="Track Settings" expanded={true}>
        <div className="space-y-4">
          <InspectorRow label="Name">
            <input
              type="text"
              value={track.name}
              onChange={(e) => onPropertyChange('name', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </InspectorRow>
          <InspectorRow label="Type">
            <SelectInput
              value={track.type}
              onChange={(v) => onPropertyChange('type', v)}
              options={['video', 'audio', 'text', 'effect']}
            />
          </InspectorRow>
          <InspectorRow label="Visible">
            <CheckboxInput
              checked={track.visible !== false}
              onChange={(v) => onPropertyChange('visible', v)}
            />
          </InspectorRow>
          <InspectorRow label="Locked">
            <CheckboxInput
              checked={track.locked || false}
              onChange={(v) => onPropertyChange('locked', v)}
            />
          </InspectorRow>
          <InspectorRow label="Muted">
            <CheckboxInput
              checked={track.muted || false}
              onChange={(v) => onPropertyChange('muted', v)}
            />
          </InspectorRow>
          <InspectorRow label="Height">
            <NumberInput
              value={track.height || 80}
              onChange={(v) => onPropertyChange('height', v)}
              step={10}
              min={40}
              max={300}
              unit="px"
            />
          </InspectorRow>
        </div>
      </InspectorSection>
    </div>
  );
}

// Effect Inspector Panel
function EffectInspectorPanel({
  effect,
  onPropertyChange,
}: {
  effect: any;
  onPropertyChange: (prop: string, value: any) => void;
}) {
  return (
    <div className="space-y-6">
      <InspectorSection title={effect.name} expanded={true}>
        <div className="space-y-4">
          <InspectorRow label="Enabled">
            <CheckboxInput
              checked={effect.enabled !== false}
              onChange={(v) => onPropertyChange('enabled', v)}
            />
          </InspectorRow>
          {effect.parameters?.map((param: any) => (
            <InspectorRow key={param.key} label={param.label}>
              {param.type === 'number' && (
                <NumberInput
                  value={effect.parameters[param.key] || param.default}
                  onChange={(v) => {
                    const newParams = { ...effect.parameters, [param.key]: v };
                    onPropertyChange('parameters', newParams);
                  }}
                  step={param.step || 1}
                  min={param.min}
                  max={param.max}
                  unit={param.unit}
                />
              )}
              {param.type === 'boolean' && (
                <CheckboxInput
                  checked={effect.parameters[param.key] || param.default}
                  onChange={(v) => {
                    const newParams = { ...effect.parameters, [param.key]: v };
                    onPropertyChange('parameters', newParams);
                  }}
                />
              )}
              {param.type === 'color' && (
                <ColorInput
                  value={effect.parameters[param.key] || param.default}
                  onChange={(v) => {
                    const newParams = { ...effect.parameters, [param.key]: v };
                    onPropertyChange('parameters', newParams);
                  }}
                />
              )}
              {param.type === 'select' && (
                <SelectInput
                  value={effect.parameters[param.key] || param.default}
                  onChange={(v) => {
                    const newParams = { ...effect.parameters, [param.key]: v };
                    onPropertyChange('parameters', newParams);
                  }}
                  options={param.options}
                />
              )}
            </InspectorRow>
          ))}
        </div>
      </InspectorSection>
    </div>
  );
}

// Project Inspector Panel
function ProjectInspectorPanel({
  project,
  onPropertyChange,
}: {
  project: any;
  onPropertyChange: (prop: string, value: any) => void;
}) {
  return (
    <div className="space-y-6">
      <InspectorSection title="Project Settings" expanded={true}>
        <div className="space-y-4">
          <InspectorRow label="Name">
            <input
              type="text"
              value={project.name}
              onChange={(e) => onPropertyChange('name', e.target.value)}
              className="w-full px-3 py-2 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
            />
          </InspectorRow>
          <InspectorRow label="Resolution">
            <div className="flex gap-2">
              <NumberInput
                label="Width"
                value={project.resolution?.width || 1920}
                onChange={(v) => onPropertyChange('resolution', { ...project.resolution, width: v })}
                step={1}
                min={1}
              />
              <NumberInput
                label="Height"
                value={project.resolution?.height || 1080}
                onChange={(v) => onPropertyChange('resolution', { ...project.resolution, height: v })}
                step={1}
                min={1}
              />
            </div>
          </InspectorRow>
          <InspectorRow label="Frame Rate">
            <NumberInput
              value={project.frameRate || 30}
              onChange={(v) => onPropertyChange('frameRate', v)}
              step={1}
              min={1}
              max={120}
              unit="fps"
            />
          </InspectorRow>
          <InspectorRow label="Background Color">
            <ColorInput
              value={project.backgroundColor || '#000000'}
              onChange={(v) => onPropertyChange('backgroundColor', v)}
            />
          </InspectorRow>
        </div>
      </InspectorSection>
    </div>
  );
}

// Shared Inspector Components
function InspectorSection({ title, expanded, onToggle, children }: {
  title: string;
  expanded: boolean;
  onToggle: () => void;
  children: React.ReactNode;
}) {
  return (
    <div className="bg-white dark:bg-surface-800 rounded-lg border border-surface-200 dark:border-surface-700 overflow-hidden">
      <button
        onClick={onToggle}
        className="w-full px-4 py-3 flex items-center justify-between hover:bg-surface-50 dark:hover:bg-surface-700/50 transition-colors"
        aria-expanded={expanded}
      >
        <h3 className="font-medium text-surface-900 dark:text-surface-100">{title}</h3>
        {expanded ? <ChevronUp className="h-5 w-5 text-surface-500" /> : <ChevronDown className="h-5 w-5 text-surface-500" />}
      </button>
      {expanded && (
        <div className="px-4 pb-4 border-t border-surface-200 dark:border-surface-700 animate-in slide-in-from-top-2 duration-150">
          {children}
        </div>
      )}
    </div>
  );
}

function InspectorRow({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-center gap-4">
      <label className="w-28 text-sm text-surface-600 dark:text-surface-400 font-medium shrink-0">{label}</label>
      <div className="flex-1">{children}</div>
    </div>
  );
}

function NumberInput({
  label,
  value,
  onChange,
  step = 1,
  min,
  max,
  unit,
}: {
  label?: string;
  value: number;
  onChange: (value: number) => void;
  step?: number;
  min?: number;
  max?: number;
  unit?: string;
}) {
  return (
    <div className="flex items-center gap-2">
      <input
        type="number"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value) || 0)}
        step={step}
        min={min}
        max={max}
        className="w-20 px-2 py-1.5 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 text-right"
      />
      {unit && <span className="text-xs text-surface-500">{unit}</span>}
    </div>
  );
}

function SliderInput({
  value,
  onChange,
  min = 0,
  max = 1,
  step = 0.01,
}: {
  value: number;
  onChange: (value: number) => void;
  min?: number;
  max?: number;
  step?: number;
}) {
  return (
    <div className="flex items-center gap-3 flex-1 max-w-xs">
      <input
        type="range"
        value={value}
        onChange={(e) => onChange(parseFloat(e.target.value))}
        min={min}
        max={max}
        step={step}
        className="flex-1 h-1.5 bg-surface-200 dark:bg-surface-700 rounded-lg appearance-none accent-brand-500 cursor-pointer"
      />
      <span className="w-12 text-sm text-right text-surface-900 dark:text-surface-100 font-mono">
        {(value * 100).toFixed(0)}%
      </span>
    </div>
  );
}

function CheckboxInput({
  checked,
  onChange,
}: {
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <button
      onClick={() => onChange(!checked)}
      className={cn(
        'relative w-10 h-6 rounded-full transition-colors',
        checked ? 'bg-brand-500' : 'bg-surface-200 dark:bg-surface-700'
      )}
      role="switch"
      aria-checked={checked}
    >
      <span
        className={cn(
          'absolute top-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform',
          checked ? 'translate-x-5' : 'translate-x-0.5'
        )}
      />
    </button>
  );
}

function SelectInput({
  value,
  onChange,
  options,
}: {
  value: string;
  onChange: (value: string) => void;
  options: string[];
}) {
  return (
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full max-w-xs px-3 py-2 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500"
    >
      {options.map((option) => (
        <option key={option} value={option}>{option}</option>
      ))}
    </select>
  );
}

function ColorInput({
  value,
  onChange,
}: {
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <div className="flex items-center gap-2">
      <input
        type="color"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-10 h-10 rounded-lg border border-surface-200 dark:border-surface-700 cursor-pointer"
      />
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-24 px-2 py-1.5 text-sm bg-surface-100 dark:bg-surface-800 border border-surface-200 dark:border-surface-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 font-mono uppercase"
      />
    </div>
  );
}