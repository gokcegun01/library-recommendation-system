import { useState, useCallback } from 'react';
import { Toast } from '@/components/common/Toast';

interface ToastState {
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  id: number;
}

/**
 * Custom hook for showing toast notifications
 *
 * @example
 * const { showToast, ToastContainer } = useToast();
 * showToast('Book added!', 'success');
 * return <div>{ToastContainer}</div>
 */
export function useToast() {
  const [toasts, setToasts] = useState<ToastState[]>([]);

  const showToast = useCallback(
    (message: string, type: 'success' | 'error' | 'info' | 'warning' = 'success') => {
      const id = Date.now();
      setToasts((prev) => [...prev, { message, type, id }]);
    },
    []
  );

  const removeToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((toast) => toast.id !== id));
  }, []);

  const ToastContainer = (
    <>
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => removeToast(toast.id)}
        />
      ))}
    </>
  );

  return { showToast, ToastContainer };
}
