'use client';

import { useState } from 'react';
import { User, Bell, Shield, Palette, Globe, Key, Trash2, Save, Loader2 } from '@/components/ui/icons';

const tabs = [
  { id: 'profile', name: 'Profile', icon: User },
  { id: 'notifications', name: 'Notifications', icon: Bell },
  { id: 'security', name: 'Security', icon: Shield },
  { id: 'appearance', name: 'Appearance', icon: Palette },
  { id: 'language', name: 'Language', icon: Globe },
  { id: 'danger', name: 'Danger Zone', icon: Trash2 },
];

export default function SettingsPage() {
  const [activeTab, setActiveTab] = useState('profile');
  const [isSaving, setIsSaving] = useState(false);

  const handleSave = async () => {
    setIsSaving(true);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsSaving(false);
  };

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-display-sm font-bold text-text-primary">Settings</h1>
        <p className="mt-1 text-body-md text-text-secondary">
          Manage your account, preferences, and security settings
        </p>
      </div>

      <div className="card overflow-hidden">
        <div className="flex flex-col lg:flex-row">
          {/* Sidebar navigation */}
          <aside className="lg:w-56 border-r border-border-default bg-surface-50/50 dark:bg-surface-900/50 dark:border-surface-800">
            <nav className="p-4 space-y-1" aria-label="Settings sections">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={clsx(
                    'w-full flex items-center gap-3 rounded-lg px-3 py-2.5 text-body-sm font-medium transition-all duration-fast',
                    activeTab === tab.id
                      ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/50 dark:text-brand-300'
                      : 'text-text-secondary hover:bg-surface-100 hover:text-text-primary dark:hover:bg-surface-800'
                  )}
                  aria-current={activeTab === tab.id ? 'page' : undefined}
                >
                  <tab.icon className="h-5 w-5 flex-shrink-0" aria-hidden="true" />
                  <span>{tab.name}</span>
                </button>
              ))}
            </nav>
          </aside>

          {/* Content panels */}
          <main className="flex-1 p-6 lg:p-8 overflow-y-auto">
            {activeTab === 'profile' && <ProfileTab />}
            {activeTab === 'notifications' && <NotificationsTab />}
            {activeTab === 'security' && <SecurityTab />}
            {activeTab === 'appearance' && <AppearanceTab />}
            {activeTab === 'language' && <LanguageTab />}
            {activeTab === 'danger' && <DangerZoneTab />}

            {/* Save button for all tabs */}
            <div className="mt-8 pt-6 border-t border-border-default flex justify-end">
              <button
                onClick={handleSave}
                disabled={isSaving}
                className="btn-primary"
              >
                {isSaving ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                    <span>Saving...</span>
                  </>
                ) : (
                  <>
                    <Save className="h-4 w-4" aria-hidden="true" />
                    <span>Save Changes</span>
                  </>
                )}
              </button>
            </div>
          </main>
        </div>
      </div>
    </div>
  );
}

function ProfileTab() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-heading-lg font-semibold text-text-primary mb-2">Profile</h2>
        <p className="text-body-md text-text-secondary">Manage your personal information and public profile</p>
      </div>

      <div className="flex items-center gap-6 p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
        <div className="h-20 w-20 rounded-full bg-brand-100 flex items-center justify-center flex-shrink-0 dark:bg-brand-900/50">
          <User className="h-10 w-10 text-brand-600 dark:text-brand-400" aria-hidden="true" />
        </div>
        <div>
          <label className="btn-outline btn-sm">Change Avatar</label>
          <input type="file" accept="image/*" className="sr-only" id="avatar-upload" />
          <p className="mt-1 text-body-sm text-text-muted">JPG, PNG up to 2MB</p>
        </div>
      </div>

      <div className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="firstName" className="label">First Name</label>
            <input id="firstName" type="text" defaultValue="John" className="input" />
          </div>
          <div>
            <label htmlFor="lastName" className="label">Last Name</label>
            <input id="lastName" type="text" defaultValue="Doe" className="input" />
          </div>
        </div>
        <div>
          <label htmlFor="email" className="label">Email Address</label>
          <input id="email" type="email" defaultValue="john@clipyantra.com" className="input" />
          <p className="mt-1 text-body-sm text-text-muted">This email is used for login and notifications</p>
        </div>
        <div>
          <label htmlFor="username" className="label">Username</label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted">@</span>
            <input id="username" type="text" defaultValue="johndoe" className="input pl-8" />
          </div>
          <p className="mt-1 text-body-sm text-text-muted">Your public profile: clipyantra.com/@johndoe</p>
        </div>
        <div>
          <label htmlFor="bio" className="label">Bio</label>
          <textarea id="bio" rows={3} defaultValue="Video creator and AI enthusiast. Building the future of content creation." className="input resize-none" />
        </div>
        <div>
          <label htmlFor="website" className="label">Website</label>
          <input id="website" type="url" defaultValue="https://johndoe.com" className="input" placeholder="https://example.com" />
        </div>
      </div>
    </div>
  );
}

function NotificationsTab() {
  const notificationTypes = [
    { name: 'Email Notifications', description: 'Receive updates via email', enabled: true },
    { name: 'Project Complete', description: 'Notify when clip generation finishes', enabled: true },
    { name: 'Weekly Digest', description: 'Weekly summary of your activity', enabled: false },
    { name: 'Marketing Emails', description: 'Product updates and tips', enabled: false },
    { name: 'Push Notifications', description: 'Browser notifications for important events', enabled: true },
    { name: 'Team Activity', description: 'Comments, mentions, and approvals', enabled: true },
  ];

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-heading-lg font-semibold text-text-primary mb-2">Notifications</h2>
        <p className="text-body-md text-text-secondary">Choose how and when you want to be notified</p>
      </div>

      <div className="space-y-4">
        {notificationTypes.map((notification) => (
          <div key={notification.name} className="flex items-center justify-between p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
            <div>
              <p className="font-medium text-text-primary">{notification.name}</p>
              <p className="text-body-sm text-text-muted">{notification.description}</p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                defaultChecked={notification.enabled}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-surface-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-brand-500/20 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-brand-600"></div>
            </label>
          </div>
        ))}
      </div>
    </div>
  );
}

function SecurityTab() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-heading-lg font-semibold text-text-primary mb-2">Security</h2>
        <p className="text-body-md text-text-secondary">Manage your password and two-factor authentication</p>
      </div>

      <div className="space-y-6">
        <section className="p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
          <h3 className="text-heading-md font-semibold text-text-primary mb-4">Password</h3>
          <div className="space-y-4">
            <div>
              <label htmlFor="currentPassword" className="label">Current Password</label>
              <input id="currentPassword" type="password" className="input" placeholder="••••••••" />
            </div>
            <div>
              <label htmlFor="newPassword" className="label">New Password</label>
              <input id="newPassword" type="password" className="input" placeholder="••••••••" />
              <p className="mt-1 text-body-sm text-text-muted">At least 8 characters with uppercase, lowercase, number, and symbol</p>
            </div>
            <div>
              <label htmlFor="confirmPassword" className="label">Confirm New Password</label>
              <input id="confirmPassword" type="password" className="input" placeholder="••••••••" />
            </div>
          </div>
        </section>

        <section className="p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-heading-md font-semibold text-text-primary">Two-Factor Authentication</h3>
              <p className="text-body-sm text-text-muted">Add an extra layer of security to your account</p>
            </div>
            <span className="badge badge-warning">Not Enabled</span>
          </div>
          <button className="btn-outline">
            <Shield className="h-4 w-4" aria-hidden="true" />
            <span>Enable 2FA</span>
          </button>
        </section>

        <section className="p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
          <h3 className="text-heading-md font-semibold text-text-primary mb-4">Active Sessions</h3>
          <div className="space-y-3">
            {sessions.map((session) => (
              <div key={session.id} className="flex items-center justify-between p-3 bg-background-primary rounded-lg border border-border-default">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-lg bg-brand-100 flex items-center justify-center dark:bg-brand-900/50">
                    {session.icon}
                  </div>
                  <div>
                    <p className="font-medium text-text-primary">{session.device}</p>
                    <p className="text-body-sm text-text-muted">{session.location} · {session.lastActive}</p>
                  </div>
                </div>
                {session.current ? (
                  <span className="badge badge-primary text-xs">Current</span>
                ) : (
                  <button className="btn-ghost btn-sm btn-icon text-error hover:bg-error/10" aria-label={`Revoke ${session.device} session`}>
                    <Trash2 className="h-4 w-4" aria-hidden="true" />
                  </button>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}

function AppearanceTab() {
  const themes = [
    { id: 'light', name: 'Light', icon: '☀️' },
    { id: 'dark', name: 'Dark', icon: '🌙' },
    { id: 'system', name: 'System', icon: '💻' },
  ];

  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-heading-lg font-semibold text-text-primary mb-2">Appearance</h2>
        <p className="text-body-md text-text-secondary">Customize how ClipYantra looks on your device</p>
      </div>

      <section className="p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
        <h3 className="text-heading-md font-semibold text-text-primary mb-4">Theme</h3>
        <div className="grid gap-4 sm:grid-cols-3">
          {themes.map((theme) => (
            <button
              key={theme.id}
              className={clsx(
                'p-4 rounded-xl border-2 transition-all text-left',
                theme.id === 'system'
                  ? 'border-brand-500 bg-brand-50 dark:bg-brand-900/20'
                  : 'border-border-default hover:border-brand-300 dark:hover:border-surface-600'
              )}
            >
              <span className="text-3xl block mb-2" role="img" aria-label={theme.icon}>{theme.icon}</span>
              <span className="font-medium text-text-primary">{theme.name}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="p-4 bg-surface-50 dark:bg-surface-900/50 rounded-xl">
        <h3 className="text-heading-md font-semibold text-text-primary mb-4">Density</h3>
        <div className="flex gap-4">
          {['Comfortable', 'Compact', 'Spacious'].map((density) => (
            <label key={density} className="flex-1 cursor-pointer">
              <input type="radio" name="density" defaultChecked={density === 'Comfortable'} className="sr-only peer" />
              <div className={clsx(
                'p-4 rounded-xl border-2 text-center transition-all',
                'peer-checked:border-brand-500 peer-checked:bg-brand-50 dark:peer-checked:bg-brand-900/20 border-border-default'
              )}>
                <span className="font-medium text-text-primary">{density}</span>
              </div>
            </label>
          ))}
        </div>
      </section>
    </div>
  );
}

function LanguageTab() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-heading-lg font-semibold text-text-primary mb-2">Language & Region</h2>
        <p className="text-body-md text-text-secondary">Set your preferred language and regional settings</p>
      </div>

      <div className="space-y-4">
        <div>
          <label htmlFor="language" className="label">Language</label>
          <select id="language" className="input">
            <option value="en">English (US)</option>
            <option value="en-GB">English (UK)</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            <option value="ja">Japanese</option>
            <option value="ko">Korean</option>
            <option value="zh">Chinese (Simplified)</option>
          </select>
        </div>
        <div>
          <label htmlFor="timezone" className="label">Timezone</label>
          <select id="timezone" className="input">
            <option value="UTC">UTC</option>
            <option value="America/New_York">Eastern Time (US & Canada)</option>
            <option value="America/Chicago">Central Time (US & Canada)</option>
            <option value="America/Denver">Mountain Time (US & Canada)</option>
            <option value="America/Los_Angeles">Pacific Time (US & Canada)</option>
            <option value="Europe/London">London</option>
            <option value="Europe/Paris">Paris</option>
            <option value="Asia/Tokyo">Tokyo</option>
            <option value="Asia/Shanghai">Shanghai</option>
          </select>
        </div>
        <div>
          <label htmlFor="dateFormat" className="label">Date Format</label>
          <select id="dateFormat" className="input">
            <option value="MM/DD/YYYY">MM/DD/YYYY</option>
            <option value="DD/MM/YYYY">DD/MM/YYYY</option>
            <option value="YYYY-MM-DD">YYYY-MM-DD</option>
          </select>
        </div>
        <div>
          <label htmlFor="timeFormat" className="label">Time Format</label>
          <select id="timeFormat" className="input">
            <option value="12h">12 Hour (3:30 PM)</option>
            <option value="24h">24 Hour (15:30)</option>
          </select>
        </div>
      </div>
    </div>
  );
}

function DangerZoneTab() {
  return (
    <div className="space-y-6 max-w-2xl">
      <div>
        <h2 className="text-heading-lg font-semibold text-text-primary mb-2">Danger Zone</h2>
        <p className="text-body-md text-text-secondary">Irreversible and destructive actions</p>
      </div>

      <div className="p-4 bg-error/5 border border-error/20 rounded-xl">
        <div className="flex items-start gap-3">
          <Trash2 className="h-5 w-5 text-error flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <h3 className="font-semibold text-error">Delete Account</h3>
            <p className="mt-1 text-body-sm text-text-secondary">
              Permanently delete your account and all associated data. This action cannot be undone.
              All your projects, clips, and settings will be permanently removed.
            </p>
          </div>
        </div>
        <div className="mt-4 flex justify-end">
          <button className="btn-danger">
            <Trash2 className="h-4 w-4" aria-hidden="true" />
            <span>Delete Account</span>
          </button>
        </div>
      </div>

      <div className="p-4 bg-warning/5 border border-warning/20 rounded-xl">
        <div className="flex items-start gap-3">
          <Key className="h-5 w-5 text-warning flex-shrink-0 mt-0.5" aria-hidden="true" />
          <div>
            <h3 className="font-semibold text-warning">Reset All Data</h3>
            <p className="mt-1 text-body-sm text-text-secondary">
              Reset your account to initial state. This will remove all projects and clips but keep your account.
            </p>
          </div>
        </div>
        <div className="mt-4 flex justify-end">
          <button className="btn-outline text-warning border-warning hover:bg-warning/10">
            <Key className="h-4 w-4" aria-hidden="true" />
            <span>Reset Data</span>
          </button>
        </div>
      </div>
    </div>
  );
}

import { clsx } from 'clsx';

const sessions = [
  {
    id: '1',
    device: 'Chrome on macOS',
    location: 'San Francisco, CA',
    lastActive: 'Just now',
    current: true,
    icon: (
      <svg className="h-5 w-5 text-brand-600" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <rect x="2" y="3" width="20" height="14" rx="2" />
        <path d="M8 21h8" />
        <path d="M12 17v4" />
      </svg>
    ),
  },
  {
    id: '2',
    device: 'Safari on iPhone',
    location: 'San Francisco, CA',
    lastActive: '2 hours ago',
    current: false,
    icon: (
      <svg className="h-5 w-5 text-surface-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
        <path d="M12 18h.01" />
      </svg>
    ),
  },
  {
    id: '3',
    device: 'Firefox on Windows',
    location: 'New York, NY',
    lastActive: '3 days ago',
    current: false,
    icon: (
      <svg className="h-5 w-5 text-surface-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" aria-hidden="true">
        <rect x="2" y="3" width="20" height="14" rx="2" />
        <path d="M8 21h8" />
        <path d="M12 17v4" />
      </svg>
    ),
  },
];

function Key({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4" />
    </svg>
  );
}

function Shield({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

function Palette({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="13.5" cy="6.5" r="2.5" />
      <circle cx="18" cy="12" r="2.5" />
      <circle cx="12" cy="18" r="2.5" />
      <circle cx="6" cy="12" r="2.5" />
      <circle cx="12" cy="6.5" r="5" />
    </svg>
  );
}

function Globe({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="12" cy="12" r="10" />
      <line x1="2" y1="12" x2="22" y2="12" />
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
    </svg>
  );
}