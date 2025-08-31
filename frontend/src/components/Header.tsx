import React, { useState } from 'react';
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { 
  Menu, 
  X, 
  User, 
  LogOut, 
  Settings, 
  Home, 
  BarChart3, 
  Navigation,
  Bell,
  ChevronDown,
  MessageSquare
} from "lucide-react";
import NotificationDropdown from './NotificationDropdown';

const Header = () => {
  const { user, signOut } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const handleSignOut = async () => {
    await signOut();
    navigate('/');
  };

  return (
    <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50 shadow-sm">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center gap-3">
            <div 
              className="flex items-center gap-2 cursor-pointer group"
              onClick={() => navigate('/')}
            >
              <div className="p-2 rounded-lg bg-gradient-to-r from-blue-600 to-purple-600 group-hover:scale-110 transition-transform duration-200">
                <Navigation className="h-6 w-6 text-white" />
              </div>
              <div className="hidden sm:block">
                <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  CTAS
                </h1>
                <p className="text-xs text-slate-500 -mt-1">Coastal Threat Alert System</p>
              </div>
            </div>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-6">
            <Button
              variant="ghost"
              className="text-slate-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              onClick={() => navigate('/')}
            >
              <Home className="h-4 w-4 mr-2" />
              Home
            </Button>
            <Button
              variant="ghost"
              className="text-slate-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              onClick={() => navigate('/quiz')}
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              Quiz
            </Button>
            <Button
              variant="ghost"
              className="text-slate-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              onClick={() => navigate('/navigation')}
            >
              <Navigation className="h-4 w-4 mr-2" />
              Navigation
            </Button>
            <Button
              variant="ghost"
              className="text-slate-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              onClick={() => navigate('/reports')}
            >
              <BarChart3 className="h-4 w-4 mr-2" />
              Reports
            </Button>
            <Button
              variant="ghost"
              className="text-slate-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
              onClick={() => navigate('/sms-alerts')}
            >
              <MessageSquare className="h-4 w-4 mr-2" />
              SMS Alerts
            </Button>
          </nav>

          {/* Right Side - User Info and Actions */}
          <div className="flex items-center gap-4">
            {/* Notifications */}
            <NotificationDropdown />

            {/* User Menu */}
            {user ? (
              <div className="flex items-center gap-3">
                <div className="hidden sm:flex items-center gap-2 text-right">
                  <div>
                    <p className="text-sm font-medium text-slate-800">{user.full_name}</p>
                    <p className="text-xs text-slate-500">{user.email}</p>
                  </div>
                </div>
                
                <div className="relative group">
                  <Button
                    variant="ghost"
                    className="flex items-center gap-2 hover:bg-slate-100 rounded-full p-2"
                  >
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 flex items-center justify-center">
                      <User className="h-4 w-4 text-white" />
                    </div>
                    <ChevronDown className="h-4 w-4 text-slate-600 group-hover:text-blue-600 transition-colors" />
                  </Button>
                  
                  {/* Dropdown Menu */}
                  <div className="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-slate-200 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-50">
                    <div className="py-2">
                      <div className="px-4 py-2 border-b border-slate-100">
                        <p className="text-sm font-medium text-slate-800">{user.full_name}</p>
                        <p className="text-xs text-slate-500">{user.email}</p>
                      </div>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                        onClick={() => navigate('/dashboard')}
                      >
                        <Home className="h-4 w-4 mr-2" />
                        Dashboard
                      </Button>
                      <Button
                        variant="ghost"
                        className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                        onClick={() => navigate('/settings')}
                      >
                        <Settings className="h-4 w-4 mr-2" />
                        Settings
                      </Button>
                      <div className="border-t border-slate-100 mt-2 pt-2">
                        <Button
                          variant="ghost"
                          className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50"
                          onClick={handleSignOut}
                        >
                          <LogOut className="h-4 w-4 mr-2" />
                          Sign Out
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Button
                  variant="ghost"
                  className="text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                  onClick={() => navigate('/login')}
                >
                  Login
                </Button>
                <Button
                  className="bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg transition-all duration-200 hover:scale-105"
                  onClick={() => navigate('/register')}
                >
                  Sign Up
                </Button>
              </div>
            )}

            {/* Mobile Menu Button */}
            <Button
              variant="ghost"
              className="md:hidden p-2"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-slate-200 bg-white/95 backdrop-blur-md">
            <div className="py-4 space-y-2">
              <Button
                variant="ghost"
                className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                onClick={() => {
                  navigate('/');
                  setIsMobileMenuOpen(false);
                }}
              >
                <Home className="h-4 w-4 mr-2" />
                Home
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                onClick={() => {
                  navigate('/quiz');
                  setIsMobileMenuOpen(false);
                }}
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Quiz
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                onClick={() => {
                  navigate('/navigation');
                  setIsMobileMenuOpen(false);
                }}
              >
                <Navigation className="h-4 w-4 mr-2" />
                Navigation
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                onClick={() => {
                  navigate('/reports');
                  setIsMobileMenuOpen(false);
                }}
              >
                <BarChart3 className="h-4 w-4 mr-2" />
                Reports
              </Button>
              <Button
                variant="ghost"
                className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                onClick={() => {
                  navigate('/sms-alerts');
                  setIsMobileMenuOpen(false);
                }}
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                SMS Alerts
              </Button>
              
              {user && (
                <>
                  <div className="border-t border-slate-200 pt-2 mt-2">
                    <div className="px-4 py-2">
                      <p className="text-sm font-medium text-slate-800">{user.full_name}</p>
                      <p className="text-xs text-slate-500">{user.email}</p>
                    </div>
                    <Button
                      variant="ghost"
                      className="w-full justify-start text-slate-700 hover:text-blue-600 hover:bg-blue-50"
                      onClick={() => {
                        navigate('/dashboard');
                        setIsMobileMenuOpen(false);
                      }}
                    >
                      <Home className="h-4 w-4 mr-2" />
                      Dashboard
                    </Button>
                    <Button
                      variant="ghost"
                      className="w-full justify-start text-red-600 hover:text-red-700 hover:bg-red-50"
                      onClick={() => {
                        handleSignOut();
                        setIsMobileMenuOpen(false);
                      }}
                    >
                      <LogOut className="h-4 w-4 mr-2" />
                      Sign Out
                    </Button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;