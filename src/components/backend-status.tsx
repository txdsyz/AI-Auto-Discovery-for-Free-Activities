'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';
import { AlertCircle, CheckCircle, XCircle } from 'lucide-react';

export function BackendStatus() {
  const [status, setStatus] = useState<'checking' | 'connected' | 'disconnected'>('checking');

  useEffect(() => {
    checkBackend();
  }, []);

  const checkBackend = async () => {
    try {
      await api.healthCheck();
      setStatus('connected');
    } catch (error) {
      setStatus('disconnected');
    }
  };

  if (status === 'checking') {
    return null;
  }

  if (status === 'connected') {
    return (
      <div className="bg-green-50 border-b border-green-200 px-6 py-2">
        <div className="flex items-center gap-2 text-sm text-green-800">
          <CheckCircle className="h-4 w-4" />
          <span>Connected to backend API</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-yellow-50 border-b border-yellow-200 px-6 py-2">
      <div className="flex items-center gap-2 text-sm text-yellow-800">
        <AlertCircle className="h-4 w-4" />
        <span>Backend not running - Using mock data. Start backend with: <code className="bg-yellow-100 px-1 rounded">cd backend && python main.py</code></span>
      </div>
    </div>
  );
}
