import axios from 'axios';
import { useAuthStore } from '../store/authStore';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const { accessToken } = useAuthStore.getState();
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const { refreshToken, logout } = useAuthStore.getState();
      
      if (refreshToken) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: refreshToken,
          });
          
          const { access_token, refresh_token } = response.data;
          useAuthStore.getState().login(
            useAuthStore.getState().user!,
            access_token,
            refresh_token
          );
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        } catch {
          logout();
        }
      } else {
        logout();
      }
    }
    
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: async (email: string, password: string) => {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post('/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  register: async (data: { email: string; username: string; password: string; full_name?: string }) => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },
  
  getMe: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

// Inventory API
export const inventoryAPI = {
  list: async (params?: { page?: number; size?: number; low_stock?: boolean }) => {
    const response = await api.get('/inventory', { params });
    return response.data;
  },
  
  getSummary: async () => {
    const response = await api.get('/inventory/summary/overview');
    return response.data;
  },
  
  create: async (data: any) => {
    const response = await api.post('/inventory', data);
    return response.data;
  },
  
  update: async (id: string, data: any) => {
    const response = await api.patch(`/inventory/${id}`, data);
    return response.data;
  },
};

// Shipments API
export const shipmentsAPI = {
  list: async (params?: { page?: number; size?: number; status?: string }) => {
    const response = await api.get('/shipments', { params });
    return response.data;
  },
  
  get: async (id: string) => {
    const response = await api.get(`/shipments/${id}`);
    return response.data;
  },
  
  track: async (trackingNumber: string) => {
    const response = await api.get(`/shipments/track/${trackingNumber}`);
    return response.data;
  },
  
  create: async (data: any) => {
    const response = await api.post('/shipments', data);
    return response.data;
  },
  
  updateStatus: async (id: string, status: string) => {
    const response = await api.post(`/shipments/${id}/status?new_status=${status}`);
    return response.data;
  },
  
  getSummary: async () => {
    const response = await api.get('/shipments/summary/overview');
    return response.data;
  },
};

// Suppliers API
export const suppliersAPI = {
  list: async (params?: { page?: number; size?: number; search?: string }) => {
    const response = await api.get('/suppliers', { params });
    return response.data;
  },
  
  get: async (id: string) => {
    const response = await api.get(`/suppliers/${id}`);
    return response.data;
  },
  
  getRiskAssessment: async (id: string) => {
    const response = await api.get(`/suppliers/${id}/risk-assessment`);
    return response.data;
  },
  
  create: async (data: any) => {
    const response = await api.post('/suppliers', data);
    return response.data;
  },
  
  update: async (id: string, data: any) => {
    const response = await api.patch(`/suppliers/${id}`, data);
    return response.data;
  },
};

// Analytics API
export const analyticsAPI = {
  getDashboardKPIs: async () => {
    const response = await api.get('/analytics/dashboard/kpis');
    return response.data;
  },
  
  getDemandForecast: async (productId: string, days: number = 30) => {
    const response = await api.post('/analytics/demand/forecast', {
      product_id: productId,
      forecast_days: days,
    });
    return response.data;
  },
  
  getAnomalies: async (params?: { severity?: string; is_acknowledged?: boolean }) => {
    const response = await api.get('/analytics/anomalies', { params });
    return response.data;
  },
  
  acknowledgeAnomaly: async (id: string) => {
    const response = await api.post(`/analytics/anomalies/${id}/acknowledge`);
    return response.data;
  },
  
  optimizeRoute: async (data: {
    origin: { latitude: number; longitude: number };
    destination: { latitude: number; longitude: number };
    waypoints?: Array<{ latitude: number; longitude: number }>;
  }) => {
    const response = await api.post('/analytics/routes/optimize', data);
    return response.data;
  },
  
  getSupplyChainHealth: async (days: number = 30) => {
    const response = await api.get('/analytics/reports/supply-chain-health', {
      params: { time_range_days: days },
    });
    return response.data;
  },
};
