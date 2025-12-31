import { useState } from 'react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
} from 'recharts';
import {
  ArrowTrendingUpIcon,
  ExclamationTriangleIcon,
  SparklesIcon,
  CpuChipIcon,
} from '@heroicons/react/24/outline';

const demandForecastData = [
  { month: 'Jan', actual: 4200, predicted: 4100, lower: 3800, upper: 4400 },
  { month: 'Feb', actual: 3800, predicted: 3900, lower: 3600, upper: 4200 },
  { month: 'Mar', actual: 5100, predicted: 4800, lower: 4500, upper: 5100 },
  { month: 'Apr', actual: 4600, predicted: 4700, lower: 4400, upper: 5000 },
  { month: 'May', actual: 5400, predicted: 5200, lower: 4900, upper: 5500 },
  { month: 'Jun', actual: null, predicted: 5600, lower: 5200, upper: 6000 },
  { month: 'Jul', actual: null, predicted: 5900, lower: 5400, upper: 6400 },
  { month: 'Aug', actual: null, predicted: 6200, lower: 5700, upper: 6700 },
];

const anomalyData = [
  { date: '2024-01-01', value: 98, anomaly: false },
  { date: '2024-01-02', value: 102, anomaly: false },
  { date: '2024-01-03', value: 97, anomaly: false },
  { date: '2024-01-04', value: 145, anomaly: true },
  { date: '2024-01-05', value: 103, anomaly: false },
  { date: '2024-01-06', value: 99, anomaly: false },
  { date: '2024-01-07', value: 95, anomaly: false },
  { date: '2024-01-08', value: 52, anomaly: true },
  { date: '2024-01-09', value: 101, anomaly: false },
  { date: '2024-01-10', value: 98, anomaly: false },
];

const supplierRiskRadar = [
  { metric: 'Financial', score: 85 },
  { metric: 'Delivery', score: 92 },
  { metric: 'Quality', score: 78 },
  { metric: 'Compliance', score: 95 },
  { metric: 'Geopolitical', score: 65 },
  { metric: 'Operational', score: 88 },
];

const routeOptimizationData = [
  { route: 'Route A', original: 450, optimized: 380 },
  { route: 'Route B', original: 320, optimized: 290 },
  { route: 'Route C', original: 580, optimized: 420 },
  { route: 'Route D', original: 410, optimized: 355 },
  { route: 'Route E', original: 290, optimized: 265 },
];

export default function AnalyticsPage() {
  const [activeTab, setActiveTab] = useState<'forecast' | 'anomaly' | 'risk' | 'route'>('forecast');

  const tabs = [
    { id: 'forecast', label: 'Demand Forecast', icon: ArrowTrendingUpIcon },
    { id: 'anomaly', label: 'Anomaly Detection', icon: ExclamationTriangleIcon },
    { id: 'risk', label: 'Risk Analysis', icon: SparklesIcon },
    { id: 'route', label: 'Route Optimization', icon: CpuChipIcon },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">AI Analytics</h1>
        <p className="text-gray-500 dark:text-gray-400">
          ML-powered insights for supply chain optimization
        </p>
      </div>

      {/* Model metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Forecast Accuracy</p>
          <p className="text-2xl font-bold text-green-600">94.2%</p>
          <p className="text-xs text-gray-400">LSTM + Random Forest</p>
        </div>
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Anomalies Detected</p>
          <p className="text-2xl font-bold text-yellow-600">12</p>
          <p className="text-xs text-gray-400">Isolation Forest</p>
        </div>
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Route Savings</p>
          <p className="text-2xl font-bold text-blue-600">18.5%</p>
          <p className="text-xs text-gray-400">Graph Neural Network</p>
        </div>
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Risk Alerts</p>
          <p className="text-2xl font-bold text-red-600">3</p>
          <p className="text-xs text-gray-400">Multi-factor Analysis</p>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`flex items-center py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-600 dark:text-primary-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400'
              }`}
            >
              <tab.icon className="w-5 h-5 mr-2" />
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab content */}
      <div className="card p-6">
        {activeTab === 'forecast' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Demand Forecast with Confidence Intervals
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                LSTM neural network combined with Random Forest ensemble for accurate predictions
              </p>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <AreaChart data={demandForecastData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area
                  type="monotone"
                  dataKey="upper"
                  stackId="1"
                  stroke="none"
                  fill="#93c5fd"
                  fillOpacity={0.3}
                  name="Upper Bound"
                />
                <Area
                  type="monotone"
                  dataKey="lower"
                  stackId="2"
                  stroke="none"
                  fill="#ffffff"
                  name="Lower Bound"
                />
                <Line
                  type="monotone"
                  dataKey="predicted"
                  stroke="#3b82f6"
                  strokeWidth={2}
                  name="Predicted"
                />
                <Line
                  type="monotone"
                  dataKey="actual"
                  stroke="#10b981"
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  name="Actual"
                />
              </AreaChart>
            </ResponsiveContainer>
            <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                <strong>AI Insight:</strong> Demand is projected to increase by 15% over the next quarter.
                Consider increasing inventory levels for high-demand products by early June.
              </p>
            </div>
          </div>
        )}

        {activeTab === 'anomaly' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Anomaly Detection in Supply Chain Metrics
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Isolation Forest algorithm detecting unusual patterns in real-time
              </p>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={anomalyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line
                  type="monotone"
                  dataKey="value"
                  stroke="#6366f1"
                  strokeWidth={2}
                  dot={(props) => {
                    const { cx, cy, payload } = props;
                    if (payload.anomaly) {
                      return (
                        <circle
                          cx={cx}
                          cy={cy}
                          r={8}
                          fill="#ef4444"
                          stroke="#fff"
                          strokeWidth={2}
                        />
                      );
                    }
                    return <circle cx={cx} cy={cy} r={4} fill="#6366f1" />;
                  }}
                />
              </LineChart>
            </ResponsiveContainer>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
                <p className="font-medium text-red-800 dark:text-red-200">Anomaly Detected: Jan 4</p>
                <p className="text-sm text-red-600 dark:text-red-300">
                  Unusual spike in shipment volume (45% above normal). Possible causes: bulk order,
                  data entry error, or supply surge.
                </p>
              </div>
              <div className="bg-red-50 dark:bg-red-900/20 p-4 rounded-lg">
                <p className="font-medium text-red-800 dark:text-red-200">Anomaly Detected: Jan 8</p>
                <p className="text-sm text-red-600 dark:text-red-300">
                  Significant drop in inventory levels (48% below normal). Possible causes:
                  stockout, theft, or system error.
                </p>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'risk' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Supplier Risk Assessment
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Multi-dimensional risk analysis using ML classification models
              </p>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ResponsiveContainer width="100%" height={350}>
                <RadarChart data={supplierRiskRadar}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="metric" />
                  <PolarRadiusAxis angle={30} domain={[0, 100]} />
                  <Radar
                    name="Risk Score"
                    dataKey="score"
                    stroke="#8b5cf6"
                    fill="#8b5cf6"
                    fillOpacity={0.5}
                  />
                </RadarChart>
              </ResponsiveContainer>
              <div className="space-y-4">
                <h4 className="font-medium text-gray-900 dark:text-white">Risk Breakdown</h4>
                {supplierRiskRadar.map((item) => (
                  <div key={item.metric} className="flex items-center justify-between">
                    <span className="text-sm text-gray-600 dark:text-gray-400">{item.metric}</span>
                    <div className="flex items-center space-x-3">
                      <div className="w-32 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${
                            item.score >= 80
                              ? 'bg-green-500'
                              : item.score >= 60
                              ? 'bg-yellow-500'
                              : 'bg-red-500'
                          }`}
                          style={{ width: `${item.score}%` }}
                        />
                      </div>
                      <span className="text-sm font-medium text-gray-900 dark:text-white w-12">
                        {item.score}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'route' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                Route Optimization Results
              </h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Graph Neural Network with OR-Tools for optimal delivery routes
              </p>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={routeOptimizationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="route" />
                <YAxis label={{ value: 'Distance (km)', angle: -90, position: 'insideLeft' }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="original" name="Original Distance" fill="#94a3b8" />
                <Bar dataKey="optimized" name="Optimized Distance" fill="#22c55e" />
              </BarChart>
            </ResponsiveContainer>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
                <p className="text-2xl font-bold text-green-600">18.5%</p>
                <p className="text-sm text-green-800 dark:text-green-200">Distance Reduction</p>
              </div>
              <div className="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
                <p className="text-2xl font-bold text-blue-600">৳45,000</p>
                <p className="text-sm text-blue-800 dark:text-blue-200">Monthly Fuel Savings</p>
              </div>
              <div className="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
                <p className="text-2xl font-bold text-purple-600">12 hrs</p>
                <p className="text-sm text-purple-800 dark:text-purple-200">Time Saved Daily</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
