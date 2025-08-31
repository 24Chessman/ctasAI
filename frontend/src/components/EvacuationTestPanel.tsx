import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  AlertTriangle, 
  Bell, 
  Users, 
  Mail, 
  MessageSquare, 
  Smartphone,
  CheckCircle,
  XCircle,
  Loader2
} from "lucide-react";

interface EvacuationTestPanelProps {
  className?: string;
}

const EvacuationTestPanel: React.FC<EvacuationTestPanelProps> = ({ className }) => {
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [customMessage, setCustomMessage] = useState("");
  const [targetLocation, setTargetLocation] = useState("");

  const testEvacuationSystem = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/evacuation/test-evacuation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.detail || 'Failed to test evacuation system');
      }
    } catch (err) {
      setError('Network error: Could not connect to backend server');
    } finally {
      setIsLoading(false);
    }
  };

  const triggerEvacuationAlert = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/evacuation/trigger-evacuation', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          location: targetLocation || undefined,
          threat_level: "HIGH",
          custom_message: customMessage || undefined
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.detail || 'Failed to trigger evacuation alert');
      }
    } catch (err) {
      setError('Network error: Could not connect to backend server');
    } finally {
      setIsLoading(false);
    }
  };

  const sendCustomAlert = async () => {
    if (!customMessage.trim()) {
      setError('Please enter a custom message');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/evacuation/send-custom-alert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: customMessage,
          title: "Custom Alert",
          target_location: targetLocation || undefined
        }),
      });

      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.detail || 'Failed to send custom alert');
      }
    } catch (err) {
      setError('Network error: Could not connect to backend server');
    } finally {
      setIsLoading(false);
    }
  };

  const getRegisteredUsers = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://localhost:8000/api/v1/evacuation/users');
      const data = await response.json();
      
      if (response.ok) {
        setResult(data);
      } else {
        setError(data.detail || 'Failed to get registered users');
      }
    } catch (err) {
      setError('Network error: Could not connect to backend server');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={className}>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertTriangle className="h-5 w-5 text-orange-600" />
            Evacuation Alert Testing Panel
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Test Controls */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-4">
              <div>
                <Label htmlFor="location">Target Location (Optional)</Label>
                <Input
                  id="location"
                  placeholder="e.g., Mumbai, Zone A"
                  value={targetLocation}
                  onChange={(e) => setTargetLocation(e.target.value)}
                />
              </div>
              
              <div>
                <Label htmlFor="message">Custom Message (Optional)</Label>
                <Textarea
                  id="message"
                  placeholder="Enter custom evacuation message..."
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  rows={3}
                />
              </div>
            </div>

            <div className="space-y-3">
              <Button 
                onClick={testEvacuationSystem}
                disabled={isLoading}
                className="w-full"
                variant="outline"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <AlertTriangle className="h-4 w-4 mr-2" />
                )}
                Test Real Threat Detection
              </Button>

              <Button 
                onClick={triggerEvacuationAlert}
                disabled={isLoading}
                className="w-full"
                variant="destructive"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Bell className="h-4 w-4 mr-2" />
                )}
                Trigger Evacuation Alert
              </Button>

              <Button 
                onClick={sendCustomAlert}
                disabled={isLoading || !customMessage.trim()}
                className="w-full"
                variant="secondary"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <MessageSquare className="h-4 w-4 mr-2" />
                )}
                Send Custom Alert
              </Button>

              <Button 
                onClick={getRegisteredUsers}
                disabled={isLoading}
                className="w-full"
                variant="outline"
              >
                {isLoading ? (
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                ) : (
                  <Users className="h-4 w-4 mr-2" />
                )}
                Get Registered Users
              </Button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <Alert variant="destructive">
              <XCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Results Display */}
          {result && (
            <div className="space-y-4">
              <Alert>
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>
                  <strong>Operation completed successfully!</strong>
                </AlertDescription>
              </Alert>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Results</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Success Status */}
                  <div className="flex items-center gap-2">
                    <Badge variant={result.success ? "default" : "destructive"}>
                      {result.success ? "Success" : "Failed"}
                    </Badge>
                    <span className="text-sm text-muted-foreground">
                      {result.message}
                    </span>
                  </div>

                  {/* Notification Statistics */}
                  {result.results && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      <div className="text-center p-3 bg-muted rounded-lg">
                        <div className="text-2xl font-bold text-primary">
                          {result.results.total_users || 0}
                        </div>
                        <div className="text-sm text-muted-foreground">Total Users</div>
                      </div>
                      
                      <div className="text-center p-3 bg-muted rounded-lg">
                        <div className="text-2xl font-bold text-green-600">
                          {result.results.email_sent || 0}
                        </div>
                        <div className="text-sm text-muted-foreground flex items-center justify-center gap-1">
                          <Mail className="h-3 w-3" />
                          Emails
                        </div>
                      </div>
                      
                      <div className="text-center p-3 bg-muted rounded-lg">
                        <div className="text-2xl font-bold text-blue-600">
                          {result.results.sms_sent || 0}
                        </div>
                        <div className="text-sm text-muted-foreground flex items-center justify-center gap-1">
                          <MessageSquare className="h-3 w-3" />
                          SMS
                        </div>
                      </div>
                      
                      <div className="text-center p-3 bg-muted rounded-lg">
                        <div className="text-2xl font-bold text-purple-600">
                          {result.results.push_sent || 0}
                        </div>
                        <div className="text-sm text-muted-foreground flex items-center justify-center gap-1">
                          <Smartphone className="h-3 w-3" />
                          Push
                        </div>
                      </div>
                    </div>
                  )}

                  {/* User List */}
                  {result.users && (
                    <div>
                      <h4 className="font-semibold mb-2">Registered Users ({result.total_users})</h4>
                      <div className="max-h-40 overflow-y-auto space-y-2">
                        {result.users.map((user: any, index: number) => (
                          <div key={index} className="flex items-center justify-between p-2 bg-muted rounded text-sm">
                            <span>{user.full_name || 'Unknown'}</span>
                            <div className="flex gap-2">
                              {user.has_phone && <Badge variant="outline" className="text-xs">SMS</Badge>}
                              {user.has_device_token && <Badge variant="outline" className="text-xs">Push</Badge>}
                              <Badge variant="outline" className="text-xs">{user.location || 'Unknown'}</Badge>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Threat Data */}
                  {result.threat_data && (
                    <div>
                      <h4 className="font-semibold mb-2">Threat Information</h4>
                      <div className="bg-muted p-3 rounded text-sm">
                        <pre className="whitespace-pre-wrap">
                          {JSON.stringify(result.threat_data, null, 2)}
                        </pre>
                      </div>
                    </div>
                  )}

                  {/* Timestamp */}
                  <div className="text-xs text-muted-foreground">
                    Timestamp: {result.timestamp}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Instructions */}
          <Card className="bg-blue-50 border-blue-200">
            <CardContent className="pt-6">
              <h4 className="font-semibold text-blue-800 mb-2">How to Test:</h4>
              <ul className="text-sm text-blue-700 space-y-1">
                <li>• <strong>Test Real Threat Detection:</strong> Runs actual threat detection and sends alerts if threats are found</li>
                <li>• <strong>Trigger Evacuation Alert:</strong> Sends evacuation alerts to all users with mock threat data</li>
                <li>• <strong>Send Custom Alert:</strong> Sends a custom message to users</li>
                <li>• <strong>Get Registered Users:</strong> Shows all users in the system</li>
              </ul>
            </CardContent>
          </Card>
        </CardContent>
      </Card>
    </div>
  );
};

export default EvacuationTestPanel;
