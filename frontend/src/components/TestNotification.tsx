import React from 'react';
import { Button } from '@/components/ui/button';
import { useNotifications } from '@/contexts/NotificationContext';

const TestNotification = () => {
  const { addNotification } = useNotifications();

  const addTestNotification = (type: 'info' | 'warning' | 'error' | 'success') => {
    const messages = {
      info: {
        title: 'System Update',
        message: 'A new system update is available. Please check the latest features.',
        priority: 'low' as const
      },
      warning: {
        title: 'Weather Alert',
        message: 'High winds detected in coastal areas. Please take necessary precautions.',
        priority: 'medium' as const
      },
      error: {
        title: 'System Error',
        message: 'Critical system error detected. Emergency protocols activated.',
        priority: 'high' as const
      },
      success: {
        title: 'Alert Resolved',
        message: 'Previous storm warning has been resolved. All systems operational.',
        priority: 'low' as const
      }
    };

    addNotification({
      ...messages[type],
      type
    });
  };

  return (
    <div className="p-4 space-y-4">
      <h3 className="text-lg font-semibold">Test Notifications</h3>
      <div className="flex flex-wrap gap-2">
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => addTestNotification('info')}
        >
          Add Info
        </Button>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => addTestNotification('warning')}
        >
          Add Warning
        </Button>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => addTestNotification('error')}
        >
          Add Error
        </Button>
        <Button 
          variant="outline" 
          size="sm" 
          onClick={() => addTestNotification('success')}
        >
          Add Success
        </Button>
      </div>
    </div>
  );
};

export default TestNotification;
