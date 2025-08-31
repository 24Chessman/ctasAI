import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";
import StatsCard from "@/components/StatsCard";
import AlertCard from "@/components/AlertCard";
import MockDrillCard from "@/components/MockDrillCard";
import WeatherCard from "@/components/WeatherCard";
import heroImage from "@/assets/vue.svg";
import { 
  Shield, 
  AlertTriangle, 
  Users, 
  Target, 
  MapPin, 
  Activity,
  Waves,
  Radio,
  Camera,
  Navigation,
  Brain
} from "lucide-react";

const Index = () => {
  const [selectedRole, setSelectedRole] = useState<"admin" | "authority" | "community">("admin");
  const navigate = useNavigate();

  const handleViewLiveAlerts = () => {
    navigate('/live-alerts');
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="relative h-96 bg-gradient-to-r from-primary/90 to-secondary/90 flex items-center justify-center text-center overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat opacity-20"
          style={{ backgroundImage: `url(${heroImage})` }}
        />
        <div className="relative z-10 max-w-4xl mx-auto px-4">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Shield className="h-12 w-12 text-white" />
            <h1 className="text-5xl font-bold text-white">CTAS</h1>
          </div>
          <h2 className="text-2xl font-semibold text-white/90 mb-4">
            Coastal Threat Alert System
          </h2>
          <p className="text-lg text-white/80 mb-8 max-w-2xl mx-auto">
            Advanced coastal monitoring, emergency response coordination, and community safety management platform
          </p>
          <div className="flex gap-4 justify-center">
            <Button size="lg" variant="secondary">
              Emergency Dashboard
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="bg-white/10 border-white/30 text-white hover:bg-white/20"
              onClick={handleViewLiveAlerts}
            >
              View Live Alerts
            </Button>
            <Button 
              size="lg" 
              variant="outline" 
              className="bg-white/10 border-white/30 text-white hover:bg-white/20"
              onClick={() => navigate('/quiz')}
            >
              <Brain className="h-5 w-5 mr-2" />
              Take Safety Quiz
            </Button>
          </div>
        </div>
      </section>

      {/* Role Selection */}
      <section className="py-8 bg-card border-b">
        <div className="container mx-auto px-4">
          <div className="flex justify-center gap-4">
            <Button 
              variant={selectedRole === "admin" ? "default" : "outline"}
              onClick={() => setSelectedRole("admin")}
            >
              Admin Dashboard
            </Button>
            <Button 
              variant={selectedRole === "authority" ? "default" : "outline"}
              onClick={() => setSelectedRole("authority")}
            >
              Authority View
            </Button>
            <Button 
              variant={selectedRole === "community" ? "default" : "outline"}
              onClick={() => setSelectedRole("community")}
            >
              Community Portal
            </Button>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-8">
        {/* Dashboard Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Active Alerts"
            value={7}
            description="3 critical, 4 medium"
            icon={AlertTriangle}
            variant="warning"
          />
          <StatsCard
            title="Registered Users"
            value="1,247"
            description="853 community, 394 authority"
            icon={Users}
          />
          <StatsCard
            title="Mock Drills Completed"
            value={23}
            description="This month"
            icon={Target}
            variant="success"
          />
          <StatsCard
            title="Response Rate"
            value="94%"
            description="Average response time: 3.2 min"
            icon={Activity}
            variant="success"
          />
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Alerts & Weather */}
          <div className="lg:col-span-2 space-y-6">
            {/* Active Alerts */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <AlertTriangle className="h-5 w-5 text-warning" />
                  Active Alerts
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <AlertCard
                  title="High Tide Warning"
                  severity="high"
                  location="Coastal Highway, Zone A"
                  time="2 hours ago"
                  description="Unusually high tide levels detected. Coastal flooding possible in low-lying areas."
                  status="active"
                />
                <AlertCard
                  title="Illegal Dumping Reported"
                  severity="medium"
                  location="Marine Drive Beach"
                  time="4 hours ago"
                  description="Community member reported illegal waste dumping near protected coastal area."
                  status="pending"
                />
              </CardContent>
            </Card>

            {/* Mock Drills */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-primary" />
                  Mock Drills & Training
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <MockDrillCard
                  title="Coastal Evacuation Drill"
                  date="Tomorrow, 10:00 AM"
                  location="Seaside Community Center"
                  participants={45}
                  maxParticipants={100}
                  status="upcoming"
                  type="evacuation"
                />
                <MockDrillCard
                  title="Emergency Communication Test"
                  date="Today, 2:00 PM"
                  location="District Control Room"
                  participants={12}
                  maxParticipants={15}
                  status="active"
                  type="communication"
                />
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Weather & Quick Actions */}
          <div className="space-y-6">
            {/* Weather Monitoring */}
            <WeatherCard
              location="Coastal Region A"
              temperature={28}
              condition="Partly cloudy"
              humidity={78}
              windSpeed={15}
              visibility={8}
              pressure={1013}
              riskLevel="low"
            />

            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Radio className="h-5 w-5 text-primary" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button className="w-full justify-start" variant="outline">
                  <Waves className="h-4 w-4 mr-2" />
                  Issue Emergency Alert
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <Target className="h-4 w-4 mr-2" />
                  Schedule Mock Drill
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <Camera className="h-4 w-4 mr-2" />
                  Review Reports
                </Button>
                <Button className="w-full justify-start" variant="outline">
                  <Navigation className="h-4 w-4 mr-2" />
                  Emergency Navigation
                </Button>
              </CardContent>
            </Card>

            {/* System Status */}
            <Card>
              <CardHeader>
                <CardTitle>System Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">Alert System</span>
                  <Badge className="bg-secondary text-secondary-foreground">Online</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Weather API</span>
                  <Badge className="bg-secondary text-secondary-foreground">Connected</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">SMS Gateway</span>
                  <Badge className="bg-secondary text-secondary-foreground">Active</Badge>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm">Database</span>
                  <Badge className="bg-secondary text-secondary-foreground">Healthy</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-card border-t mt-16 py-8">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Shield className="h-6 w-6 text-primary" />
            <span className="text-lg font-semibold">CTAS</span>
          </div>
          <p className="text-sm text-muted-foreground">
            Coastal Threat Alert System - Developed by DAUD Team for HackOut'25
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            Protecting coastal communities through technology and collaboration
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Index;