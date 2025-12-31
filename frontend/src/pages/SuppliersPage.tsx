import { useState } from 'react';
import { MagnifyingGlassIcon, PlusIcon } from '@heroicons/react/24/outline';

const mockSuppliers = [
  { id: '1', name: 'ABC Electronics Ltd', code: 'SUP-001', city: 'Dhaka', country: 'Bangladesh', riskScore: 0.15, reliabilityScore: 0.92, status: 'Active' },
  { id: '2', name: 'XYZ Textiles Corp', code: 'SUP-002', city: 'Chittagong', country: 'Bangladesh', riskScore: 0.45, reliabilityScore: 0.78, status: 'Active' },
  { id: '3', name: 'Global Pharma Inc', code: 'SUP-003', city: 'Singapore', country: 'Singapore', riskScore: 0.08, reliabilityScore: 0.98, status: 'Active' },
  { id: '4', name: 'China Tech Solutions', code: 'SUP-004', city: 'Shenzhen', country: 'China', riskScore: 0.62, reliabilityScore: 0.65, status: 'Under Review' },
  { id: '5', name: 'India Foods Export', code: 'SUP-005', city: 'Mumbai', country: 'India', riskScore: 0.25, reliabilityScore: 0.85, status: 'Active' },
];

export default function SuppliersPage() {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSuppliers = mockSuppliers.filter((supplier) =>
    supplier.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    supplier.code.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getRiskLevel = (score: number) => {
    if (score < 0.3) return { label: 'Low', color: 'text-green-600' };
    if (score < 0.6) return { label: 'Medium', color: 'text-yellow-600' };
    return { label: 'High', color: 'text-red-600' };
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Suppliers</h1>
          <p className="text-gray-500 dark:text-gray-400">Manage supplier relationships and risk assessment</p>
        </div>
        <button className="btn-primary">
          <PlusIcon className="w-5 h-5 mr-2" />
          Add Supplier
        </button>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Total Suppliers</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">48</p>
        </div>
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Active</p>
          <p className="text-2xl font-bold text-green-600">42</p>
        </div>
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">High Risk</p>
          <p className="text-2xl font-bold text-red-600">3</p>
        </div>
        <div className="card p-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">Avg Reliability</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">87.5%</p>
        </div>
      </div>

      {/* Search */}
      <div className="card p-4">
        <div className="relative">
          <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search suppliers..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="input pl-10"
          />
        </div>
      </div>

      {/* Cards grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredSuppliers.map((supplier) => {
          const risk = getRiskLevel(supplier.riskScore);
          return (
            <div key={supplier.id} className="card p-6 hover:shadow-lg transition-shadow">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {supplier.name}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{supplier.code}</p>
                </div>
                <span
                  className={`px-2 py-1 text-xs font-medium rounded-full ${
                    supplier.status === 'Active'
                      ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                      : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                  }`}
                >
                  {supplier.status}
                </span>
              </div>

              <div className="text-sm text-gray-500 dark:text-gray-400 mb-4">
                📍 {supplier.city}, {supplier.country}
              </div>

              <div className="grid grid-cols-2 gap-4 mb-4">
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Risk Score</p>
                  <p className={`text-lg font-semibold ${risk.color}`}>
                    {risk.label} ({(supplier.riskScore * 100).toFixed(0)}%)
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Reliability</p>
                  <p className="text-lg font-semibold text-gray-900 dark:text-white">
                    {(supplier.reliabilityScore * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              <div className="flex space-x-2">
                <button className="btn-secondary flex-1 text-sm py-2">View Details</button>
                <button className="btn-primary flex-1 text-sm py-2">Risk Report</button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
