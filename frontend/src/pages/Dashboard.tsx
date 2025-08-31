import React from 'react';
import { useAuth } from '@/contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import Header from '@/components/Header';
import EvacuationTestPanel from '@/components/EvacuationTestPanel';
import { Shield, User, MapPin, Calendar, Target } from 'lucide-react';

const Dashboard: React.FC = () => {
  const { user, signOut } = useAuth();

  const handleLogout = async () => {
    await signOut();
  };

  if (!user) {
    return <div>Loading...</div>;
  }

  const userRole = user.user_metadata?.role || 'community';
  const userName = user.user_metadata?.full_name || user.email;

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* User Profile Card */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <User className="h-5 w-5" />
                Profile
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Name:</span>
                <span className="font-medium">{userName}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Email:</span>
                <span className="font-medium">{user.email}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">Role:</span>
                <Badge variant="secondary" className="capitalize">
                  {userRole}
                </Badge>
              </div>
              <Button 
                variant="outline" 
                onClick={handleLogout}
                className="w-full"
              >
                Sign Out
              </Button>
            </CardContent>
          </Card>

          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Welcome Card */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Shield className="h-5 w-5 text-primary" />
                  Welcome to CTAS
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Welcome back, {userName}! You are logged in as a {userRole} member.
                </p>
              </CardContent>
            </Card>

            {/* Role-based Content */}
            {userRole === 'admin' && (
              <>
                <Card>
                  <CardHeader>
                    <CardTitle>Admin Dashboard</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p>Admin features coming soon...</p>
                  </CardContent>
                </Card>
                
                <EvacuationTestPanel />
              </>
            )}

            {userRole === 'authority' && (
              <Card>
                <CardHeader>
                  <CardTitle>Authority Dashboard</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Authority features coming soon...</p>
                </CardContent>
              </Card>
            )}

            {userRole === 'community' && (
              <Card>
                <CardHeader>
                  <CardTitle>Community Dashboard</CardTitle>
                </CardHeader>
                <CardContent>
                  <p>Community features coming soon...</p>
                </CardContent>
              </Card>
            )}

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle>Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Button variant="outline" className="h-20 flex flex-col gap-2">
                  <Target className="h-6 w-6" />
                  <span>View Mock Drills</span>
                </Button>
                <Button variant="outline" className="h-20 flex flex-col gap-2">
                  <MapPin className="h-6 w-6" />
                  <span>Check Alerts</span>
                </Button>
                <Button variant="outline" className="h-20 flex flex-col gap-2">
                  <Calendar className="h-6 w-6" />
                  <span>Schedule</span>
                </Button>
                <Button variant="outline" className="h-20 flex flex-col gap-2">
                  <Shield className="h-6 w-6" />
                  <span>Safety Tips</span>
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
