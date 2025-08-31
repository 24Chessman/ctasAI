import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Header from "@/components/Header";

interface ThreatData {
  timestamp: string;
  weather_data: {
    wind_speed: number;
    pressure: number;
    wave_height: number;
    water_level: number;
    temp_c: number;
    humidity: number;
  };
  cyclone: {
    probability: number;
    classification: string;
    confidence: number;
  };
  storm_surge: {
    total_water_level: number;
    threat_level: string;
    pressure_surge: number;
    wind_surge: number;
  };
  overall_threat: string;
  recommendations: string[];
}

const LiveAlerts = () => {
  const [threatData, setThreatData] = useState<ThreatData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchThreatData();
    
    // Set up interval to refresh data every minute
    const intervalId = setInterval(fetchThreatData, 60000);
    
    return () => clearInterval(intervalId);
  }, []);

  const fetchThreatData = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/v1/threat-detection');
      
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Response data:', data);
      
      if (data.status === "success") {
        setThreatData(data.data);
        setError(null);
      } else {
        throw new Error(data.message || "Unknown error");
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      console.error('Error fetching threat data:', err);
    } finally {
      setLoading(false);
    }
  };

  const getThreatLevelClass = (level: string) => {
    switch (level) {
      case 'HIGH': return 'bg-red-100 border-red-400 text-red-800';
      case 'MEDIUM': return 'bg-yellow-100 border-yellow-400 text-yellow-800';
      case 'LOW': return 'bg-green-100 border-green-400 text-green-800';
      default: return 'bg-gray-100 border-gray-400 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-4 py-8 flex items-center justify-center h-96">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
            <p className="mt-4 text-muted-foreground">Loading threat assessment...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="container mx-auto px-4 py-8 flex items-center justify-center h-96">
          <div className="bg-card p-6 rounded-lg shadow-md max-w-md w-full">
            <div className="text-destructive text-center mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <h2 className="text-xl font-bold text-center mb-4">Error Loading Data</h2>
            <p className="text-muted-foreground mb-6">{error}</p>
            <div className="flex justify-center space-x-4">
              <Button onClick={fetchThreatData}>
                Try Again
              </Button>
              <Button variant="outline" onClick={() => navigate(-1)}>
                Go Back
              </Button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Coastal Threat Monitoring</h1>
          <Button variant="outline" onClick={() => navigate(-1)}>
            Go Back
          </Button>
        </div>

        {threatData && (
          <>
            {/* Overall Threat Level */}
            <Card className="mb-6">
              <CardContent className="p-6">
                <div className={`p-4 border-l-4 rounded-md ${getThreatLevelClass(threatData.overall_threat)}`}>
                  <div className="flex items-center justify-between">
                    <h2 className="text-xl font-semibold">Overall Threat Level</h2>
                    <Badge className={`text-sm font-medium ${getThreatLevelClass(threatData.overall_threat)}`}>
                      {threatData.overall_threat}
                    </Badge>
                  </div>
                  <p className="text-muted-foreground mt-2">
                    Last updated: {new Date(threatData.timestamp).toLocaleString()}
                  </p>
                </div>
              </CardContent>
            </Card>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              {/* Cyclone Threat Card */}
              <Card>
                <CardHeader>
                  <CardTitle>Cyclone Detection</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Probability:</span>
                    <span className="font-medium">{(threatData.cyclone.probability * 100).toFixed(2)}%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Classification:</span>
                    <span className="font-medium">{threatData.cyclone.classification}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Confidence:</span>
                    <span className="font-medium">{(threatData.cyclone.confidence * 100).toFixed(2)}%</span>
                  </div>
                </CardContent>
              </Card>

              {/* Storm Surge Card */}
              <Card>
                <CardHeader>
                  <CardTitle>Storm Surge Prediction</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Total Water Level:</span>
                    <span className="font-medium">{threatData.storm_surge.total_water_level}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Threat Level:</span>
                    <span className="font-medium capitalize">{threatData.storm_surge.threat_level}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Pressure Surge:</span>
                    <span className="font-medium">{threatData.storm_surge.pressure_surge}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Wind Surge:</span>
                    <span className="font-medium">{threatData.storm_surge.wind_surge}m</span>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Weather Conditions Card */}
            <Card className="mb-6">
              <CardHeader>
                <CardTitle>Current Weather Conditions</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <span className="block text-muted-foreground">Wind Speed</span>
                    <span className="block text-xl font-semibold">{threatData.weather_data.wind_speed} km/h</span>
                  </div>
                  <div className="text-center">
                    <span className="block text-muted-foreground">Pressure</span>
                    <span className="block text-xl font-semibold">{threatData.weather_data.pressure} hPa</span>
                  </div>
                  <div className="text-center">
                    <span className="block text-muted-foreground">Wave Height</span>
                    <span className="block text-xl font-semibold">{threatData.weather_data.wave_height}m</span>
                  </div>
                  <div className="text-center">
                    <span className="block text-muted-foreground">Temperature</span>
                    <span className="block text-xl font-semibold">{threatData.weather_data.temp_c}°C</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Recommendations Card */}
            <Card>
              <CardHeader>
                <CardTitle>Recommendations</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-2">
                  {threatData.recommendations.map((recommendation, index) => (
                    <li key={index} className="flex items-start">
                      <svg className="w-5 h-5 text-green-600 mt-0.5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <span>{recommendation}</span>
                    </li>
                  ))}
                </ul>
              </CardContent>
            </Card>
          </>
        )}

        <div className="mt-6 text-center">
          <Button onClick={fetchThreatData}>
            Refresh Data
          </Button>
        </div>
      </div>
    </div>
  );
};

export default LiveAlerts;