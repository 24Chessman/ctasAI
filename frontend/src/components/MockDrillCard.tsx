// MockDrillCard.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Calendar, Users, MapPin, Target, Brain } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import CoastalQuiz from "./CoastalQuiz";

interface MockDrillCardProps {
  title: string;
  date: string;
  location: string;
  participants: number;
  maxParticipants: number;
  status: "upcoming" | "active" | "completed";
  type: "evacuation" | "shelter" | "communication" | "medical";
}

const MockDrillCard = ({ 
  title, 
  date, 
  location, 
  participants, 
  maxParticipants, 
  status, 
  type 
}: MockDrillCardProps) => {
  const navigate = useNavigate();
  const [showQuiz, setShowQuiz] = useState(false);

  const handleViewDetails = () => {
    navigate('/mock-drills');
  };

  const handleJoinDrill = () => {
    navigate('/mock-drills');
  };

  const handleStartQuiz = () => {
    setShowQuiz(true);
  };

  const handleQuizComplete = (result: any) => {
    console.log('Quiz completed with score:', result.score);
    // You can save the quiz result to your database here
  };

  const handleCloseQuiz = () => {
    setShowQuiz(false);
  };
  const getStatusColor = () => {
    switch (status) {
      case "upcoming":
        return "bg-primary text-primary-foreground";
      case "active":
        return "bg-warning text-warning-foreground";
      case "completed":
        return "bg-secondary text-secondary-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getTypeIcon = () => {
    switch (type) {
      case "evacuation":
        return "🚨";
      case "shelter":
        return "🏠";
      case "communication":
        return "📡";
      case "medical":
        return "🏥";
      default:
        return "🎯";
    }
  };

  return (
    <>
      <Card className="hover:shadow-lg transition-shadow cursor-pointer" onClick={handleViewDetails}>
        <CardHeader>
          <div className="flex items-start justify-between">
            <CardTitle className="text-lg flex items-center gap-2">
              <span className="text-xl">{getTypeIcon()}</span>
              {title}
            </CardTitle>
            <Badge className={getStatusColor()}>
              {status.toUpperCase()}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <Calendar className="h-4 w-4 text-muted-foreground" />
              <span>{date}</span>
            </div>
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 text-muted-foreground" />
              <span>{location}</span>
            </div>
            <div className="flex items-center gap-2">
              <Users className="h-4 w-4 text-muted-foreground" />
              <span>{participants}/{maxParticipants} participants</span>
            </div>
            <div className="flex items-center gap-2">
              <Target className="h-4 w-4 text-muted-foreground" />
              <span className="capitalize">{type} drill</span>
            </div>
          </div>

          <div className="w-full bg-muted rounded-full h-2">
            <div 
              className="bg-primary h-2 rounded-full transition-all" 
              style={{ width: `${(participants / maxParticipants) * 100}%` }}
            />
          </div>

          <div className="flex gap-2">
            {status === "upcoming" && (
              <>
                <Button size="sm" variant="outline" onClick={handleViewDetails}>View Details</Button>
                <Button size="sm" onClick={handleJoinDrill}>Join Drill</Button>
                <Button size="sm" variant="secondary" onClick={handleStartQuiz} className="flex items-center gap-1">
                  <Brain className="h-3 w-3" />
                  Take Quiz
                </Button>
              </>
            )}
            {status === "active" && (
              <>
                <Button size="sm" variant="outline" onClick={handleViewDetails}>Live View</Button>
                <Button size="sm" className="bg-warning hover:bg-warning/90" onClick={handleJoinDrill}>Participate</Button>
                <Button size="sm" variant="secondary" onClick={handleStartQuiz} className="flex items-center gap-1">
                  <Brain className="h-3 w-3" />
                  Take Quiz
                </Button>
              </>
            )}
            {status === "completed" && (
              <>
                <Button size="sm" variant="outline" onClick={handleViewDetails}>View Results</Button>
                <Button size="sm" onClick={handleJoinDrill}>Download Report</Button>
                <Button size="sm" variant="secondary" onClick={handleStartQuiz} className="flex items-center gap-1">
                  <Brain className="h-3 w-3" />
                  Take Quiz
                </Button>
              </>
            )}
          </div>
        </CardContent>
      </Card>

      {showQuiz && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <CoastalQuiz 
              onComplete={handleQuizComplete}
              onClose={handleCloseQuiz}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default MockDrillCard;