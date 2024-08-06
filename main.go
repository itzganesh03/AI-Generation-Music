package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"path/filepath"
)

type Card struct {
	Title       string `json:"title"`
	Description string `json:"description"`
	AudioURL    string `json:"audioUrl"`
	ImageURL    string `json:"imageUrl"`
}

type CardDetails struct {
	Cards []Card `json:"cards"`
}

func main() {
	http.HandleFunc("/", serveHTML)
	http.HandleFunc("/submit", corsMiddleware(submitHandler))
	http.HandleFunc("/cards", corsMiddleware(fetchCardsHandler)) // Add the fetch-cards endpoint

	fmt.Println("Server started at http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func serveHTML(w http.ResponseWriter, r *http.Request) {
	p := filepath.Join("static", "index.html")
	http.ServeFile(w, r, p)
}

func submitHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	var cardDetails CardDetails
	if err := json.NewDecoder(r.Body).Decode(&cardDetails); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Process the card details (e.g., save to a database)
	// For now, just print to the console
	fmt.Printf("Received card details: %+v\n", cardDetails)
	fmt.Println("################### successfully got data ######################")
	fmt.Println("")

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "success"})
}

func fetchCardsHandler(w http.ResponseWriter, r *http.Request) {

	if r.Method != http.MethodGet {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	// Simulate fetching cards from a data source
	cards := []Card{
		{Title: "Card 1", Description: "Description for card 1", AudioURL: "audio1.mp3", ImageURL: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr4_j6B_Rm1Om5WrQW6en163GJyhkE2awj9A&s"},
		{Title: "Card 2", Description: "Description for card 2", AudioURL: "audio1.mp3", ImageURL: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSr4_j6B_Rm1Om5WrQW6en163GJyhkE2awj9A&s"},
	}

	cardDetails := CardDetails{Cards: cards}
	fmt.Println("fetchCardsHandler called: \n", cardDetails) // Add this line
	fmt.Println("################### successfully fetch data ######################")
	fmt.Println("")

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(cardDetails); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if r.Method == http.MethodOptions {
			w.WriteHeader(http.StatusNoContent)
			return
		}

		next(w, r)
	}
}
