import { MapPin, Navigation, Compass, AlertTriangle, Phone, Clock } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import Header from "@/components/Header";

const NavigationPage = () => {
  const emergencyContacts = [
    { name: "Coast Guard", number: "1-800-424-8802", icon: Phone },
    { name: "Emergency Services", number: "911", icon: AlertTriangle },
    { name: "Weather Service", number: "1-800-427-7623", icon: Clock },
  ];

  const safetyGuidelines = [
    {
      title: "Before Heading Out",
      items: [
        "Check weather forecasts and marine conditions",
        "Inform someone of your route and expected return time",
        "Ensure all safety equipment is on board",
        "Verify communication devices are working"
      ]
    },
    {
      title: "During Navigation",
      items: [
        "Maintain constant awareness of weather changes",
        "Keep emergency contacts readily available",
        "Monitor radio for weather alerts",
        "Stay within designated safe zones"
      ]
    },
    {
      title: "Emergency Procedures",
      items: [
        "Immediately seek shelter if storm warnings are issued",
        "Use emergency flares only in actual emergencies",
        "Stay with your vessel unless it's unsafe",
        "Signal for help using available communication methods"
      ]
    }
  ];

  const navigationZones = [
    {
      name: "Safe Zone A",
      status: "Open",
      description: "Protected bay area, suitable for all vessels",
      coordinates: "27°58'N, 82°48'W"
    },
    {
      name: "Restricted Zone B",
      status: "Limited Access",
      description: "High traffic area, speed restrictions apply",
      coordinates: "27°59'N, 82°47'W"
    },
    {
      name: "Emergency Zone C",
      status: "Closed",
      description: "Storm surge area, access prohibited",
      coordinates: "28°00'N, 82°46'W"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="container mx-auto px-4 py-8 space-y-8">
      <div className="text-center space-y-4">
        <div className="flex items-center justify-center space-x-2">
          <Navigation className="h-8 w-8 text-primary" />
          <h1 className="text-3xl font-bold">Coastal Navigation</h1>
        </div>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          Essential navigation information, safety guidelines, and emergency procedures for coastal waters.
        </p>
      </div>

      {/* Emergency Contacts */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <AlertTriangle className="h-5 w-5 text-destructive" />
            <span>Emergency Contacts</span>
          </CardTitle>
          <CardDescription>
            Keep these numbers readily available for emergency situations
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-4">
            {emergencyContacts.map((contact, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 border rounded-lg">
                <contact.icon className="h-5 w-5 text-primary" />
                <div>
                  <p className="font-medium">{contact.name}</p>
                  <p className="text-sm text-muted-foreground">{contact.number}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Navigation Zones */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <MapPin className="h-5 w-5 text-primary" />
            <span>Navigation Zones</span>
          </CardTitle>
          <CardDescription>
            Current status of coastal navigation zones
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {navigationZones.map((zone, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-2">
                    <h3 className="font-medium">{zone.name}</h3>
                    <Badge 
                      variant={zone.status === "Open" ? "default" : zone.status === "Limited Access" ? "secondary" : "destructive"}
                    >
                      {zone.status}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-1">{zone.description}</p>
                  <p className="text-xs text-muted-foreground">Coordinates: {zone.coordinates}</p>
                </div>
                <Button variant="outline" size="sm">
                  View Details
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Safety Guidelines */}
      <div className="grid md:grid-cols-3 gap-6">
        {safetyGuidelines.map((section, index) => (
          <Card key={index}>
            <CardHeader>
              <CardTitle className="text-lg">{section.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {section.items.map((item, itemIndex) => (
                  <li key={itemIndex} className="flex items-start space-x-2">
                    <div className="h-1.5 w-1.5 bg-primary rounded-full mt-2 flex-shrink-0" />
                    <span className="text-sm">{item}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Weather Information */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Compass className="h-5 w-5 text-primary" />
            <span>Current Weather Conditions</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-4 gap-4">
            <div className="text-center p-4 border rounded-lg">
              <p className="text-2xl font-bold text-primary">75°F</p>
              <p className="text-sm text-muted-foreground">Temperature</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <p className="text-2xl font-bold text-primary">15 mph</p>
              <p className="text-sm text-muted-foreground">Wind Speed</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <p className="text-2xl font-bold text-primary">3 ft</p>
              <p className="text-sm text-muted-foreground">Wave Height</p>
            </div>
            <div className="text-center p-4 border rounded-lg">
              <p className="text-2xl font-bold text-green-600">Good</p>
              <p className="text-sm text-muted-foreground">Visibility</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
          <CardDescription>
            Access important navigation tools and resources
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <MapPin className="h-6 w-6" />
              <span>Marine Charts</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <Navigation className="h-6 w-6" />
              <span>Route Planner</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <AlertTriangle className="h-6 w-6" />
              <span>Emergency Guide</span>
            </Button>
            <Button variant="outline" className="h-20 flex flex-col space-y-2">
              <Phone className="h-6 w-6" />
              <span>Contact Coast Guard</span>
            </Button>
          </div>
        </CardContent>
      </Card>
      </div>
    </div>
  );
};

export default NavigationPage;
