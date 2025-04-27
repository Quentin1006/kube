package main

import (
	"flag"
	quizresult "quiz/QuizResult"
)

func main() {
	quiz := quizresult.QuizResult{}

	var filename string
	flag.StringVar(&filename, "file", "problems.csv", "path to the quiz file")
	flag.Parse()

	quiz.InitQuiz(filename)

	quiz.StartQuiz()
	quiz.ShowResults()

}
