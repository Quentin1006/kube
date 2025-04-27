package quizresult

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"slices"
	"strings"
	"time"
)

var MaxAttemps = 3

type Problem struct {
	Number      int
	Question    string
	Solution    string
	UserAnswers []string
	TimeTaken   time.Duration
}

func (p Problem) Attempts() int {
	return len(p.UserAnswers)
}

func (p Problem) IsCorrect() bool {
	return slices.Contains(p.UserAnswers, p.Solution)
}

func (p *Problem) AddAnswer(answer string) {
	p.UserAnswers = append(p.UserAnswers, answer)
}

func (p *Problem) validate(answer string) bool {
	answer = strings.TrimSpace(strings.ReplaceAll(answer, "\r\n", ""))
	p.AddAnswer(answer)
	return p.Solution == answer
}

func (p *Problem) Ask() {
	reader := bufio.NewReader(os.Stdin)

	isValid := false
	startProblemTime := time.Now()
	for !isValid && p.Attempts() < MaxAttemps {

		fmt.Printf("Problem #%d: %s = ", p.Number, p.Question)
		answer, _ := reader.ReadString('\n')
		isValid = p.validate(answer)

		if !isValid {
			fmt.Printf("Incorrect! You have %d attempts left.\n", MaxAttemps-p.Attempts())
		} else {
			fmt.Println("Correct!")
		}

	}
	p.TimeTaken = time.Since(startProblemTime)
}

type QuizResult struct {
	results []Problem
}

func (q QuizResult) score() [2]int {
	score := 0
	total := len(q.results)

	for _, result := range q.results {
		if result.IsCorrect() {
			score++
		}
	}

	return [2]int{score, total}
}

func (q *QuizResult) addProblem(id int, question string, solution string) {
	problem := Problem{
		Number:   id,
		Question: question,
		Solution: solution,
	}
	q.results = append(q.results, problem)
}

func (q *QuizResult) InitQuiz(filename string) {
	file, err := os.ReadFile(filename)
	if err != nil {
		log.Fatal("Error reading file:", err)
	}

	content := string(file)

	if len(content) == 0 {
		fmt.Println("No problems to show")

	}
	problems := strings.Split(content, "\r\n")

	for idx, problem := range problems {
		if problem == "" {
			continue
		}

		parts := strings.Split(problem, ",")
		question, solution := parts[0], parts[1]

		q.addProblem(idx+1, question, solution)
	}

}

func (q *QuizResult) StartQuiz() {
	for _, result := range q.results {
		result.Ask()
	}
}

func (q *QuizResult) ShowResults() {
	fmt.Println("Quiz Results:")
	fmt.Printf("Score: %d/%d\n", q.score()[0], q.score()[1])
	for _, result := range q.results {
		fmt.Printf("Problem #%d: %s\n", result.Number, result.Question)
		fmt.Printf("Your answer(s): %s\n", strings.Join(result.UserAnswers, ", "))
		if result.IsCorrect() {
			fmt.Println("Correct!")
		} else {
			fmt.Printf("Incorrect! The correct answer is: %s\n", result.Solution)
		}
		fmt.Printf("Time taken: %v seconds\n", result.TimeTaken.Seconds())
	}
}
