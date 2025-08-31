import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Brain, Trophy, Target, Waves, AlertTriangle, Wind, Shield, RefreshCw } from "lucide-react";
import Header from "@/components/Header";
import CoastalQuiz from "@/components/CoastalQuiz";
import { useState } from "react";

const QuizPage = () => {
  const [showQuiz, setShowQuiz] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [quizResults, setQuizResults] = useState<any[]>([]);

  const handleStartQuiz = (category?: string) => {
    setSelectedCategory(category || null);
    setShowQuiz(true);
  };

  const handleQuizComplete = (result: any) => {
    const quizType = selectedCategory ? `${selectedCategory} Quiz` : 'Complete Quiz';
    setQuizResults(prev => [...prev, { 
      ...result, 
      date: new Date().toISOString(),
      quizType: quizType
    }]);
    setShowQuiz(false);
    setSelectedCategory(null);
  };

  const handleCloseQuiz = () => {
    setShowQuiz(false);
    setSelectedCategory(null);
  };

  const getAverageScore = () => {
    if (quizResults.length === 0) return 0;
    const total = quizResults.reduce((sum, result) => sum + result.score, 0);
    return Math.round(total / quizResults.length);
  };

  const getBestScore = () => {
    if (quizResults.length === 0) return 0;
    return Math.max(...quizResults.map(result => result.score));
  };

  const getTotalQuizzes = () => {
    return quizResults.length;
  };

  const getCategoryStats = (category: string) => {
    const categoryResults = quizResults.filter(result => result.quizType === `${category} Quiz`);
    if (categoryResults.length === 0) return { count: 0, bestScore: 0, avgScore: 0 };
    
    const bestScore = Math.max(...categoryResults.map(r => r.score));
    const avgScore = Math.round(categoryResults.reduce((sum, r) => sum + r.score, 0) / categoryResults.length);
    
    return {
      count: categoryResults.length,
      bestScore,
      avgScore
    };
  };

  const quizCategories = [
    {
      id: 'storm-surge',
      name: 'Storm Surge',
      icon: Waves,
      color: 'text-blue-600',
      description: 'Learn about storm surges, their causes, and safety measures.',
      questionCount: 3
    },
    {
      id: 'pollution',
      name: 'Pollution',
      icon: AlertTriangle,
      color: 'text-red-600',
      description: 'Understand coastal pollution and its environmental impact.',
      questionCount: 3
    },
    {
      id: 'erosion',
      name: 'Soil Erosion',
      icon: Wind,
      color: 'text-orange-600',
      description: 'Explore coastal erosion processes and prevention methods.',
      questionCount: 3
    },
    {
      id: 'safety',
      name: 'Safety Procedures',
      icon: Shield,
      color: 'text-green-600',
      description: 'Master essential safety procedures for coastal emergencies.',
      questionCount: 3
    },
    {
      id: 'preparedness',
      name: 'Preparedness',
      icon: Brain,
      color: 'text-purple-600',
      description: 'Learn about emergency preparedness and planning.',
      questionCount: 3
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Hero Section */}
          <div className="text-center mb-8">
            <div className="flex items-center justify-center gap-3 mb-4">
              <Brain className="h-12 w-12 text-primary" />
              <h1 className="text-4xl font-bold">Coastal Safety Quiz</h1>
            </div>
            <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
              Test your knowledge about coastal threats, storm surges, pollution, soil erosion, and safety procedures. 
              Take individual category quizzes or the complete quiz. You can retake quizzes anytime to improve your score!
            </p>
          </div>

          {/* Quiz Categories */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {quizCategories.map((category) => {
              const stats = getCategoryStats(category.name);
              const IconComponent = category.icon;
              
              return (
                <Card key={category.id} className="hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <IconComponent className={`h-5 w-5 ${category.color}`} />
                      {category.name}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-3">
                      {category.description}
                    </p>
                    <div className="flex items-center justify-between mb-3">
                      <Badge variant="secondary">{category.questionCount} Questions</Badge>
                      {stats.count > 0 && (
                        <Badge variant="outline">
                          Best: {stats.bestScore}%
                        </Badge>
                      )}
                    </div>
                    <div className="space-y-2">
                      <Button 
                        onClick={() => handleStartQuiz(category.id)} 
                        className="w-full"
                        variant="outline"
                      >
                        {stats.count > 0 ? 'Retake Quiz' : 'Start Quiz'}
                      </Button>
                      {stats.count > 0 && (
                        <div className="text-xs text-muted-foreground text-center">
                          Taken {stats.count} time{stats.count > 1 ? 's' : ''} • Avg: {stats.avgScore}%
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })}

            <Card className="hover:shadow-lg transition-shadow bg-primary/5 border-primary/20">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5 text-primary" />
                  Complete Quiz
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-muted-foreground mb-3">
                  Take the full 15-question quiz covering all topics.
                </p>
                <div className="flex items-center justify-between mb-3">
                  <Badge variant="secondary">15 Questions</Badge>
                  {getCategoryStats('Complete').count > 0 && (
                    <Badge variant="outline">
                      Best: {getCategoryStats('Complete').bestScore}%
                    </Badge>
                  )}
                </div>
                <Button onClick={() => handleStartQuiz()} className="w-full">
                  {getCategoryStats('Complete').count > 0 ? 'Retake Complete Quiz' : 'Start Complete Quiz'}
                </Button>
              </CardContent>
            </Card>
          </div>

          {/* Quiz Statistics */}
          {quizResults.length > 0 && (
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Trophy className="h-5 w-5 text-yellow-600" />
                  Your Quiz Statistics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-primary">{getAverageScore()}%</div>
                    <p className="text-sm text-muted-foreground">Average Score</p>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">{getBestScore()}%</div>
                    <p className="text-sm text-muted-foreground">Best Score</p>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">{getTotalQuizzes()}</div>
                    <p className="text-sm text-muted-foreground">Quizzes Taken</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Recent Results */}
          {quizResults.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle>Recent Quiz Results</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {quizResults.slice(-10).reverse().map((result, index) => (
                    <div key={index} className="flex items-center justify-between p-4 bg-muted rounded-lg">
                      <div className="flex items-center gap-4">
                        <div className="text-2xl font-bold text-primary">{result.score}%</div>
                        <div>
                          <div className="font-medium">
                            {result.quizType} - {result.correctAnswers} out of {result.totalQuestions} correct
                          </div>
                          <div className="text-sm text-muted-foreground">
                            {new Date(result.date).toLocaleDateString()} - {Math.floor(result.timeTaken / 60)}m {result.timeTaken % 60}s
                          </div>
                        </div>
                      </div>
                      <Badge variant={result.score >= 80 ? "default" : result.score >= 60 ? "secondary" : "destructive"}>
                        {result.score >= 80 ? "Excellent" : result.score >= 60 ? "Good" : "Needs Improvement"}
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Quiz Instructions */}
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>How the Quiz Works</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h3 className="font-semibold mb-2">Quiz Features:</h3>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• Individual category quizzes (3 questions each)</li>
                    <li>• Complete quiz (15 questions)</li>
                    <li>• Multiple choice format</li>
                    <li>• Detailed explanations for each answer</li>
                    <li>• Progress tracking and statistics</li>
                    <li>• Unlimited retakes to improve scores</li>
                    <li>• Time measurement</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold mb-2">Scoring System:</h3>
                  <ul className="space-y-2 text-sm text-muted-foreground">
                    <li>• 90-100%: Coastal Safety Expert</li>
                    <li>• 80-89%: Strong Knowledge</li>
                    <li>• 70-79%: Good Understanding</li>
                    <li>• 60-69%: Needs Improvement</li>
                    <li>• Below 60%: Keep Studying</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Quiz Modal */}
      {showQuiz && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="w-full max-w-4xl max-h-[90vh] overflow-y-auto">
            <CoastalQuiz 
              onComplete={handleQuizComplete}
              onClose={handleCloseQuiz}
              category={selectedCategory}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizPage;
