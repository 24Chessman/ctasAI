import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./contexts/AuthContext";
import { NotificationProvider } from "./contexts/NotificationContext";
import ErrorBoundary from "./components/ErrorBoundary";
import Index from "./pages/Index";
import TestComponent from "./components/TestComponent";
import NotFound from "./pages/NotFound";
import LoginPage from "./components/auth/LoginPage";
import RegistrationPage from "./components/auth/RegistrationPage";
import ForgotPasswordPage from "./components/auth/ForgotPasswordPage";
import LiveAlerts from "./pages/LiveAlerts";
import MockDrillsPage from "./pages/MockDrillPage";
import Dashboard from "./pages/Dashboard";
import QuizPage from "./pages/QuizPage";
import NavigationPage from "./pages/Navigation";
import ReportsPage from "./pages/Reports";
import SMSAlerts from "./pages/SMSAlerts";

const queryClient = new QueryClient();

const App = () => (
  <ErrorBoundary>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <NotificationProvider>
          <TooltipProvider>
            <Toaster />
            <Sonner />
            <BrowserRouter>
              <Routes>
                <Route path="/" element={<Index />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegistrationPage />} />
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/live-alerts" element={<LiveAlerts />} />
                <Route path="/mock-drills" element={<MockDrillsPage />} />
                <Route path="/quiz" element={<QuizPage />} />
                <Route path="/navigation" element={<NavigationPage />} />
                <Route path="/reports" element={<ReportsPage />} />
                <Route path="/sms-alerts" element={<SMSAlerts />} />

                {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
                <Route path="*" element={<NotFound />} />
              </Routes>
            </BrowserRouter>
          </TooltipProvider>
        </NotificationProvider>
      </AuthProvider>
    </QueryClientProvider>
  </ErrorBoundary>
);

export default App;