import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  MessageSquare, 
  Phone, 
  AlertTriangle, 
  Users, 
  Send, 
  CheckCircle, 
  XCircle,
  Settings,
  TestTube,
  Bell,
  Shield,
  Activity
} from "lucide-react";
import Header from "@/components/Header";
import { toast } from "sonner";

interface SMSStatus {
  sms_configured: boolean;
  sms_provider: string;
  users_with_phones: number;
  api_key_configured: boolean;
  api_url_configured: boolean;
}

interface SMSResponse {
  success: boolean;
  message: string;
  total_users: number;
  successful: number;
  failed: number;
  errors: string[];
}

const SMSAlerts = () => {
  const [smsStatus, setSmsStatus] = useState<SMSStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [testPhone, setTestPhone] = useState('');
  const [testMessage, setTestMessage] = useState('Test SMS from CTAS Alert System');
  const [threatLevel, setThreatLevel] = useState('HIGH');
  const [customMessage, setCustomMessage] = useState('');
  const [location, setLocation] = useState('');
  const [lastResult, setLastResult] = useState<SMSResponse | null>(null);

  useEffect(() => {
    fetchSMSStatus();
  }, []);

  const fetchSMSStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/sms/sms-status');
      if (response.ok) {
        const data = await response.json();
        setSmsStatus(data);
      }
    } catch (error) {
      console.error('Error fetching SMS status:', error);
    }
  };

  const sendTestSMS = async () => {
    if (!testPhone.trim()) {
      toast.error('Please enter a phone number');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/v1/sms/test-sms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone: testPhone,
          message: testMessage
        }),
      });

      const data = await response.json();
      
      if (data.success) {
        toast.success('Test SMS sent successfully!');
      } else {
        toast.error(`Failed to send test SMS: ${data.message}`);
      }
    } catch (error) {
      toast.error('Error sending test SMS');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendHighAlert = async () => {
    setLoading(true);
    try {
      // Sample threat data
      const threatData = {
        cyclone: {
          probability: 0.85,
          intensity: 'Category 3',
          direction: 'Northwest'
        },
        storm_surge: {
          threat_level: 'HIGH',
          total_water_level: 3.2,
          surge_height: 2.1
        },
        overall_threat: threatLevel
      };

      const response = await fetch('http://localhost:8000/api/v1/sms/send-high-alert', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          threat_level: threatLevel,
          threat_data: threatData,
          location: location || undefined,
          message: customMessage || undefined
        }),
      });

      const data: SMSResponse = await response.json();
      setLastResult(data);
      
      if (data.success) {
        toast.success(`High alert sent! ${data.successful} SMS sent successfully`);
      } else {
        toast.error(`Failed to send high alert: ${data.message}`);
      }
    } catch (error) {
      toast.error('Error sending high alert');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const sendBulkSMS = async () => {
    if (!customMessage.trim()) {
      toast.error('Please enter a message');
      return;
    }

    setLoading(true);
    try {
      // For demo purposes, using sample phone numbers
      const phoneNumbers = ['+919876543210', '+919876543211', '+919876543212'];

      const response = await fetch('http://localhost:8000/api/v1/sms/send-bulk-sms', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phone_numbers: phoneNumbers,
          message: customMessage
        }),
      });

      const data: SMSResponse = await response.json();
      setLastResult(data);
      
      if (data.success) {
        toast.success(`Bulk SMS sent! ${data.successful} SMS sent successfully`);
      } else {
        toast.error(`Failed to send bulk SMS: ${data.message}`);
      }
    } catch (error) {
      toast.error('Error sending bulk SMS');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center gap-3">
              <MessageSquare className="h-12 w-12 text-primary" />
              <h1 className="text-4xl font-bold">SMS Alert Management</h1>
            </div>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Send emergency SMS alerts to users based on their phone numbers. 
              Manage high alerts, test SMS functionality, and monitor delivery status.
            </p>
          </div>

          {/* SMS Status */}
          {smsStatus && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Activity className="h-5 w-5" />
                  SMS Service Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
                    <div className={`w-3 h-3 rounded-full ${smsStatus.sms_configured ? 'bg-green-500' : 'bg-red-500'}`} />
                    <div>
                      <p className="font-medium">SMS Configured</p>
                      <p className="text-sm text-muted-foreground">
                        {smsStatus.sms_configured ? 'Yes' : 'No'}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
                    <Phone className="h-5 w-5 text-blue-500" />
                    <div>
                      <p className="font-medium">Provider</p>
                      <p className="text-sm text-muted-foreground capitalize">
                        {smsStatus.sms_provider}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
                    <Users className="h-5 w-5 text-green-500" />
                    <div>
                      <p className="font-medium">Users with Phones</p>
                      <p className="text-sm text-muted-foreground">
                        {smsStatus.users_with_phones}
                      </p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-3 p-4 bg-muted rounded-lg">
                    <Settings className="h-5 w-5 text-purple-500" />
                    <div>
                      <p className="font-medium">API Status</p>
                      <p className="text-sm text-muted-foreground">
                        {smsStatus.api_key_configured && smsStatus.api_url_configured ? 'Ready' : 'Not Ready'}
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Test SMS */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TestTube className="h-5 w-5" />
                Test SMS
              </CardTitle>
              <CardDescription>
                Send a test SMS to verify your configuration
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">Phone Number</label>
                  <Input
                    placeholder="+919876543210"
                    value={testPhone}
                    onChange={(e) => setTestPhone(e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Message</label>
                  <Input
                    placeholder="Test message"
                    value={testMessage}
                    onChange={(e) => setTestMessage(e.target.value)}
                  />
                </div>
              </div>
              <Button 
                onClick={sendTestSMS} 
                disabled={loading || !smsStatus?.sms_configured}
                className="w-full"
              >
                <Send className="h-4 w-4 mr-2" />
                Send Test SMS
              </Button>
            </CardContent>
          </Card>

          {/* High Alert SMS */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-red-500" />
                High Alert SMS
              </CardTitle>
              <CardDescription>
                Send emergency alerts to all users with phone numbers
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">Threat Level</label>
                  <Select value={threatLevel} onValueChange={setThreatLevel}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="HIGH">High</SelectItem>
                      <SelectItem value="MEDIUM">Medium</SelectItem>
                      <SelectItem value="LOW">Low</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium">Location (Optional)</label>
                  <Input
                    placeholder="coastal_zone_1"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Custom Message (Optional)</label>
                  <Input
                    placeholder="Custom alert message"
                    value={customMessage}
                    onChange={(e) => setCustomMessage(e.target.value)}
                  />
                </div>
              </div>
              
              <Alert>
                <Bell className="h-4 w-4" />
                <AlertDescription>
                  This will send an emergency SMS to all users with phone numbers. 
                  The message will include threat details and evacuation instructions.
                </AlertDescription>
              </Alert>
              
              <Button 
                onClick={sendHighAlert} 
                disabled={loading || !smsStatus?.sms_configured}
                variant="destructive"
                className="w-full"
              >
                <Shield className="h-4 w-4 mr-2" />
                Send High Alert SMS
              </Button>
            </CardContent>
          </Card>

          {/* Bulk SMS */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MessageSquare className="h-5 w-5" />
                Bulk SMS
              </CardTitle>
              <CardDescription>
                Send custom SMS to specific phone numbers
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium">Message</label>
                <Textarea
                  placeholder="Enter your SMS message here..."
                  value={customMessage}
                  onChange={(e) => setCustomMessage(e.target.value)}
                  rows={3}
                />
              </div>
              
              <Alert>
                <MessageSquare className="h-4 w-4" />
                <AlertDescription>
                  This will send SMS to demo phone numbers. In production, you can specify exact phone numbers.
                </AlertDescription>
              </Alert>
              
              <Button 
                onClick={sendBulkSMS} 
                disabled={loading || !smsStatus?.sms_configured}
                className="w-full"
              >
                <Send className="h-4 w-4 mr-2" />
                Send Bulk SMS
              </Button>
            </CardContent>
          </Card>

          {/* Last Result */}
          {lastResult && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  {lastResult.success ? (
                    <CheckCircle className="h-5 w-5 text-green-500" />
                  ) : (
                    <XCircle className="h-5 w-5 text-red-500" />
                  )}
                  Last SMS Result
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="flex items-center gap-2">
                    <Badge variant={lastResult.success ? "default" : "destructive"}>
                      {lastResult.success ? "Success" : "Failed"}
                    </Badge>
                    <span className="text-sm text-muted-foreground">{lastResult.message}</span>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="text-center p-4 bg-muted rounded-lg">
                      <p className="text-2xl font-bold text-blue-600">{lastResult.total_users}</p>
                      <p className="text-sm text-muted-foreground">Total Users</p>
                    </div>
                    <div className="text-center p-4 bg-muted rounded-lg">
                      <p className="text-2xl font-bold text-green-600">{lastResult.successful}</p>
                      <p className="text-sm text-muted-foreground">Successful</p>
                    </div>
                    <div className="text-center p-4 bg-muted rounded-lg">
                      <p className="text-2xl font-bold text-red-600">{lastResult.failed}</p>
                      <p className="text-sm text-muted-foreground">Failed</p>
                    </div>
                  </div>
                  
                  {lastResult.errors.length > 0 && (
                    <div>
                      <p className="text-sm font-medium text-red-600 mb-2">Errors:</p>
                      <ul className="text-sm text-muted-foreground space-y-1">
                        {lastResult.errors.slice(0, 5).map((error, index) => (
                          <li key={index}>• {error}</li>
                        ))}
                        {lastResult.errors.length > 5 && (
                          <li>• ... and {lastResult.errors.length - 5} more errors</li>
                        )}
                      </ul>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Configuration Instructions */}
          <Card>
            <CardHeader>
              <CardTitle>Configuration Instructions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="prose prose-sm max-w-none">
                <h4 className="font-semibold">SMS Provider Setup:</h4>
                <ol className="list-decimal list-inside space-y-2 text-sm text-muted-foreground">
                  <li>Choose an SMS provider (Twilio, Nexmo, AWS SNS, or custom)</li>
                  <li>Add your API credentials to the backend .env file</li>
                  <li>Configure the SMS service in the backend settings</li>
                  <li>Test the configuration using the Test SMS feature</li>
                </ol>
                
                <h4 className="font-semibold mt-4">Environment Variables:</h4>
                <div className="bg-muted p-3 rounded-lg text-sm font-mono">
                  <p>SMS_API_KEY=your_api_key</p>
                  <p>SMS_API_URL=your_api_url</p>
                  <p>TWILIO_ACCOUNT_SID=your_twilio_sid</p>
                  <p>TWILIO_AUTH_TOKEN=your_twilio_token</p>
                  <p>TWILIO_PHONE_NUMBER=your_twilio_number</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default SMSAlerts;
