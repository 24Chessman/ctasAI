// MockDrillsPage.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import MockDrillCard from "@/components/MockDrillCard";
import Header from "@/components/Header";

const MockDrillsPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Small spacing partition between header and card */}
      <div className="h-6 bg-muted/20 border-y"></div>
      
      <div className="container mx-auto px-4 py-8">
        <Card className="shadow-lg border-0">
          <CardHeader className="pb-4 border-b">
            <CardTitle className="flex items-center gap-2 text-2xl font-bold text-primary">
              Mock Drills & Training Sessions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6 pt-6">
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
            <MockDrillCard
              title="Medical Emergency Response"
              date="Last Friday, 9:00 AM"
              location="Central Hospital"
              participants={28}
              maxParticipants={30}
              status="completed"
              type="medical"
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default MockDrillsPage;