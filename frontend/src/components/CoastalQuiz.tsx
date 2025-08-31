import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  Brain, 
  Trophy, 
  Target, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertTriangle,
  Waves,
  Wind,
  Shield,
  Award,
  X
} from "lucide-react";

interface Question {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
  explanation: string;
  category: 'storm-surge' | 'pollution' | 'erosion' | 'safety' | 'preparedness';
  difficulty: 'easy' | 'medium' | 'hard';
}

interface QuizResult {
  score: number;
  totalQuestions: number;
  correctAnswers: number;
  timeTaken: number;
  categoryScores: Record<string, number>;
}

interface CoastalQuizProps {
  onComplete: (result: QuizResult) => void;
  onClose: () => void;
  category?: string | null;
}

const coastalQuizQuestions: Question[] = [
  // Storm Surge Questions
  {
    id: 1,
    question: "What is a storm surge?",
    options: [
      "A type of hurricane",
      "A rapid rise in sea level caused by strong winds and low pressure",
      "A tsunami warning",
      "A type of coastal flood"
    ],
    correctAnswer: 1,
    explanation: "A storm surge is a rapid rise in sea level caused by strong winds pushing water toward the shore and low atmospheric pressure allowing the water to rise.",
    category: "storm-surge",
    difficulty: "easy"
  },
  {
    id: 2,
    question: "Which of the following factors most affects storm surge height?",
    options: [
      "Wind speed",
      "Rainfall amount",
      "Temperature",
      "Humidity"
    ],
    correctAnswer: 0,
    explanation: "Wind speed is the primary factor affecting storm surge height. Stronger winds push more water toward the shore.",
    category: "storm-surge",
    difficulty: "medium"
  },
  {
    id: 3,
    question: "What should you do if a storm surge warning is issued?",
    options: [
      "Stay at home and wait",
      "Immediately evacuate to higher ground",
      "Go to the beach to watch",
      "Continue normal activities"
    ],
    correctAnswer: 1,
    explanation: "When a storm surge warning is issued, you should immediately evacuate to higher ground as storm surges can be deadly and unpredictable.",
    category: "storm-surge",
    difficulty: "easy"
  },

  // Pollution Questions
  {
    id: 4,
    question: "What is the main cause of coastal pollution?",
    options: [
      "Natural erosion",
      "Human activities and waste disposal",
      "Marine animals",
      "Weather patterns"
    ],
    correctAnswer: 1,
    explanation: "Human activities, including improper waste disposal, industrial runoff, and plastic pollution, are the main causes of coastal pollution.",
    category: "pollution",
    difficulty: "easy"
  },
  {
    id: 5,
    question: "Which of the following is NOT a common coastal pollutant?",
    options: [
      "Plastic waste",
      "Oil spills",
      "Agricultural runoff",
      "Volcanic ash"
    ],
    correctAnswer: 3,
    explanation: "Volcanic ash is not a common coastal pollutant. Plastic waste, oil spills, and agricultural runoff are major coastal pollution sources.",
    category: "pollution",
    difficulty: "medium"
  },
  {
    id: 6,
    question: "How does coastal pollution affect marine life?",
    options: [
      "It has no effect",
      "It only affects fish",
      "It can cause death, disease, and habitat destruction",
      "It only affects plants"
    ],
    correctAnswer: 2,
    explanation: "Coastal pollution can cause death, disease, and habitat destruction for various marine organisms, disrupting entire ecosystems.",
    category: "pollution",
    difficulty: "medium"
  },

  // Erosion Questions
  {
    id: 7,
    question: "What is coastal erosion?",
    options: [
      "The building up of sand on beaches",
      "The gradual wearing away of coastal land by natural forces",
      "The creation of new islands",
      "The movement of fish"
    ],
    correctAnswer: 1,
    explanation: "Coastal erosion is the gradual wearing away of coastal land by natural forces like waves, currents, and wind.",
    category: "erosion",
    difficulty: "easy"
  },
  {
    id: 8,
    question: "Which human activity can accelerate coastal erosion?",
    options: [
      "Building seawalls",
      "Planting vegetation",
      "Removing sand dunes",
      "Creating artificial reefs"
    ],
    correctAnswer: 2,
    explanation: "Removing sand dunes can accelerate coastal erosion as dunes act as natural barriers against wave action.",
    category: "erosion",
    difficulty: "medium"
  },
  {
    id: 9,
    question: "What is one effective way to prevent coastal erosion?",
    options: [
      "Building more roads",
      "Planting coastal vegetation",
      "Removing all structures",
      "Draining wetlands"
    ],
    correctAnswer: 1,
    explanation: "Planting coastal vegetation like mangroves and beach grasses can help prevent erosion by stabilizing soil and reducing wave impact.",
    category: "erosion",
    difficulty: "easy"
  },

  // Safety Questions
  {
    id: 10,
    question: "What should you do if you're caught in a rip current?",
    options: [
      "Swim directly toward shore",
      "Swim parallel to the shore",
      "Panic and call for help",
      "Dive underwater"
    ],
    correctAnswer: 1,
    explanation: "If caught in a rip current, swim parallel to the shore to escape the current, then swim back to shore.",
    category: "safety",
    difficulty: "easy"
  },
  {
    id: 11,
    question: "What color flag indicates dangerous swimming conditions?",
    options: [
      "Green",
      "Yellow",
      "Red",
      "Blue"
    ],
    correctAnswer: 2,
    explanation: "A red flag indicates dangerous swimming conditions and you should avoid entering the water.",
    category: "safety",
    difficulty: "easy"
  },
  {
    id: 12,
    question: "What should you do before going to the beach?",
    options: [
      "Check the weather forecast",
      "Bring only a towel",
      "Go alone for safety",
      "Ignore warning signs"
    ],
    correctAnswer: 0,
    explanation: "Always check the weather forecast and beach conditions before going to the beach for safety.",
    category: "safety",
    difficulty: "easy"
  },

  // Preparedness Questions
  {
    id: 13,
    question: "What should be in your emergency kit for coastal areas?",
    options: [
      "Only food and water",
      "Food, water, first aid, flashlight, and important documents",
      "Just a phone",
      "Nothing special"
    ],
    correctAnswer: 1,
    explanation: "An emergency kit should include food, water, first aid supplies, flashlight, and important documents for coastal emergencies.",
    category: "preparedness",
    difficulty: "medium"
  },
  {
    id: 14,
    question: "What is the best way to stay informed about coastal threats?",
    options: [
      "Ignore all warnings",
      "Only check social media",
      "Monitor official weather services and emergency broadcasts",
      "Ask neighbors only"
    ],
    correctAnswer: 2,
    explanation: "Monitor official weather services and emergency broadcasts for accurate and timely information about coastal threats.",
    category: "preparedness",
    difficulty: "easy"
  },
  {
    id: 15,
    question: "What should you do if a hurricane warning is issued?",
    options: [
      "Go to the beach to watch",
      "Stay at home and wait",
      "Follow evacuation orders and emergency instructions",
      "Continue normal activities"
    ],
    correctAnswer: 2,
    explanation: "If a hurricane warning is issued, follow evacuation orders and emergency instructions from local authorities.",
    category: "preparedness",
    difficulty: "easy"
  }
];

const CoastalQuiz: React.FC<CoastalQuizProps> = ({ onComplete, onClose, category }) => {
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [showExplanation, setShowExplanation] = useState(false);
  const [score, setScore] = useState(0);
  const [startTime, setStartTime] = useState<number>(Date.now());
  const [quizComplete, setQuizComplete] = useState(false);

  // Filter questions based on category
  const filteredQuestions = category 
    ? coastalQuizQuestions.filter(q => q.category === category)
    : coastalQuizQuestions;

  const currentQuestion = filteredQuestions[currentQuestionIndex];
  const totalQuestions = filteredQuestions.length;

  useEffect(() => {
    setStartTime(Date.now());
  }, []);

  const handleAnswerSelect = (answerIndex: number) => {
    if (selectedAnswer !== null) return; // Prevent multiple selections
    setSelectedAnswer(answerIndex);
  };

  const handleNextQuestion = () => {
    if (selectedAnswer === currentQuestion.correctAnswer) {
      setScore(score + 1);
    }

    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(currentQuestionIndex + 1);
      setSelectedAnswer(null);
      setShowExplanation(false);
    } else {
      // Quiz complete
      const finalScore = selectedAnswer === currentQuestion.correctAnswer ? score + 1 : score;
      const timeTaken = Math.floor((Date.now() - startTime) / 1000);
      
      const result: QuizResult = {
        score: Math.round((finalScore / totalQuestions) * 100),
        totalQuestions: totalQuestions,
        correctAnswers: finalScore,
        timeTaken: timeTaken,
        categoryScores: {
          [currentQuestion.category]: Math.round((finalScore / totalQuestions) * 100)
        }
      };

      setQuizComplete(true);
      onComplete(result);
    }
  };

  const getProgressPercentage = () => {
    return ((currentQuestionIndex + 1) / totalQuestions) * 100;
  };

  const getScoreMessage = (score: number) => {
    if (score >= 90) return "Coastal Safety Expert! 🌊🏆";
    if (score >= 80) return "Strong Knowledge! 🌊👍";
    if (score >= 70) return "Good Understanding! 🌊✅";
    if (score >= 60) return "Needs Improvement! 🌊📚";
    return "Keep Studying! 🌊💪";
  };

  if (quizComplete) {
    return null; // Quiz is handled by parent component
  }

  return (
    <Card className="w-full max-w-5xl mx-auto bg-white/95 backdrop-blur-sm border-0 shadow-2xl">
      <CardHeader className="bg-gradient-to-r from-blue-50 to-purple-50 border-b border-slate-200">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-3 text-2xl font-bold text-slate-800">
            <div className="p-2 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600">
              <Brain className="h-6 w-6 text-white" />
            </div>
            {category ? `${category.charAt(0).toUpperCase() + category.slice(1)} Quiz` : 'Complete Coastal Safety Quiz'}
          </CardTitle>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={onClose}
            className="hover:bg-slate-200 rounded-full p-2"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>
        <div className="space-y-3">
          <div className="flex justify-between text-sm text-slate-600">
            <span className="font-medium">Question {currentQuestionIndex + 1} of {totalQuestions}</span>
            <span className="font-medium">Score: {score}/{currentQuestionIndex + (selectedAnswer === currentQuestion.correctAnswer ? 1 : 0)}</span>
          </div>
          <div className="relative">
            <div className="w-full bg-slate-200 rounded-full h-3">
              <div 
                className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500 ease-out"
                style={{ width: `${getProgressPercentage()}%` }}
              ></div>
            </div>
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 opacity-20 rounded-full animate-pulse"></div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-8 space-y-8">
        {/* Question */}
        <div className="space-y-6">
          <div className="flex items-center gap-3 mb-4">
            <Badge variant="outline" className="bg-slate-100 border-slate-300 text-slate-700">
              {currentQuestion.category.replace('-', ' ').toUpperCase()}
            </Badge>
            <Badge variant="outline" className="bg-blue-100 border-blue-300 text-blue-700">
              {currentQuestion.difficulty.charAt(0).toUpperCase() + currentQuestion.difficulty.slice(1)}
            </Badge>
          </div>
          
          <h3 className="text-2xl font-bold text-slate-800 leading-relaxed">{currentQuestion.question}</h3>
          
          {/* Answer Options */}
          <div className="space-y-4">
            {currentQuestion.options.map((option, index) => (
              <button
                key={index}
                onClick={() => handleAnswerSelect(index)}
                disabled={selectedAnswer !== null}
                className={`w-full p-6 text-left rounded-xl border-2 transition-all duration-200 group ${
                  selectedAnswer === index
                    ? index === currentQuestion.correctAnswer
                      ? 'bg-green-50 border-green-500 text-green-800 shadow-lg scale-105'
                      : 'bg-red-50 border-red-500 text-red-800 shadow-lg scale-105'
                    : selectedAnswer !== null && index === currentQuestion.correctAnswer
                    ? 'bg-green-50 border-green-500 text-green-800 shadow-lg scale-105'
                    : 'bg-white border-slate-200 hover:border-blue-300 hover:bg-blue-50 hover:shadow-md'
                }`}
              >
                <div className="flex items-center gap-4">
                  <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center text-sm font-bold transition-all duration-200 ${
                    selectedAnswer === index
                      ? index === currentQuestion.correctAnswer
                        ? 'bg-green-500 border-green-500 text-white scale-110'
                        : 'bg-red-500 border-red-500 text-white scale-110'
                      : selectedAnswer !== null && index === currentQuestion.correctAnswer
                      ? 'bg-green-500 border-green-500 text-white scale-110'
                      : 'border-slate-300 bg-white group-hover:border-blue-400 group-hover:bg-blue-50'
                  }`}>
                    {String.fromCharCode(65 + index)}
                  </div>
                  <span className="text-lg font-medium">{option}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Explanation */}
        {selectedAnswer !== null && (
          <div className={`p-6 rounded-xl border-2 ${
            selectedAnswer === currentQuestion.correctAnswer 
              ? 'border-green-200 bg-green-50' 
              : 'border-red-200 bg-red-50'
          } animate-in slide-in-from-bottom-2 duration-300`}>
            <div className="flex items-start gap-4">
              {selectedAnswer === currentQuestion.correctAnswer ? (
                <div className="p-2 rounded-full bg-green-100">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
              ) : (
                <div className="p-2 rounded-full bg-red-100">
                  <XCircle className="h-6 w-6 text-red-600" />
                </div>
              )}
              <div className="flex-1">
                <div className="font-bold text-lg mb-2">
                  {selectedAnswer === currentQuestion.correctAnswer ? 'Correct! 🎉' : 'Incorrect'}
                </div>
                <p className="text-slate-700 leading-relaxed">{currentQuestion.explanation}</p>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <div className="flex justify-between items-center pt-6 border-t border-slate-200">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-slate-500">
              <Clock className="h-4 w-4" />
              <span>Take your time to think</span>
            </div>
          </div>
          
          <Button 
            onClick={handleNextQuestion}
            disabled={selectedAnswer === null}
            className={`min-w-[140px] h-12 text-lg font-semibold transition-all duration-200 ${
              selectedAnswer === null 
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed' 
                : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:shadow-lg hover:scale-105'
            }`}
          >
            {currentQuestionIndex < totalQuestions - 1 ? 'Next Question' : 'Finish Quiz'}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default CoastalQuiz;
