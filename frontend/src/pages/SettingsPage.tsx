import { useState } from 'react';
import {
  UserCircleIcon,
  BellIcon,
  ShieldCheckIcon,
  PaintBrushIcon,
  KeyIcon,
} from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

export default function SettingsPage() {
  const [activeSection, setActiveSection] = useState('profile');
  const [notifications, setNotifications] = useState({
    email: true,
    push: true,
    anomalyAlerts: true,
    shipmentUpdates: true,
    lowStock: true,
    riskAlerts: false,
  });

  const sections = [
    { id: 'profile', label: 'Profile', icon: UserCircleIcon },
    { id: 'notifications', label: 'Notifications', icon: BellIcon },
    { id: 'security', label: 'Security', icon: ShieldCheckIcon },
    { id: 'appearance', label: 'Appearance', icon: PaintBrushIcon },
    { id: 'api', label: 'API Keys', icon: KeyIcon },
  ];

  const handleSave = () => {
    toast.success('Settings saved successfully!');
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p className="text-gray-500 dark:text-gray-400">Manage your account and preferences</p>
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Sidebar */}
        <div className="lg:w-64 flex-shrink-0">
          <nav className="card p-2 space-y-1">
            {sections.map((section) => (
              <button
                key={section.id}
                onClick={() => setActiveSection(section.id)}
                className={`w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors ${
                  activeSection === section.id
                    ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-200'
                    : 'text-gray-600 hover:bg-gray-100 dark:text-gray-400 dark:hover:bg-gray-800'
                }`}
              >
                <section.icon className="w-5 h-5 mr-3" />
                {section.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="flex-1">
          <div className="card p-6">
            {activeSection === 'profile' && (
              <div className="space-y-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Profile Settings
                </h2>
                <div className="flex items-center space-x-6">
                  <div className="w-20 h-20 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
                    <span className="text-2xl font-bold text-primary-600 dark:text-primary-400">
                      MT
                    </span>
                  </div>
                  <button className="btn-secondary">Change Avatar</button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Full Name
                    </label>
                    <input
                      type="text"
                      defaultValue="Md. Tanvir Hossain"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Email
                    </label>
                    <input
                      type="email"
                      defaultValue="tanvir@example.com"
                      className="input"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Phone
                    </label>
                    <input type="tel" defaultValue="+880 1XXX-XXXXXX" className="input" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Company
                    </label>
                    <input type="text" defaultValue="ChainSense AI" className="input" />
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Bio
                  </label>
                  <textarea
                    rows={3}
                    defaultValue="Supply chain analyst with expertise in ML-powered optimization"
                    className="input"
                  />
                </div>
                <button onClick={handleSave} className="btn-primary">
                  Save Changes
                </button>
              </div>
            )}

            {activeSection === 'notifications' && (
              <div className="space-y-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Notification Preferences
                </h2>
                <div className="space-y-4">
                  {[
                    { key: 'email', label: 'Email Notifications', desc: 'Receive updates via email' },
                    { key: 'push', label: 'Push Notifications', desc: 'Browser push notifications' },
                    {
                      key: 'anomalyAlerts',
                      label: 'Anomaly Alerts',
                      desc: 'Get notified when ML detects anomalies',
                    },
                    {
                      key: 'shipmentUpdates',
                      label: 'Shipment Updates',
                      desc: 'Status changes for tracked shipments',
                    },
                    {
                      key: 'lowStock',
                      label: 'Low Stock Warnings',
                      desc: 'Alerts when inventory is running low',
                    },
                    {
                      key: 'riskAlerts',
                      label: 'Supplier Risk Alerts',
                      desc: 'Notifications for high-risk supplier events',
                    },
                  ].map((item) => (
                    <div
                      key={item.key}
                      className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg"
                    >
                      <div>
                        <p className="font-medium text-gray-900 dark:text-white">{item.label}</p>
                        <p className="text-sm text-gray-500 dark:text-gray-400">{item.desc}</p>
                      </div>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={notifications[item.key as keyof typeof notifications]}
                          onChange={(e) =>
                            setNotifications({
                              ...notifications,
                              [item.key]: e.target.checked,
                            })
                          }
                          className="sr-only peer"
                        />
                        <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full rtl:peer-checked:after:-translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
                      </label>
                    </div>
                  ))}
                </div>
                <button onClick={handleSave} className="btn-primary">
                  Save Preferences
                </button>
              </div>
            )}

            {activeSection === 'security' && (
              <div className="space-y-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Security Settings
                </h2>
                <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="flex items-center">
                    <ShieldCheckIcon className="w-6 h-6 text-green-600 mr-3" />
                    <div>
                      <p className="font-medium text-green-800 dark:text-green-200">
                        Two-Factor Authentication Enabled
                      </p>
                      <p className="text-sm text-green-600 dark:text-green-300">
                        Your account is protected with 2FA
                      </p>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Current Password
                    </label>
                    <input type="password" className="input" placeholder="••••••••" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      New Password
                    </label>
                    <input type="password" className="input" placeholder="••••••••" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                      Confirm New Password
                    </label>
                    <input type="password" className="input" placeholder="••••••••" />
                  </div>
                </div>
                <button onClick={handleSave} className="btn-primary">
                  Update Password
                </button>
              </div>
            )}

            {activeSection === 'appearance' && (
              <div className="space-y-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Appearance Settings
                </h2>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                    Theme
                  </label>
                  <div className="grid grid-cols-3 gap-4">
                    {['Light', 'Dark', 'System'].map((theme) => (
                      <button
                        key={theme}
                        className={`p-4 border-2 rounded-lg text-center transition-colors ${
                          theme === 'System'
                            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20'
                            : 'border-gray-200 dark:border-gray-700 hover:border-primary-300'
                        }`}
                      >
                        <p className="font-medium text-gray-900 dark:text-white">{theme}</p>
                      </button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-4">
                    Dashboard Layout
                  </label>
                  <select className="input">
                    <option>Compact</option>
                    <option>Comfortable</option>
                    <option>Spacious</option>
                  </select>
                </div>
              </div>
            )}

            {activeSection === 'api' && (
              <div className="space-y-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">API Keys</h2>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Manage your API keys for programmatic access to ChainSense AI
                </p>
                <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                  <p className="text-sm text-yellow-800 dark:text-yellow-200">
                    ⚠️ Keep your API keys secure. Never share them publicly or commit them to
                    version control.
                  </p>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">Production Key</p>
                      <p className="text-sm font-mono text-gray-500 dark:text-gray-400">
                        cs_live_••••••••••••••••
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <button className="btn-secondary text-sm">Copy</button>
                      <button className="text-red-600 hover:text-red-700 text-sm font-medium">
                        Revoke
                      </button>
                    </div>
                  </div>
                  <div className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">Development Key</p>
                      <p className="text-sm font-mono text-gray-500 dark:text-gray-400">
                        cs_test_••••••••••••••••
                      </p>
                    </div>
                    <div className="flex space-x-2">
                      <button className="btn-secondary text-sm">Copy</button>
                      <button className="text-red-600 hover:text-red-700 text-sm font-medium">
                        Revoke
                      </button>
                    </div>
                  </div>
                </div>
                <button className="btn-primary">Generate New Key</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
