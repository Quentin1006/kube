package main

import (
	"sort"
)

func TwoOldestAges(ages []int) [2]int {
	lastTwo := [2]int{}
	sort.Ints(ages)
	copy(lastTwo[:], ages[len(ages)-2:])
	return lastTwo
}
