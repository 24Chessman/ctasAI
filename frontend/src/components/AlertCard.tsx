import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AlertTriangle, MapPin, Clock } from "lucide-react";

interface AlertCardProps {
  title: string;
  severity: "low" | "medium" | "high" | "critical";
  location: string;
  time: string;
  description: string;
  status: "active" | "resolved" | "pending";
}

const AlertCard = ({ title, severity, location, time, description, status }: AlertCardProps) => {
  const getSeverityColor = () => {
    switch (severity) {
      case "critical":
        return "bg-destructive text-destructive-foreground";
      case "high":
        return "bg-warning text-warning-foreground";
      case "medium":
        return "bg-primary text-primary-foreground";
      case "low":
        return "bg-secondary text-secondary-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getStatusColor = () => {
    switch (status) {
      case "active":
        return "bg-destructive text-destructive-foreground";
      case "resolved":
        return "bg-secondary text-secondary-foreground";
      case "pending":
        return "bg-warning text-warning-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  return (
    <Card className="hover:shadow-lg transition-shadow">
      <CardHeader>
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-warning" />
            {title}
          </CardTitle>
          <div className="flex gap-2">
            <Badge className={getSeverityColor()}>
              {severity.toUpperCase()}
            </Badge>
            <Badge className={getStatusColor()}>
              {status.toUpperCase()}
            </Badge>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground">{description}</p>
        
        <div className="flex items-center gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-1">
            <MapPin className="h-4 w-4" />
            {location}
          </div>
          <div className="flex items-center gap-1">
            <Clock className="h-4 w-4" />
            {time}
          </div>
        </div>

        <div className="flex gap-2">
          <Button size="sm" variant="outline">View Details</Button>
          <Button size="sm">Take Action</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default AlertCard;