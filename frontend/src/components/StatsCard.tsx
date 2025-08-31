import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface StatsCardProps {
  title: string;
  value: string | number;
  description?: string;
  icon: LucideIcon;
  variant?: "default" | "warning" | "destructive" | "success";
}

const StatsCard = ({ title, value, description, icon: Icon, variant = "default" }: StatsCardProps) => {
  const getVariantStyles = () => {
    switch (variant) {
      case "warning":
        return "border-warning/20 bg-warning/5";
      case "destructive":
        return "border-destructive/20 bg-destructive/5";
      case "success":
        return "border-secondary/20 bg-secondary/5";
      default:
        return "";
    }
  };

  const getIconStyles = () => {
    switch (variant) {
      case "warning":
        return "text-warning";
      case "destructive":
        return "text-destructive";
      case "success":
        return "text-secondary";
      default:
        return "text-primary";
    }
  };

  return (
    <Card className={`${getVariantStyles()}`}>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <Icon className={`h-4 w-4 ${getIconStyles()}`} />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{value}</div>
        {description && (
          <p className="text-xs text-muted-foreground">{description}</p>
        )}
      </CardContent>
    </Card>
  );
};

export default StatsCard;