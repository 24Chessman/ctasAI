import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Cloud, Wind, Droplets, Eye, Thermometer } from "lucide-react";

interface WeatherCardProps {
  location: string;
  temperature: number;
  condition: string;
  humidity: number;
  windSpeed: number;
  visibility: number;
  pressure: number;
  riskLevel: "low" | "medium" | "high";
}

const WeatherCard = ({ 
  location, 
  temperature, 
  condition, 
  humidity, 
  windSpeed, 
  visibility, 
  pressure, 
  riskLevel 
}: WeatherCardProps) => {
  const getRiskColor = () => {
    switch (riskLevel) {
      case "high":
        return "bg-destructive text-destructive-foreground";
      case "medium":
        return "bg-warning text-warning-foreground";
      case "low":
        return "bg-secondary text-secondary-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getWeatherIcon = () => {
    if (condition.toLowerCase().includes("cloud")) return "☁️";
    if (condition.toLowerCase().includes("rain")) return "🌧️";
    if (condition.toLowerCase().includes("storm")) return "⛈️";
    if (condition.toLowerCase().includes("clear")) return "☀️";
    return "🌤️";
  };

  return (
    <Card className="bg-gradient-to-br from-accent/20 to-background">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg flex items-center gap-2">
            <span className="text-2xl">{getWeatherIcon()}</span>
            {location}
          </CardTitle>
          <Badge className={getRiskColor()}>
            {riskLevel.toUpperCase()} RISK
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Thermometer className="h-5 w-5 text-primary" />
            <span className="text-3xl font-bold">{temperature}°C</span>
          </div>
          <span className="text-lg text-muted-foreground capitalize">{condition}</span>
        </div>

        <div className="grid grid-cols-2 gap-4 text-sm">
          <div className="flex items-center gap-2">
            <Droplets className="h-4 w-4 text-blue-500" />
            <span>Humidity: {humidity}%</span>
          </div>
          <div className="flex items-center gap-2">
            <Wind className="h-4 w-4 text-gray-500" />
            <span>Wind: {windSpeed} km/h</span>
          </div>
          <div className="flex items-center gap-2">
            <Eye className="h-4 w-4 text-purple-500" />
            <span>Visibility: {visibility} km</span>
          </div>
          <div className="flex items-center gap-2">
            <Cloud className="h-4 w-4 text-gray-400" />
            <span>Pressure: {pressure} hPa</span>
          </div>
        </div>

        {riskLevel === "high" && (
          <div className="bg-destructive/10 border border-destructive/20 rounded-lg p-3">
            <p className="text-sm text-destructive font-medium">
              ⚠️ High risk conditions detected. Monitor coastal areas closely.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default WeatherCard;