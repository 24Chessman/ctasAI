import React from 'react';

const TestComponent: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          CTAS App is Working! 🎉
        </h1>
        <p className="text-gray-600 mb-4">
          The application is loading successfully. If you can see this, the basic setup is working.
        </p>
        <div className="space-y-2">
          <p className="text-sm text-gray-500">
            • React is working ✓
          </p>
          <p className="text-sm text-gray-500">
            • Tailwind CSS is working ✓
          </p>
          <p className="text-sm text-gray-500">
            • TypeScript is working ✓
          </p>
        </div>
      </div>
    </div>
  );
};

export default TestComponent;
