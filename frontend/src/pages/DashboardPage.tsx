import {
  CubeIcon,
  TruckIcon,
  ExclamationTriangleIcon,
  ChartBarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

// Mock data for charts
const demandData = [
  { date: 'Mon', actual: 120, predicted: 115 },
  { date: 'Tue', actual: 132, predicted: 128 },
  { date: 'Wed', actual: 101, predicted: 108 },
  { date: 'Thu', actual: 134, predicted: 130 },
  { date: 'Fri', actual: 190, predicted: 180 },
  { date: 'Sat', actual: 230, predicted: 220 },
  { date: 'Sun', actual: 210, predicted: 205 },
];

const inventoryData = [
  { name: 'Electronics', value: 4000, color: '#3b82f6' },
  { name: 'Apparel', value: 3000, color: '#22c55e' },
  { name: 'Food & Beverage', value: 2000, color: '#f59e0b' },
  { name: 'Healthcare', value: 2780, color: '#ef4444' },
  { name: 'Others', value: 1890, color: '#8b5cf6' },
];

const shipmentData = [
  { month: 'Jan', inbound: 65, outbound: 45 },
  { month: 'Feb', inbound: 59, outbound: 52 },
  { month: 'Mar', inbound: 80, outbound: 68 },
  { month: 'Apr', inbound: 81, outbound: 75 },
  { month: 'May', inbound: 56, outbound: 48 },
  { month: 'Jun', inbound: 55, outbound: 42 },
];

const stats = [
  {
    name: 'Total Inventory',
    value: '12,450',
    change: '+12.5%',
    changeType: 'increase',
    icon: CubeIcon,
    color: 'bg-blue-500',
  },
  {
    name: 'Active Shipments',
    value: '89',
    change: '+4.3%',
    changeType: 'increase',
    icon: TruckIcon,
    color: 'bg-green-500',
  },
  {
    name: 'Anomaly Alerts',
    value: '7',
    change: '-2',
    changeType: 'decrease',
    icon: ExclamationTriangleIcon,
    color: 'bg-yellow-500',
  },
  {
    name: 'Forecast Accuracy',
    value: '94.2%',
    change: '+1.8%',
    changeType: 'increase',
    icon: ChartBarIcon,
    color: 'bg-purple-500',
  },
];

const recentAlerts = [
  { id: 1, type: 'Demand Spike', product: 'SKU-12345', severity: 'high', time: '2 hours ago' },
  { id: 2, type: 'Low Stock', product: 'SKU-67890', severity: 'medium', time: '4 hours ago' },
  { id: 3, type: 'Delivery Delay', shipment: 'CS20251231ABC', severity: 'low', time: '6 hours ago' },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-500 dark:text-gray-400">
          Overview of your supply chain intelligence
        </p>
      </div>

      {/* Stats grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div key={stat.name} className="stat-card">
            <div className="flex items-center justify-between">
              <div className={`${stat.color} p-3 rounded-lg`}>
                <stat.icon className="w-6 h-6 text-white" />
              </div>
              <span
                className={`flex items-center text-sm font-medium ${
                  stat.changeType === 'increase' ? 'text-green-600' : 'text-red-600'
                }`}
              >
                {stat.changeType === 'increase' ? (
                  <ArrowTrendingUpIcon className="w-4 h-4 mr-1" />
                ) : (
                  <ArrowTrendingDownIcon className="w-4 h-4 mr-1" />
                )}
                {stat.change}
              </span>
            </div>
            <div className="mt-4">
              <h3 className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400">{stat.name}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Demand Forecast Chart */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Demand Forecast vs Actual
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={demandData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
                <XAxis dataKey="date" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="predicted"
                  stroke="#3b82f6"
                  fill="#3b82f6"
                  fillOpacity={0.2}
                  strokeWidth={2}
                  name="Predicted"
                />
                <Area
                  type="monotone"
                  dataKey="actual"
                  stroke="#22c55e"
                  fill="#22c55e"
                  fillOpacity={0.2}
                  strokeWidth={2}
                  name="Actual"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Inventory Distribution */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Inventory Distribution by Category
          </h3>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={inventoryData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {inventoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Shipments and Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Shipment Trends */}
        <div className="card p-6 lg:col-span-2">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Shipment Trends
          </h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={shipmentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.2} />
                <XAxis dataKey="month" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="inbound" fill="#3b82f6" name="Inbound" radius={[4, 4, 0, 0]} />
                <Bar dataKey="outbound" fill="#22c55e" name="Outbound" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Alerts */}
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            Recent Alerts
          </h3>
          <div className="space-y-4">
            {recentAlerts.map((alert) => (
              <div
                key={alert.id}
                className="flex items-start space-x-3 p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50"
              >
                <div
                  className={`w-2 h-2 mt-2 rounded-full flex-shrink-0 ${
                    alert.severity === 'high'
                      ? 'bg-red-500'
                      : alert.severity === 'medium'
                      ? 'bg-yellow-500'
                      : 'bg-green-500'
                  }`}
                />
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-white">
                    {alert.type}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate">
                    {alert.product || alert.shipment}
                  </p>
                  <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
          <button className="w-full mt-4 text-sm text-primary-600 hover:text-primary-500 font-medium">
            View all alerts →
          </button>
        </div>
      </div>

      {/* Supply Chain Health Score */}
      <div className="card p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Supply Chain Health Score
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Based on real-time metrics and ML analysis
            </p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-bold text-green-500">87.5</div>
            <div className="text-sm text-gray-500">out of 100</div>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {[
            { name: 'Inventory Accuracy', value: 98.2 },
            { name: 'Order Fulfillment', value: 96.5 },
            { name: 'On-Time Delivery', value: 93.8 },
            { name: 'Supplier Quality', value: 91.2 },
            { name: 'Forecast Accuracy', value: 87.5 },
          ].map((metric) => (
            <div key={metric.name} className="text-center">
              <div className="text-2xl font-semibold text-gray-900 dark:text-white">
                {metric.value}%
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400">{metric.name}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
